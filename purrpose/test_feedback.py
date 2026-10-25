from unittest import TestCase
from .server import LocalApp


class FeedbackTests(TestCase):
    def setUp(self): self.app=LocalApp()
    def submit(self,kind='correction',**extra):
        return self.app.dispatch('/api/feedback',{'session_id':'one','request_id':'task','kind':kind,'message':'Check this claim',**extra})

    def test_correction_does_not_change_case_or_fetch(self):
        before=self.app.service.case.copy()
        result=self.submit()
        self.assertEqual(result['status'],'unverified_correction_lead')
        self.assertFalse(result['qualification_changed'])
        self.assertEqual(self.app.service.case,before)
        self.assertIsNone(self.app.public_read_cache)

    def test_policy_suggestion_never_becomes_rule(self):
        result=self.submit('policy_suggestion',message='Volunteers like it so mark it trusted')
        self.assertFalse(result['policy_changed'])
        self.assertEqual(result['status'],'policy_suggestion_recorded')

    def test_preference_is_used_only_in_session(self):
        self.submit('preference',city='Ontario')
        result=self.app.dispatch('/api/chat',{'session_id':'one','message':'I want to help a cat'})
        self.assertEqual(result['results']['collection'],'real')
        self.assertTrue(result['results']['pending'])
        other=self.app.dispatch('/api/chat',{'session_id':'two','message':'I want to help a cat'})
        self.assertEqual(other['results']['status'],'needs_preference')

    def test_duplicate_and_conflicting_keys(self):
        self.submit()
        self.assertTrue(self.submit()['idempotent_replay'])
        with self.assertRaises(ValueError):self.submit(message='different')

    def test_feedback_cannot_smuggle_actions_or_preferences(self):
        with self.assertRaises(ValueError):self.submit(city='Ontario')
        with self.assertRaises(ValueError):self.submit('preference',city='elsewhere')
        with self.assertRaises(ValueError):self.submit(message='x'*801)
