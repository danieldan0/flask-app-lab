from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, request
from .forms import PostForm
from .utils import load_posts, save_post, get_post

posts = [
    {"id": 1, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe'},
    {"id": 2, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
    {"id": 3, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
] 


@post_bp.route('/add_post', methods=["GET", "POST"]) 
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_post = {"id": len(load_posts()) + 1, 'title': title, 'content': content}
        save_post(new_post)
        flash(f"Post {title} added successfully!", "success")
        return redirect(url_for(".get_posts"))
    elif request.method == "POST":
        flash(f"Enter the correct data in the form!", "danger")
    return render_template("add_post.html", form=form)


@post_bp.route('/') 
def get_posts():
    return render_template("posts.html", posts=load_posts())

@post_bp.route('/<int:id>') 
def detail_post(id):
    post = get_post(id)
    if not post:
        return abort(404)
    return render_template("detail_post.html", post=post)