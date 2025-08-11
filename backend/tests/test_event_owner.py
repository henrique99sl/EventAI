import pytest
from datetime import date
from app import create_app, db
from models.user import User
from models.event import Event


@pytest.fixture
def client():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            user = User(
                username="owner",
                email="owner@test.com",
                password_hash="123",
                role="user",
            )
            db.session.add(user)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()


def test_create_event_with_owner(client):
    with client.application.app_context():
        owner = User.query.first()
        event = Event(
            name="Test Event",
            date=date(2025, 12, 12),  # Corrigido para datetime.date
            venue_id=1,
            owner_id=owner.id,
        )
        db.session.add(event)
        db.session.commit()

        saved_event = Event.query.filter_by(name="Test Event").first()
        assert saved_event is not None
        assert saved_event.owner_id == owner.id
