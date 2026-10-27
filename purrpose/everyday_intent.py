"""Conservative everyday-language signals, never authority to verify evidence."""
import re
import unicodedata


def normalize(message):
    text=unicodedata.normalize('NFKC',message).casefold().replace('’',"'")
    text=re.sub(r"\bi(?:'d| would) (?:really )?like\b",'i want',text)
    text=re.sub(r'\bwanna\b','want to',text)
    for wrong,right in [('orgs','organizations'),('organisations','organizations'),('orgnizations','organizations'),
                        ('charites','charities'),('resuce','rescue'),('kitties','cats'),('kitty','cat'),('pls','please')]:
        text=re.sub(r'\b'+wrong+r'\b',right,text)
    for chinese,english in [('多伦多',' Toronto '),('渥太华',' Ottawa '),('安大略省',' Ontario '),('安省',' Ontario ')]:
        text=text.replace(chinese,english)
    return re.sub(r'\s+',' ',text).strip().casefold()


def discovery_signal(text):
    animal=bool(re.search(r'\b(cat|cats|kitten|kittens|feline)\b',text)) or '猫' in text
    organization=bool(re.search(r'\b(rescue|rescues|organizations|charities|shelters|shelter)\b',text))
    action=bool(re.search(r'\b(find|finding|looking|search|searching|recommend|suggest|list|show|help|support|donate|donating|give|giving)\b',text))
    action=action or any(w in text for w in ('想帮','帮助','捐','找','推荐','救助','支持','看看'))
    return animal and action, organization and action


def organization_signal(text):
    return bool(re.search(r"\b(?:i|we) (?:run|represent|manage|operate)\b.*\b(rescue|shelter|organization)\b",text)) or bool(re.search(
        r"\b(?:our|my) (?:rescue|shelter|organization)\b|\bi(?:'m| am) (?:a|an) (?:rescue|organization)\b",text)) or any(
        w in text for w in ('我是救助组织','我们是救助','我们机构','我们组织','我的机构','我们的官网'))
