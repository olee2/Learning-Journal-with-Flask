from flask import (Flask, g, render_template, flash,
                   redirect, url_for, request)
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
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route("/", methods=("GET", "POST"))
def index():
    """The index page lists all entries."""
    entries = models.Entry.select()
    return render_template("index.html", entries=entries)


@app.route("/entries", methods=("GET", "POST"))
def entries():
    """The entries page lists all entries."""
    return index()


@app.route("/entries/new", methods=("GET", "POST"))
def new():
    """
    Allows the user to add new entries to the journal.
    Gets data from html-form and stores it in variables. 
    Date is checked to see that it can be converted into datetime.
    Time spent is checked to see that it is a integer.
    Title is checked to see that it contains characters
    and that it is a unique title.
    Creates an instance of the entry model. 
    """
    if request.method == "POST":
        title = request.form["title"]
        date = request.form["date"]
        time_spent = request.form["timeSpent"]
        learned = request.form["whatILearned"]
        resources = request.form["ResourcesToRemember"]
        
        try:
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
            
        except ValueError:
            flash("Please select a valid date. (dd.mm.yyyy)", "error")
            return render_template("new.html",
                                   date=datetime.datetime.now(),
                                   title=title,
                                   time_spent=time_spent,
                                   learned=learned,
                                   resources=resources)
        
        else:
            try:
                time_spent = int(time_spent)
                
            except ValueError:
                flash("Please fill in time spent as an integer.", "error")
                return render_template("new.html",
                                       date=datetime.datetime.now(),
                                       title=title,
                                       time_spent=time_spent,
                                       learned=learned,
                                       resources=resources
                                       )
            
            else:
                if title.strip():
                    try:
                        models.Entry.create(
                            title=title,
                            date= date,
                            time_spent=time_spent,
                            learned=learned,
                            resources=resources
                            )
                        
                    except models.IntegrityError:
                        flash("Please choose a unique title.")
                        return render_template("new.html",
                                               date=datetime.datetime.now(),
                                               title=title,
                                               time_spent=time_spent,
                                               learned=learned,
                                               resources=resources
                                               )
                    
                else:
                    flash("Please add a title.")
                    return render_template("new.html",
                                           date=date,
                                           title=title,
                                           time_spent=time_spent,
                                           learned=learned,
                                           resources=resources
                                           )
                
            return redirect(url_for("index"))
    return render_template("new.html", date=datetime.datetime.now())


@app.route("/entries/<int:id_num>/edit", methods=("GET", "POST"))
def edit(id_num):
    """
    Allows the user to edit existing entries in the journal.
    Existing data is loaded into the html-form.
    Gets data from the html-form and stores it in variables.
    Date is checked to see that it can be converted into datetime.
    Time spent is checked to see that it is a integer.
    Title is checked to see that it contains characters
    and that it is a unique title.
    Updates the instance of the entry model. 
    """
    entry = models.Entry.select().where(models.Entry.id == id_num).get()
    
    if request.method == "POST":
        title = request.form["title"]
        date = request.form["date"]
        time_spent = request.form["timeSpent"]
        learned = request.form["whatILearned"]
        resources = request.form["ResourcesToRemember"]

        entry.learned = learned
        entry.resources = resources
        
        try:
            entry.date = datetime.datetime.strptime(date, "%Y-%m-%d")
            entry.save()
            
        except ValueError:
            flash("Please select a valid date. (dd.mm.yyyy)", "error")
            return render_template("edit.html", entry=entry)
        
        else:
            try:
                entry.time_spent = int(time_spent)
                entry.save()
                
            except ValueError:
                flash("Please fill in time spent as an integer.", "error")
                return render_template("edit.html", entry=entry)
            
            else:
                if title.strip():
                    try:
                        entry.title = request.form["title"]
                        entry.save()
                        
                    except models.IntegrityError:
                        flash("Please choose a unique title.")
                        return render_template("edit.html", entry=entry)
                    
                    return redirect(url_for("index"))
                
                else:
                    flash("Please add a title.")
                    return render_template("edit.html", entry=entry)

        
    return render_template("edit.html", entry=entry)

@app.route("/entries/<int:id_num>", methods=("GET", "POST"))
def details(id_num):
    """View the entry details."""
    entry = models.Entry.select().where(models.Entry.id == id_num).get()
    return render_template("detail.html", entry=entry)

@app.route("/entries/<int:id_num>/delete", methods=("GET", "POST"))
def delete(id_num):
    """Delete entry."""
    entry = models.Entry.select().where(models.Entry.id == id_num).get()
    entry.delete_instance()
    return redirect(url_for("index"))


if __name__ == "__main__":
    models.initialize()
    try:
        models.Entry.create(
            title = "My first",
            date = datetime.datetime.now().date(),
            time_spent = 90,
            learned = "Test",
            resources = "Test",
            )
        
    except models.IntegrityError:
        pass

    app.run(debug=True)
    
