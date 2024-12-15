from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, request, session
from .forms import PostForm
from .utils import load_posts, save_post, get_post

from .models import Post
from app import db


@post_bp.route('/add_post', methods=["GET", "POST"]) 
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        category = form.category.data
        is_active = form.is_active.data
        publish_date = form.publish_date.data
        new_post = Post(title=title, content=content, category=category, is_active=is_active, posted=publish_date)
        db.session.add(new_post)
        db.session.commit()
        flash(f"Post {title} added successfully!", "success")
        return redirect(url_for(".get_posts"))
    elif request.method == "POST":
        flash(f"Enter the correct data in the form!", "danger")
    return render_template("add_post.html", form=form)


@post_bp.route('/') 
def get_posts():
    stmt = db.select(Post).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>') 
def detail_post(id):
    post = db.get_or_404(Post, id)
    if not post:
        return abort(404)
    return render_template("detail_post.html", post=post)