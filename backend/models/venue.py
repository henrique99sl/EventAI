from models import db

class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "address": self.address}