from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importe os modelos APÓS criar o db para evitar circularidade
# from .venue import Venue
# from .event import Event
