from . import db


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    venue = db.relationship("Venue", backref="events")
    owner = db.relationship("User", backref="events")

    # Relacionamento opcional (permite acessar participações do evento)
    participations = db.relationship(
        "EventParticipation",
        backref="event",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date.isoformat(),
            "venue_id": self.venue_id,
            "owner_id": self.owner_id,
        }
