from models import db
from models.user import User
from models.event import Event
from models.recommendation import Recommendation
from datetime import date


def some_model(user, event):
    # Exemplo simples: score mais alto para eventos mais próximos e de interesse do usuário
    return 1.0 / (1 + abs((event.date - date.today()).days))


def calculate_and_save_recommendations():
    users = User.query.all()
    for user in users:
        events = Event.query.filter(Event.date >= date.today()).all()
        recommended = []
        for event in events:
            score = some_model(user, event)
            recommended.append((event, score))
        recommended.sort(key=lambda x: x[1], reverse=True)
        # Opcional: Limpar recomendações antigas para este usuário
        # Recommendation.query.filter_by(user_id=user.id).delete()
        for event, score in recommended[:5]:
            rec = Recommendation(user_id=user.id, event_id=event.id, score=score)
            db.session.merge(rec)
    db.session.commit()


if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        calculate_and_save_recommendations()
