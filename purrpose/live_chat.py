"""Explicit chat actions for public links and fixed registry checks.

Raw user text, not model output, authorizes a fetch. Bare links ask first.
"""
from copy import deepcopy
import re
import time
from .memory import MemoryUnavailable
from .workflow_runs import record_memory_read

ORG=('our rescue','our organization','our organisation','my organization','my organisation',
     'as organization','as an organization','as a rescue organization','organization view',
     'i run a rescue','i represent','my rescue','我们组织','我们机构','我的组织','我的机构','我是组织','我们官网','我们的官网')
SUPPORT=('i want to help','want to donate','want to support','supporter','donor','我要捐','我想捐','我想帮助','想支持','捐助者')
BOTH=('both','两者','两个都','兼备')
REVIEW=('review','check','assess','read','inspect','evaluate','verify','帮我看','检查','查证','核实','读取','缺什么','补什么','分析')
MISSING=('missing','gap','what to add','what should we publish','缺','补充','补什么')
HISTORY=('history','retained review','历史','记忆记录')
REFRESH=('refresh website','recheck website','read website again','重新读取网站','重新检查网站','刷新网站')


def audience(text):
    org=any(w in text for w in ORG) or text in ('organization','organisation','组织','机构')
    supporter=any(w in text for w in SUPPORT) or text in ('supporter','donor','捐助者')
    if any(w in text for w in BOTH) or org and supporter:return 'both'
    if org:return 'organization'
    if supporter:return 'supporter'
    return None


def result_reply(read,role,zh,retained=False):
    pages=read.get('organization_review',{}).get('pages_read',0)
    status=read['status']
    error=read.get('error','')
    reasons={
      'http_403':('The website declined automated access, so I could not read its pages.','该网站拒绝了自动读取，本次没能取得页面内容。'),
      'http_404':('The requested page could not be found. Please check the public link.','没有找到这个页面，请检查公开链接是否正确。'),
      'http_429':('The website is limiting requests. I stopped rather than retrying.','网站目前限制访问频率，我已停止，没有反复尝试。'),
      'response_too_large':('This page is larger than the demo can safely read. You could provide a shorter public case page.','这个页面超过了 demo 的读取上限，可以改为提供较短的公开案例页面。'),
      'redirect_not_followed_enter_final_https_url':('This address redirects elsewhere. Please provide the final public HTTPS address shown in your browser.','这个地址会跳转，请提供浏览器最终显示的公开 HTTPS 地址。'),
      'robots_disallowed_entry':('The website’s access rules do not allow this automated read, so I stopped.','网站的访问规则不允许这次自动读取，因此我已停止。'),
      'robots_scheduler_required':('The website requires a slower reading schedule than this demo supports, so I stopped.','网站要求按特定间隔读取，目前 demo 暂不支持，因此我已停止。'),
      'login_or_challenge_page_not_supported':('The page requires login or a browser check that this demo cannot complete.','页面要求登录或浏览器验证，目前 demo 无法完成。'),
      'insufficient_readable_text':('I could not extract enough readable text from this page to assess it.','没能从页面中提取足够的可读文字，因此暂时无法评估。')}
    if pages==0:
        fallback=('I could not complete the website read. No usable page content was available to assess.',
                  '本次没能完成网站读取，没有取得可供评估的页面内容。')
        if read['status']=='blocked':fallback=('This link is outside the demo’s supported public HTTPS addresses. Please provide a public website or case page.',
                                             '这个链接不符合 demo 支持的公开 HTTPS 地址要求，请提供公开官网或案例页面。')
        summary=reasons.get(error,fallback)[1 if zh else 0]
        reply=summary+(' 因此暂时无法判断这项需求或还缺多少钱。读取失败不代表组织或募款不可信。' if zh else
                       ' I cannot assess the need or remaining amount from this attempt. An access failure is not evidence of wrongdoing.')
    else:
        partial=read['status']!='read_complete'
        summary=(f'读到了 {pages} 个公开页面。'+('另有页面未能读取。' if partial else '')) if zh else (
                 f'I read {pages} public '+('page.' if pages==1 else 'pages.')+(' Some other pages could not be read.' if partial else ''))
        reply=summary+(' 这些内容是网站自己的说法，尚未独立核实；目前仍无法确认具体缺款金额。' if zh else
                       ' These are the website’s own statements, not independently verified evidence. A reliable remaining amount is still unknown.')
        if role in ('organization','both'):reply+=(' 右侧 Review 列出了本次已读范围内找到的信息、缺口和补充建议。' if zh else
                                                 ' Open Review to see what was found, what is missing from these pages, and what to publish or clarify.')
    if role in ('organization','both'):
        if pages:
            reply=summary+(' 以下是本次已读页面的材料检查摘要。出现相关文字不代表证据已核实，没找到也不代表整个网站没有。' if zh else
                ' Here is the publication checklist for the pages I read. Related wording is not verified evidence; not found here does not mean absent from your entire website.')
        else:
            reply=summary+(' 因为未能读到内容，暂时无法判断你们已公布什么材料。下面只能提供通用清单，不是针对官网完成的审查，也不代表组织不可信。' if zh else
                ' I cannot tell what you have already published. The checklist below is general guidance, not a completed review of your website or an adverse finding about your organization.')
    if retained:reply=('以下是之前保存的读取结果，没有重新访问网站。' if zh else 'This is the previously saved read; I have not visited the website again. ')+reply
    memory=read.get('memory',{}).get('status')
    if memory=='saved':memory_note=(('已保存本次未能读取的检查记录，没有核实任何证据。' if pages==0 else '已保存本次读取内容和未解决的问题。') if zh else
                                    ('Saved a record of the unsuccessful check; no evidence was verified.' if pages==0 else 'Saved the source observations and open questions.'))
    elif memory=='save_failed':memory_note='这次记录未能保存。' if zh else 'This check could not be saved.'
    else:memory_note='本次检查没有写入记忆。' if zh else 'This check was not saved to memory.'
    response={'reply':reply,'mode':'explicit_public_workflow','new_cloud_calls':0,'site_review':deepcopy(read),
              'audience':role,'retained_source_read':retained,'source_summary':summary,'memory_note':memory_note}
    if role in ('organization','both'):
        response['live_organization_review']=deepcopy(read.get('organization_review'))
        response['publication_checklist']=deepcopy(read.get('organization_review',{}).get('fields',[]))
    return response


