from math import ceil

from flask import abort, Blueprint
from flask import request
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from diaphragm.board.forms import ThreadForm, PostForm
from diaphragm.board.models import Post, Thread, db, Like, Dislike
from diaphragm.board.utils import send_xml
from diaphragm.utils import render_ajax, json_dict, thumbnail, safely_upload, shorten


board = Blueprint("board", __name__,
                  static_folder="static",
                  static_url_path="/static/board",
                  template_folder="templates")


BUMP_LIMIT = 500
PAGES = 3
THREADS_PER_PAGE = 4


@board.route("/api/start_thread", methods=["POST"])
def start_thread():
    form = ThreadForm()

    if not form.validate_on_submit():
        abort(400)

    thread = Thread(form.subject.data)
    post = create_post(thread, form)

    if Thread.query.count() >= PAGES * THREADS_PER_PAGE:
        last_thread = Thread.query.order_by(Thread.bump).first()
        last_thread.posts.delete()
        db.session.delete(last_thread)

    db.session.add(thread)
    db.session.add(post)
    db.session.commit()
    return json_dict(thread_id=thread.id)


@board.route("/api/post_message", methods=["POST"])
def post_message():
    form = PostForm()

    if not form.validate_on_submit():
        abort(400)

    thread = Thread.query.filter(Thread.id == form.thread.data).first()

    if not thread:
        abort(404)

    post = create_post(thread, form)

    if thread.posts.count() < BUMP_LIMIT:
        thread.bump = post.time
        db.session.add(thread)

    db.session.add(post)
    db.session.commit()
    return json_dict(post_id=post.id)


def create_post(thread, form):
    if not form.fileupload.data:
        return Post(thread, form.message.data, form.author.data)
    else:
        attachment = safely_upload(board.static_folder, form.fileupload.data)
        if attachment is None:
            abort(400)
        return Post(thread, form.message.data, form.author.data, attachment)


@board.route("/api/board/page/<page>")
@board.route("/api/board/page/<page>/<image>")
def show_board_page(page, image=None):
    try:
        page = int(page)
    except:
        abort(404)

    threads = Thread.query\
        .order_by(Thread.bump.desc()) \
        .limit(THREADS_PER_PAGE) \
        .offset(page*THREADS_PER_PAGE)\
        .all()

    if len(threads) == 0 and page != 0:
        abort(404)

    threads = [(t, t.op(), shorten(t.op().message), t.posts.count()-1) for t in threads]

    form = ThreadForm()

    threads_count = Thread.query.count()
    pages_count = int(ceil(threads_count / float(THREADS_PER_PAGE)))

    return render_ajax("board.html", threads=threads, form=form,
                       thumbnail=thumbnail, full_size=image,
                       pages=pages_count, current_page=page)


@board.route("/api/board")
@board.route("/api/board/<image>")
def show_board(image=None):
    return show_board_page(0, image)


@board.route("/api/board/thread/<thread_id>")
@board.route("/api/board/thread/<thread_id>/<image>")
def show_thread(thread_id, image=None):
    thread = Thread.query.filter(Thread.id == thread_id).first()

    if not thread:
        abort(404)

    op = thread.op()
    form = PostForm(thread=thread.id)
    posts = thread.posts.filter(Post.id != op.id)
    return render_ajax("thread.html", op=op, thread=thread,
                       posts=posts, form=form,
                       thumbnail=thumbnail, full_size=image)


@board.route("/ajaxapi/board/thread/<thread_id>/new/<last_post_id>")
def get_new_posts(thread_id, last_post_id):
    thread = Thread.query.filter(Thread.id == thread_id).first()

    if not thread:
        abort(404)

    posts = thread.posts.filter(Post.id > last_post_id)

    return render_ajax("posts.html", posts=posts,
                       thumbnail=thumbnail)


@board.route("/board/download/<thread_id>")
def download_thread(thread_id):
    thread = Thread.query.filter(Thread.id == thread_id).first()

    if not thread:
        abort(404)

    return send_xml([(thread, thread.posts.all())], "thread-{}.xml".format(thread_id))


@board.route("/board/download/all")
def download_all():
    threads = ((thread, thread.posts.all()) for thread in Thread.query.all())
    return send_xml(threads, "threads-all.xml")


@board.route("/ajaxapi/board/like/<post_id>", methods=['POST'])
def like(post_id):
    return do_like_or_dislike(post_id, Like, lambda p: p.likes)


@board.route("/ajaxapi/board/dislike/<post_id>", methods=['POST'])
def dislike(post_id):
    return do_like_or_dislike(post_id, Dislike, lambda p: p.dislikes)


@board.route("/ajaxapi/board/likes/<post_id>", methods=['GET'])
def get_likes(post_id):
    post = Post.query.filter(Post.id == post_id).first()

    if not post:
        abort(404)

    return json_dict(likes_count=post.likes.count(),
                     dislikes_count=post.dislikes.count())


def do_like_or_dislike(post_id, factory, ret):
    ip_addr = request.environ.get('REMOTE_ADDR')
    post = Post.query.filter(Post.id == post_id).first()

    if not post:
        abort(404)

    like = factory(post_id, ip_addr)
    db.session.add(like)

    try:
        db.session.commit()
    except (IntegrityError, InvalidRequestError):
        db.session.rollback()

        like = ret(post).filter(factory.ip_address == ip_addr).scalar()
        db.session.delete(like)
        db.session.commit()

    return json_dict(count=ret(post).count())
