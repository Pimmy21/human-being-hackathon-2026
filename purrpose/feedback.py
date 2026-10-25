"""Bounded process-local feedback receipts; suggestions never become evidence."""
from copy import deepcopy
from datetime import datetime, timezone
import re


class Feedback:
    def __init__(self, conversation):
        self.conversation = conversation
        self.receipts = {}

    def submit(self, *, session_id, request_id, kind, message, city=None):
        if (not isinstance(session_id,str) or not re.fullmatch(r'[A-Za-z0-9-]{1,80}',session_id)
                or not isinstance(request_id,str) or not re.fullmatch(r'[A-Za-z0-9-]{1,80}',request_id)
                or kind not in ('preference','correction','policy_suggestion')
                or not isinstance(message,str) or not 1 <= len(message.strip()) <= 800):
            raise ValueError('Invalid feedback')
        if kind == 'preference':
            if city not in ('Ottawa','Toronto','Ontario'):
                raise ValueError('Choose a supported preference')
        elif city is not None:
            raise ValueError('Only preference feedback can set a city')
        key=(session_id,request_id)
        inputs=(kind,message,city)
        if key in self.receipts:
            previous,result=self.receipts[key]
            if previous != inputs: raise ValueError('Request ID reused for different feedback')
            return {**deepcopy(result),'idempotent_replay':True}
        if len(self.receipts)>=100:
            raise ValueError('Local feedback capacity reached')
        if kind=='preference':
            if session_id not in self.conversation.sessions:
                self.conversation.reply(session_id,'hi')
            state=self.conversation.sessions[session_id]
            state.update(city=None if city=='Ontario' else city, region_wide=city=='Ontario',
                         collection='real', research=False, active=False, expand=False)
            state.pop('last_live_read',None)
            status='session_preference_recorded'
            notice='Applied only to this conversation. Next discovery uses this city/region. No permanent donor profile.'
        elif kind=='correction':
            status='unverified_correction_lead'
            notice='Recorded as an unverified Lucy lead. No facts, qualification or sources changed. A permitted source refresh must be requested separately.'
        else:
            status='policy_suggestion_recorded'
            notice='Recorded for policy-owner consideration, not applied. One suggestion cannot create a universal trust rule.'
        result={'status':status,'kind':kind,'request_id':request_id,
                'recorded_at':datetime.now(timezone.utc).isoformat(),'notice':notice,
                'case_id':'REAL-LUCY-GHS' if kind!='preference' else None,
                'facts_changed':False,'qualification_changed':False,'policy_changed':False,
                'source_reads':0,'new_cloud_calls':0,'idempotent_replay':False,
                'storage':'process_memory_only; lost on server restart'}
        self.receipts[key]=(inputs,deepcopy(result))
        return result