def handle(app,state,message,zh):
    text=message.strip().casefold()
    urls=[u.rstrip('.,，。)）') for u in re.findall(r'https?://[^\s<>"\[\]]+',message,re.I)]
    def answer(en,cn,**extra):return {'reply':cn if zh else en,'mode':'explicit_public_workflow','new_cloud_calls':0,**extra}
    if urls:
        if any(w in text for w in ("don't",'do not','不要','别读取','不允许')):
            return answer('No website was fetched. Tell me if and how you want the link reviewed.','没有读取网站。请明确是否检查以及从哪个角度检查。')
        if len(urls)!=1:
            return answer('Please give one public website or case URL at a time. No website was fetched.','一次请给一个公开官网或案例网址；没有读取网站。')
        role=audience(text) or ('organization' if state.get('awaiting_organization_url') else None)
        requested=role or any(w in text for w in REVIEW)
        if not requested:
            state['pending_public_url']=urls[0]
            return answer('Would you like me to review this public link as a supporter, a rescue organization, or both? Reply “supporter”, “organization” or “both”. No website has been fetched.',
                          '你希望从捐助者、组织，还是两者角度检查？回复“捐助者”“组织”或“两者”。目前没有读取网站。')
        role=role or 'supporter'
        read=app.dispatch('/api/discover-url',{'url':urls[0]})
        state.update(public_url=urls[0],public_audience=role,public_read=read,tool_context='website',research=False,active=False)
        state.pop('pending_public_url',None)
        state.pop('awaiting_organization_url',None)
        return result_reply(read,role,zh)
    if state.get('pending_public_url'):
        role=audience(text)
        if role:
            url=state.pop('pending_public_url');read=app.dispatch('/api/discover-url',{'url':url})
            state.update(public_url=url,public_audience=role,public_read=read,tool_context='website',research=False,active=False)
            return result_reply(read,role,zh)
    from .directory_chat import handle as directory_handle
    directory_response=directory_handle(app,state,message,zh)
    if directory_response is not None:return directory_response
    registry=any(w in text for w in ('zetaris','charity registry','registry check','check registry','登记查询','登记资料查询'))
    if registry and not any(w in text for w in HISTORY):
        target='Toronto Cat Rescue' if app.registry.case_id=='REAL-TCR-REGISTRY' else 'Guelph Humane Society'
        # Registry scope is fixed and separate: never apply Toronto Cat Rescue rows to a new website.
        if target.casefold() not in text or 'north toronto' in text:
            return answer('The configured registry lookup only checks '+target+' historical 2024 information, separately from your website. Say “check '+target+' charity registry” to run that specific lookup. It cannot verify another organization.',
                          '当前登记查询只支持 '+target+' 的2024年历史资料，与新网站无关。请说“check '+target+' charity registry”执行这项固定查询；不能用它核实其他组织。')
        if not any(w in text for w in ('check','query','lookup','run','查','查询')):
            return answer('Say “check '+target+' charity registry” to explicitly request the read-only lookup.','请明确说“check '+target+' charity registry”再执行只读查询。')
        result=app.dispatch('/api/registry',{})
        state.update(registry_read=result,tool_context='registry')
        return answer('Zetaris historical lookup for '+target+': '+result['status']+'. This is not current registration, case-need or trust verification.',
                      'Zetaris 对 '+target+' 的历史查询结果：'+result['status']+'。不是当前登记、需求或可信认证。',registry_result=result)
    if state.get('tool_context')=='registry' and any(w in text for w in HISTORY) and 'website' not in text and '网站' not in text:
        started=time.time()
        try:
            history=app.dispatch('/api/registry/history',{});status='not_configured' if history.get('status')=='history_unavailable' else 'ok'
        except MemoryUnavailable:history={'status':'history_unavailable'};status='failed'
        record_memory_read(app,app.registry.case_id,history,started,status)
        return answer('Retained registry history only; no fresh SQL or website request.', '这是保存的登记查询历史，没有重新执行 SQL 或读取网站。',workflow_history=history)
    if 'lucy' in text or 'fictional' in text or '虚构' in text:return None
    read=state.get('public_read') if state.get('tool_context')=='website' or 'website' in text or '网站' in text else None
    if read:
        role=audience(text)
        if role:
            state.update(public_audience=role,tool_context='website')
            return result_reply(read,role,zh,retained=True)
        if any(w in text for w in REFRESH) or text in ('refresh','recheck','重新检查','刷新'):
            read=app.dispatch('/api/discover-url',{'url':state['public_url']})
            state.update(public_read=read,tool_context='website')
            return result_reply(read,state['public_audience'],zh)
        if any(w in text for w in HISTORY):
            started=time.time();case='SITE-'+read.get('site_id','BLOCKED').upper()
            status='not_configured';history={'status':'history_unavailable'}
            if app.memory and read.get('site_id'):
                try:history=app.memory.call('recall',case);status='ok'
                except MemoryUnavailable:status='failed'
            record_memory_read(app,case,history,started,status)
            state['tool_context']='website'
            return answer('Retained source history only; no new website request. A saved read is not a current verification.',
                          '这是保存的来源历史，没有重新读取网站；历史记录不是当前核实。',workflow_history=history)
        if any(w in text for w in (*MISSING,'evidence','source','how much','remaining','证据','来源','还缺多少','多少钱')):
            response=result_reply(read,state['public_audience'],zh,retained=True)
            pages=read.get('organization_review',{}).get('pages_read',0)
            if pages and any(w in text for w in ('how much','remaining','多少钱','还缺多少')):
                response['reply']=('还不能算出缺款。已读页面没有经过核实的同一案例费用、已收款和其他资助总额；不能用一般捐款档位或旧故事里的金额代替。没有重新访问网站。' if zh else
                    'The remaining amount is unknown. This read has no verified same-case cost, received total and other funding. General donation amounts or figures from other stories cannot substitute. I have not visited the website again.')
            elif pages and state['public_audience']=='supporter':
                response['reply']=('已有证据是本次读到的组织公开陈述，Review 中可查看原文与来源。仍需核实：当前登记与收款对象、对应猫咪的医疗材料、最新状况、同一案例的费用及已收款。页面中出现相关词语不代表材料已达标。没有重新访问网站。' if zh else
                    'The available evidence is the rescue’s published account, with quotes and source links in Review. Still to verify: current identity and recipient linkage, medical documentation for the named cat, its latest status, and same-case costs and funds received. Related wording does not mean these checks passed. I have not visited the website again.')
            return response
        return answer('I am still discussing the website you selected. Do you want its evidence, missing information, remaining funding, or a fresh website check? I have not searched or switched to another case.',
                      '我们仍在讨论你选中的网站。你想看证据、缺失信息、缺款，还是重新检查网站？本次没有搜索或切换到其他案例。')
    return None
