
def session_id(self):
    session_key = self.request.session.session_key
    if not session_key:
        session_key = self.request.session.create()
    return session_key
