from datetime import datetime

from flask import Blueprint, request, abort

from diaphragm.counter.models import Visitor
from diaphragm.database import db
from diaphragm.utils import render_ajax, json_dict

counter = Blueprint('counter', __name__,
                    template_folder="templates")


@counter.route('/api/counter')
def show_status():
    ipaddr = request.environ.get('REMOTE_ADDR')
    visitor = Visitor.query.filter(Visitor.ipaddr == ipaddr).first()
    return render_ajax("counter.html", visitor=visitor,
                       visits_today=Visitor.total_today_visits(),
                       visits_total=Visitor.total_visits(),
                       views_today=Visitor.total_today_views(),
                       views_total=Visitor.total_views())


@counter.before_app_request
def accept_visitor():
    ip, visitor = get_current_visitor()

    if ip is None:
        return

    if visitor is None:
        visitor = Visitor(ip, request.path)
        db.session.add(visitor)
        db.session.commit()
        return

    if visitor.last_visit.date() < datetime.today().date():
        visitor.visits_today = 1
        visitor.views_today = 1
        db.session.add(visitor)
        db.session.commit()

    if is_too_fast(visitor):
        return json_dict(content="Wait-wait! You click too fast!", title="Fast")


def is_too_fast(visitor):
    too_fast = (datetime.utcnow() - visitor.last_visit).total_seconds() < 0.2
    same_page = request.path == visitor.last_page
    return too_fast and same_page


@counter.after_app_request
def count_visitor(r):
    ip, visitor = get_current_visitor()

    if not visitor:
        return r

    current_time = datetime.utcnow()

    if (current_time - visitor.last_visit).total_seconds() > 30 * 60:
        visitor.visits_today += 1
        visitor.visits_total += 1

    if visitor.last_page != request.path:
        visitor.views_today += 1
        visitor.views_total += 1

    visitor.last_visit = current_time
    visitor.last_page = request.path

    db.session.add(visitor)
    db.session.commit()

    return r


def get_current_visitor():
    if not request.path.startswith('/api') or request.path.startswith('/static'):
        return None, None

    ip = request.environ.get('REMOTE_ADDR')
    return ip, Visitor.query.filter(Visitor.ipaddr == ip).first()
