from datetime import date
from models import Event, Venue


def get_next_event_response():
    next_event = Event.query.filter(Event.date >= date.today()).order_by(Event.date.asc()).first()
    if next_event:
        venue = Venue.query.get(next_event.venue_id)
        return (
            f"O próximo evento é '{next_event.name}' em "
            f"{venue.name if venue else 'local desconhecido'} "
            f"no dia {next_event.date.strftime('%d/%m/%Y')}."
        )
    else:
        return "Nenhum evento futuro encontrado."
