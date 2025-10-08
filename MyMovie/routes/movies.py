import uuid

from dataclasses import asdict
from flask import Blueprint, render_template, session, redirect, request, current_app, url_for
from MyMovie.forms import MovieForm
from MyMovie.models.models import Movie

Movies = Blueprint("movies", __name__)

@Movies.route("/home")
def index():
    movies_data = current_app.db.movies.find({})
    movies = [Movie(**movie) for movie in movies_data]


    return render_template("index.html",
                           movies=movies,
                           theme=session["theme"]
                           )

@Movies.get("/movie/<string:_id>")
def edit_movie(_id: str):
    movie_data = current_app.db.movies.find_one({"_id": _id})
    movie = Movie(**movie_data)


    return render_template("movie_details.html", movie=movie, theme=session["theme"])

@Movies.route("/add", methods=["GET", "POST"])
def add_movie():
    form = MovieForm()


    if form.validate_on_submit():
        new_movie = Movie(
                    _id=uuid.uuid4().hex,
                    title=form.title.data,
                    director=form.director.data,
                    year=form.year.data
                    )

        current_app.db.movies.insert_one(asdict(new_movie))

        return redirect(url_for(".index"))

    return render_template(
        "new_movie.html",
        title="Movies | Add Movie",
        theme=session["theme"],
        form=form
    )