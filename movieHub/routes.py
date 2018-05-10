from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from login import loginUser
import sqlite3
from server import app
from sqlite3 import Error
from imdb import IMDb
from dbFunctions import movieQuery, playsQuery, cinemaQuery, timeQuery, showtimesQuery

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        imdb_id = request.form["id"]
        return redirect(url_for('movie', id=imdb_id))
    ia = IMDb()
    movies = movieQuery(None)
    return render_template("index.html", movies=movies)


@app.route('/movie', methods=["GET" , "POST"])
def movie():
    ia = IMDb()
    imdb_id = request.args.get("id")
    
    movie = ia.get_movie(imdb_id)
    ia.update(movie)
    
    cinema_ids = playsQuery(imdb_id)
    cinemaList = []
    timesObj = []
    for i in cinema_ids:
        cinemaList.append(cinemaQuery(i.cinema_id))
        timesObj.append(timeQuery(i.cinema_id, imdb_id))

    times = []
    for obj in timesObj:
        for i in obj:
            times.append(showtimesQuery(i.showtime_id))

    return render_template("movie.html", movie=movie, cinemas=cinemaList, times=times)


@app.route('/login', methods=["GET" , "POST"])
def login():
    if request.method == "POST":
        username = str(request.form["username"])
        password = str(request.form["password"])

        if loginUser(username, password):
            return redirect(url_for("index"))

    return render_template("login.html")

@app.route('/payment', methods=["GET", "POST"])
def payment():
    if request.method == "POST":
        child_select = request.form["child"]
        student_select = request.form["student"]
        adult_select = request.form["adult"]
        pensioner_select = request.form["pensioner"]
        card_name = request.form["name"]
        card_number = request.form["number"]
        expiry_date = request.form["expiry_date"]
        ccv = request.form["CCV"]
        return redirect(url_for("payment_successful"))
    return render_template("payment.html")

@app.route('/payment_successful')
def payment_successful():
    return render_template("payment_successful.html")