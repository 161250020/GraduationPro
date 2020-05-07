class Mail:
    def __init__(self, _id, title, from_email, to_email, cc, date, doc, split, emailKind):
        self._id = _id
        self.title = title
        self.from_email = from_email
        self.to_email = to_email
        self.cc = cc
        self.date = date
        self.doc = doc
        self.split = split
        self.emailKind = emailKind

