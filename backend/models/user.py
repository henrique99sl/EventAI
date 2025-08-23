from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(20), default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
        }

    def __repr__(self):
        return f"<User {self.id} {self.username} {self.email} {self.role}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return (self.username == other.username and self.email == other.email
                and self.role == other.role)

    def __hash__(self):
        return hash((self.username, self.email, self.role))
