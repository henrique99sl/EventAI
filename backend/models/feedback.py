from . import db


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)  # CORRIGIDO!
    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(32), nullable=True)
    topics = db.Column(db.Text, nullable=True)  # comma-separated or JSON
    created_at = db.Column(db.DateTime, server_default=db.func.now())
