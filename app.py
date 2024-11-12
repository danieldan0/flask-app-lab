from flask import Flask, request, redirect, url_for, render_template, abort

app = Flask(__name__)
app.config.from_pyfile("config.py")

@app.route('/')
def main():
    return redirect(url_for('about'))  # Redirect to /about

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/education')
def education():
    return render_template("education.html")

@app.route('/skills')
def skills():
    return render_template("skills.html")

@app.route('/projects')
def projects():
    return render_template("projects.html")

if __name__ == "__main__":
    app.run()  # Launch built-in web server and run this Flask webapp, debug=True
 

