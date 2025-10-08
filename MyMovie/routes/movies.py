import datetime
import functools
import uuid

from dataclasses import asdict
from flask import Blueprint, render_template, session, redirect, request, current_app, url_for
from MyMovie.forms import MovieForm, ExtendedMovieForm
from MyMovie.models.models import Movie, User

def login_required(route):
    @functools.wraps(route)
    def wrapper(*args, **kwargs):
        if not session.get("email"):
            return redirect(url_for("auth.Login"))
        
        return route(*args, **kwargs)
    
    return wrapper


Movies = Blueprint("movies", __name__)

@Movies.route("/home")
@login_required
def index():
    if "theme" not in session:
        session["theme"] = "light"

    user_data = current_app.db.users.find_one({"email": session.get("email")})
    user = User(**user_data)

    movies_data = current_app.db.movies.find({"_id": {"$in": user.movies}   })
    movies = [Movie(**movie) for movie in movies_data]


    return render_template("index.html",
                           movies=movies,
                           theme=session["theme"],
                           username=session["email"] if "email" in session else None
                           )

@Movies.get("/movie/<string:_id>")
def movie_details(_id: str):
    if "theme" not in session:
        session["theme"] = "light"
        
    movie_data = current_app.db.movies.find_one({"_id": _id})
    movie = Movie(**movie_data)


    return render_template("movie_details.html", movie=movie, theme=session["theme"], username=session["email"] if "email" in session else None)

@Movies.route("/add", methods=["GET", "POST"])
@login_required
def add_movie():
    if "theme" not in session:
        session["theme"] = "light"
    form = MovieForm()


    if form.validate_on_submit():
        new_movie = Movie(
                    _id=uuid.uuid4().hex,
                    title=form.title.data,
                    director=form.director.data,
                    year=form.year.data
                    )

        current_app.db.movies.insert_one(asdict(new_movie))
        current_app.db.users.update_one({"email": session.get("email")}, {"$push": {"movies": new_movie._id}})

        return redirect(url_for(".index"))

    return render_template(
        "new_movie.html",
        title="Movies | Add Movie",
        theme=session["theme"],
        form=form,
        username=session["email"] if "email" in session else None
    )

@Movies.get("/movie/<string:_id>/rate")
@login_required
def rate_movie(_id: str):
    if "theme" not in session:
        session["theme"] = "light"
    rating = int(request.args.get("rating"))
    current_app.db.movies.update_one({"_id": _id}, {"$set": {"rating": rating}})
    return redirect(url_for(".movie_details", _id=_id))

@Movies.get("/movie/<string:_id>/watch")
@login_required
def watch(_id: str):
    if "theme" not in session:
        session["theme"] = "light"
    current_app.db.movies.update_one({"_id": _id}, {"$set": {"last_watched": datetime.datetime.today()}})
    return redirect(url_for(".movie_details", _id=_id, username=session["email"] if "email" in session else None))

@Movies.route("/edit/<string:_id>", methods=["GET", "POST"])
@login_required
def edit(_id: str):
    if "theme" not in session:
        session["theme"] = "light"
    movie_data = current_app.db.movies.find_one({"_id": _id})
    movie = Movie(**movie_data)
    form = ExtendedMovieForm(obj=movie)

    if form.validate_on_submit():
        movie.title = form.title.data
        movie.director = form.director.data
        movie.year = form.year.data
        movie.description = form.description.data
        movie.tags = form.tags.data
        movie.cast = form.cast.data
        movie.series = form.series.data
        movie.video_link = form.video_link.data

        current_app.db.movies.update_one({"_id": _id}, {"$set": asdict(movie)})

        return redirect(url_for(".movie_details", _id=_id))


    return render_template("edit_movie.html", movie=movie, form=form, theme=session["theme"], username=session["email"] if "email" in session else None)