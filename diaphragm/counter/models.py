from datetime import datetime

from diaphragm.database import db
from sqlalchemy.sql import func


class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ipaddr = db.Column(db.String(20))
    last_page = db.Column(db.String(80))
    last_visit = db.Column(db.DateTime)
    visits_today = db.Column(db.Integer)
    visits_total = db.Column(db.Integer)
    views_today = db.Column(db.Integer)
    views_total = db.Column(db.Integer)

    def __init__(self, ipaddr, page):
        self.ipaddr = ipaddr
        self.last_visit = datetime.utcnow()
        self.visits_today = 1
        self.visits_total = 1
        self.views_today = 1
        self.views_total = 1
        self.last_page = page

    @staticmethod
    def total_visits():
        return db.session.query(func.sum(Visitor.visits_total)).all()[0][0]

    @staticmethod
    def total_today_visits():
        return db.session.query(func.sum(Visitor.visits_today)) \
            .filter(Visitor.last_visit >= datetime.today().date()).scalar()

    @staticmethod
    def total_views():
        return db.session.query(func.sum(Visitor.views_total)).all()[0][0]

    @staticmethod
    def total_today_views():
        return db.session.query(func.sum(Visitor.views_today))\
            .filter(Visitor.last_visit >= datetime.today().date()).scalar()

