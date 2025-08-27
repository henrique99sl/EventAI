from . import db


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(32), nullable=True)
    topics = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "text": self.text,
            "sentiment": self.sentiment,
            "topics": self.topics,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }