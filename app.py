from flask import Flask, g, render_template, flash, redirect, url_for, request
from forms import EntryForm
from peewee import *

import models
import datetime

app = Flask(__name__)
app.secret_key = "laskhjsdoh8w293y82r98hf239h*^^V;"


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response


@app.route("/", methods=("GET", "POST"))
def index():
    entries = models.Entry.select()
    return render_template("index.html", entries=entries)


@app.route("/entries", methods=("GET", "POST"))
def entries():
    return index()


@app.route("/entries/new", methods=("GET", "POST"))
def new():
    if request.method == "POST":
        models.Entry.create(
            title=request.form["title"],
            date= datetime.datetime.strptime(request.form["date"], "%Y-%m-%d"),
            time_spent=request.form["timeSpent"],
            learned=request.form["whatILearned"],
            resources=request.form["ResourcesToRemember"]
            )
        return redirect(url_for("index"))
    return render_template("new.html")
        
    
@app.route("/entries/<int:id_num>", methods=("GET", "POST"))
def details(id_num):
    entry = models.Entry.select().where(models.Entry.id == id_num).get()
    return render_template("detail.html", entry=entry)


@app.route("/entries/<int:id_num>/edit", methods=("GET", "POST"))
def edit(id_num):
    entry = models.Entry.select().where(models.Entry.id == id_num).get()
    if request.method == "POST":
        if request.form["title"]:
            entry.title = request.form["title"]
        if request.form["date"]:
            entry.date = datetime.datetime.strptime(request.form["date"], "%Y-%m-%d")
        if request.form["timeSpent"]:
            entry.time_spent=request.form["timeSpent"]
        if request.form["whatILearned"]:
            entry.learned = request.form["whatILearned"]
        if request.form["ResourcesToRemember"]:
            entry.resources = request.form["ResourcesToRemember"]
        entry.save()
        return redirect(url_for("index"))
    return render_template("edit.html", entry=entry)
    

@app.route("/entries/<id>/delete", methods=("GET", "POST"))
def delete():
    pass



if __name__ == "__main__":
    models.initialize()
    try:
        models.Entry.create(
            title = "My first",
            date = datetime.datetime.now().date(),
            time_spent = 900,
            learned = ("Learned more about how to use flask"
                       "and python to create web apps."),
            resources = "Alot."
            )
    except models.IntegrityError:
        pass
    
    app.run(debug=True)
    
