from flask import Blueprint, request, jsonify
from models.event import Event

calendar_bp = Blueprint("calendar", __name__)


@calendar_bp.route("/events/calendar")
def events_calendar():
    start = request.args.get("start")
    end = request.args.get("end")
    query = Event.query
    if start:
        query = query.filter(Event.date >= start)
    if end:
        query = query.filter(Event.date <= end)
    events = query.order_by(Event.date).all()
    result = [
        {
            "id": ev.id,
            "name": ev.name,
            "date": ev.date.isoformat(),
            "venue": ev.venue_id,
        }
        for ev in events
    ]
    return jsonify(result)
