from models import db

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": str(self.date) if self.date else None,
            "venue_id": self.venue_id
        }