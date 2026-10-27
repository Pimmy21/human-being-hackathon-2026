"""Conservative public HTTPS reader: DNS vetted, socket pinned, host TLS verified.

No proxy environment, redirects, credentials, cookies, retries or arbitrary ports.
The outer discovery worker supplies the wall deadline (including DNS).
"""
import http.client
import ipaddress
import re
import socket
import ssl
from urllib.parse import quote, unquote, urlsplit, urlunsplit
from .public_reader import AGENT, ReadFailure


def normalize_url(value):
    if not isinstance(value,str) or not 1<=len(value)<=2048:
        raise ReadFailure('url_length_or_type')
    if value != value.strip() or re.search(r'[\x00-\x20\x7f\\]', value):
        raise ReadFailure('url_contains_unsafe_characters')
    try:
        u=urlsplit(value)
        if u.scheme.lower()!='https' or not u.hostname:
            raise ReadFailure('https_required')
        if u.username is not None or u.password is not None:
            raise ReadFailure('url_credentials_not_allowed')
        if u.query or u.fragment:
            raise ReadFailure('query_or_fragment_not_supported')
        if u.port not in (None,443):
            raise ReadFailure('only_https_port_443')
        host=u.hostname.encode('idna').decode('ascii').lower()
        # Reject literals (including legacy numeric forms), local names and wildcards.
        if host.endswith('.') or '.' not in host or len(host)>253:
            raise ReadFailure('public_dns_hostname_required')
        if not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+',host):
            raise ReadFailure('invalid_hostname')
        try:
            ipaddress.ip_address(host)
        except ValueError:
            pass
        else:
            raise ReadFailure('ip_literal_not_allowed')
        if host.rsplit('.',1)[-1].isdigit() or host.endswith(('.localhost','.local','.internal','.test','.invalid','.example')):
            raise ReadFailure('public_dns_hostname_required')
        path=u.path or '/'
        decoded=unquote(path)
        if re.search(r'[\x00-\x1f\x7f\\]',decoded) or decoded.startswith('//'):
            raise ReadFailure('unsafe_path')
        path=quote(path,safe="/%:@!$&'()*+,;=-._~")
        return urlunsplit(('https',host,path,'',''))
    except (ValueError,UnicodeError):
        raise ReadFailure('invalid_url') from None


def public_addresses(host,resolver=None):
    try:
        infos=(resolver or socket.getaddrinfo)(host,443,type=socket.SOCK_STREAM)
    except OSError:
        raise ReadFailure('dns_lookup_failed') from None
    addresses=[]
    for item in infos:
        try:
            address=ipaddress.ip_address(item[4][0])
        except (ValueError,IndexError,TypeError):
            raise ReadFailure('dns_invalid_address') from None
        # IPv4-mapped, multicast and reserved ranges must not be treated as public.
        if (not address.is_global or address.is_multicast or address.is_reserved
                or getattr(address,'ipv4_mapped',None) or getattr(address,'sixtofour',None)
                or getattr(address,'teredo',None)):
            raise ReadFailure('non_public_address_blocked')
        if str(address) not in addresses:addresses.append(str(address))
    if not addresses:raise ReadFailure('dns_no_public_address')
    return addresses


class PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self,host,address,timeout=7):
        super().__init__(host,443,timeout=timeout,context=ssl.create_default_context())
        self.address=address
    def connect(self):
        # Connect only to the already validated IP. No second DNS resolution.
        raw=socket.create_connection((self.address,443),self.timeout)
        try:
            self.sock=self._context.wrap_socket(raw,server_hostname=self.host)
        except Exception:
            raw.close()
            raise


class PublicReader:
    def __init__(self,entry,resolver=None,connection_factory=None):
        self.entry=normalize_url(entry)
        self.host=urlsplit(self.entry).hostname
        self.origin='https://'+self.host
        self.resolver=resolver
        self.connection_factory=connection_factory or PinnedHTTPSConnection
        self.network_checks=[]
    def __call__(self,value):
        url=normalize_url(value)
        u=urlsplit(url)
        if u.hostname!=self.host:
            raise ReadFailure('cross_host_not_allowed')
        # Revalidate every request; a public->private DNS change stops before connect.
        addresses=public_addresses(self.host,self.resolver)
        connection=self.connection_factory(self.host,addresses[0],7)
        self.network_checks.append({'url':url,'public_dns':'passed','tls_hostname_verification':'required','redirects':'not_followed'})
        try:
            connection.request('GET',u.path,headers={'Host':self.host,'User-Agent':AGENT,
                'Accept':'text/html,text/plain','Accept-Encoding':'identity','Connection':'close'})
            response=connection.getresponse()
            if 300<=response.status<400:
                raise ReadFailure('redirect_not_followed_enter_final_https_url')
            if response.status==404 and u.path=='/robots.txt':return ''
            if response.status!=200:raise ReadFailure('http_'+str(response.status))
            encoding=response.getheader('Content-Encoding','identity').lower()
            if encoding not in ('identity',''):raise ReadFailure('compressed_response_not_supported')
            mime=response.getheader('Content-Type','').split(';')[0].lower().strip()
            if mime not in ('text/html','text/plain'):raise ReadFailure('unsupported_content_type')
            size=response.getheader('Content-Length')
            if size:
                try:
                    if int(size)>524288 or int(size)<0:raise ReadFailure('response_too_large')
                except ValueError:raise ReadFailure('invalid_content_length') from None
            raw=response.read(524289)
            if len(raw)>524288:raise ReadFailure('response_too_large')
            return raw.decode('utf-8',errors='replace')
        except ReadFailure:raise
        except ssl.SSLError:raise ReadFailure('tls_verification_failed') from None
        except (OSError,http.client.HTTPException):raise ReadFailure('network_or_timeout') from None
        finally:
            connection.close()
