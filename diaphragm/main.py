from os import path

from flask import Flask
from flask import render_template, abort
from werkzeug.utils import secure_filename

from diaphragm.board import db, Post, PostForm, Thread, ThreadForm
from diaphragm.gallery import Gallery, create_thumbnails, save
from diaphragm.utils import render_ajax, json_dict

app = Flask(__name__, static_folder="static")
app.config.from_object('diaphragm.config.DebugConfig')

db.app = app
db.init_app(app)

gallery = Gallery(app.static_folder, app.config["GALLERY_FOLDER"])
thumbnails = create_thumbnails(gallery.list_static(),
                               app.static_folder, app.config["THUMBNAILS_FOLDER"])

app.uploads_folder = path.join(app.static_folder, app.config["UPLOADS_FOLDER"])
app.thumbnails_folder = path.join(app.static_folder, app.config["THUMBNAILS_FOLDER"])


@app.route("/")
@app.route("/<address>")
@app.route("/gallery/<address>")
@app.route("/board/thread/<address>")
def root(address=None):
    return render_template("layout.html")


@app.route("/api/")
def welcome():
    return render_ajax("welcome.html")


@app.route("/api/about")
def about():
    return render_ajax("about.html")


@app.route("/api/gallery")
def show_gallery():
    pictures = thumbnails.list()
    return render_ajax("gallery.html", full_size=None, pictures=pictures)


@app.route("/api/gallery/<filename>")
def get_image(filename):
    file_send = gallery.get(filename)

    if not file_send:
        abort(404)

    pictures = thumbnails.list()
    return render_ajax("gallery.html", full_size=file_send, pictures=pictures)


@app.route("/api/start_thread", methods=["POST"])
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


@app.route("/api/post_message", methods=["POST"])
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
        filename = secure_filename(form.fileupload.data.filename)
        attachment_name = save(app.uploads_folder, app.thumbnails_folder,
                               filename, form.fileupload.data)
        return Post(thread, form.message.data, form.author.data,
                    attachment_name)


@app.route("/api/board")
def board():
    threads = Thread.query.all()
    threads = [(t, t.op(), t.last(3)) for t in threads]
    form = ThreadForm()
    return render_ajax("board.html", threads=threads, form=form,
                       uploads=app.config['UPLOADS_FOLDER'],
                       thumbnails=app.config['THUMBNAILS_FOLDER'])


@app.route("/api/board/thread/<thread_id>")
def thread(thread_id):
    thread = Thread.query.filter(Thread.id == thread_id).first()

    if not thread:
        abort(404)

    op = thread.op()
    form = PostForm(thread=thread.id)
    posts = thread.posts.filter(Post.id != op.id)
    return render_ajax("thread.html", op=op, thread=thread,
                       posts=posts, form=form,
                       uploads=app.config['UPLOADS_FOLDER'],
                       thumbnails=app.config['THUMBNAILS_FOLDER'])


@app.route("/api/blog")
def blog():
    return render_ajax("coming_soon.html")


@app.route("/api/projects")
def projects():
    return render_ajax("projects.html")
