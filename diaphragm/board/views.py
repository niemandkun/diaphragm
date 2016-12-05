from flask import abort, Blueprint

from diaphragm.board.forms import ThreadForm, PostForm
from diaphragm.board.models import Post, Thread, db
from diaphragm.utils import render_ajax, json_dict, thumbnail, safely_upload, pluralize, shorten

board = Blueprint("board", __name__,
                  static_folder="static",
                  static_url_path="/static/board",
                  template_folder="templates")


@board.route("/api/start_thread", methods=["POST"])
def start_thread():
    form = ThreadForm()

    if not form.validate_on_submit():
        abort(400)

    thread = Thread(form.subject.data)
    post = create_post(thread, form)

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


@board.route("/api/board")
@board.route("/api/board/<image>")
def show_board(image=None):
    threads = Thread.query.all()
    threads = [(t, t.op(), shorten(t.op().message), t.posts.count()) for t in threads]

    form = ThreadForm()
    return render_ajax("board.html", threads=threads, form=form,
                       thumbnail=thumbnail, full_size=image,
                       pluralize=pluralize)


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
