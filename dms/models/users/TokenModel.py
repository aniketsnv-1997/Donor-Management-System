from ...app import db


class TokenModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, id, jti, token_type, user_identity, revoked, expires, create_date):
        self.id = id
        self.jti = jti
        self.token_type = token_type
        self.user_identity = user_identity
        self.revoked = revoked
        self.expires = expires
        self.create_date = create_date
