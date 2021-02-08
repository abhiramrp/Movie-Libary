import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

db = SQL("sqlite:///imdb.db")


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():

    if not session.get("user_id"):
        return render_template("home.html")
        
    userid = session["user_id"]

    userMovieList = db.execute("SELECT movielist FROM users WHERE userid = (?)", userid)[0]['movielist']
    username = db.execute("SELECT username FROM users WHERE userid = (?)", userid)[0]['username']
    
    print("asfas.  ", type(userMovieList))
    
    if userMovieList == None or len(userMovieList) == 0:
        return render_template("noreturnsindex.html", username = username)
        
    
    moviesids = userMovieList.split()
    
    htmltitles = []
        
    for i in range(len(moviesids)):
        moviesids[i] = int(moviesids[i])
        
        mtitle = db.execute("SELECT DISTINCT title FROM movies WHERE id = (?)", moviesids[i])
            
        if mtitle == None:
            continue
            
        mtitle = db.execute("SELECT DISTINCT title FROM movies WHERE id = (?)", moviesids[i])[0]['title']
        myear = db.execute("SELECT DISTINCT year FROM movies WHERE id = (?)", moviesids[i])[0]['year']

        htmltitles.append([mtitle, myear])
        
 
    return render_template("index.html", htmltitles=htmltitles, username = username)


@app.route("/bio")
def bio():
    return render_template("bio.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()


    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        rpassword = request.form.get("rpassword")

        
        if not username:
            message = "No username."
            return render_template("error.html", message = message)
            
        userList = db.execute("SELECT username FROM users WHERE username = (?)", username)
        
        if len(userList) != 0:
            message = "Username already taken. Choose another."
            return render_template("error.html", message = message)
        
        if ' ' in username:
            message = "Username cannot have spaces."
            return render_template("error.html", message = message)
            
        if ' ' in password:
            message = "Password cannot have spaces."
            return render_template("error.html", message = message)
    
        if not password:
            message = "No password."
            return render_template("error.html", message = message)
            
        if password != rpassword:
            message = "Passwords do not match."
            return render_template("error.html", message = message)
        
        
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(request.form.get("password")))
        
        session["user_id"] = db.execute("SELECT userid FROM users WHERE username = (?)", username)[0]['userid']


        return redirect("/")

    else:
        return render_template("register.html")
        
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if not session.get("user_id"):
        message = "Login required to access webpage"
        return render_template("error.html", message = message)
        
    userid = session["user_id"]
    
    if request.method == "POST":
        entry = request.form.get("entry")
        
        isEntry = db.execute("SELECT DISTINCT title FROM movies WHERE UPPER(title) LIKE UPPER(?)", entry)

        
        if len(isEntry) == 0:
            message = "Entry not found"
            return render_template("error.html", message = message)
            
        dbEntry = db.execute("SELECT DISTINCT title FROM movies WHERE UPPER(title) LIKE UPPER(?)", entry)[0]['title']
        
        isAvail = db.execute("SELECT DISTINCT title FROM movies WHERE isChecked = (?) AND title = (?)", 0, dbEntry)
        
        if len(isAvail) == 0:
            message = "Entry not available right now. Please wait for a while"
            return render_template("error.html", message = message)
        
        movieId = db.execute("SELECT id FROM movies WHERE title = (?)", dbEntry)[0]['id']
        
    
        
        userMovieList = db.execute("SELECT movielist FROM users WHERE userid = (?)", userid)[0]['movielist']
        
        
        if userMovieList == None:
            userMovieList = ""
        
        userMovieList = userMovieList + " " + str(movieId)
        
        db.execute("UPDATE movies SET isChecked = (?) WHERE id = (?)", 1, movieId)
        db.execute("UPDATE users  SET movielist = (?) WHERE userid = (?)", userMovieList, userid)
        

        return redirect("/")
 
        
    else:
        
        return render_template("checkout.html")
        

@app.route("/returns", methods=["GET", "POST"])
def returns():
    if not session.get("user_id"):
        message = "Login required to access webpage"
        return render_template("error.html", message = message)
        
    userid = session["user_id"]

    userMovieList = db.execute("SELECT movielist FROM users WHERE userid = (?)", userid)[0]['movielist']
    
    if userMovieList == None:
        return render_template("noreturns.html")
        
    
    moviesids = userMovieList.split()
    

    htmltitles = []
    
    
        
    for i in range(len(moviesids)):
        moviesids[i] = int(moviesids[i])
        
        mtitle = db.execute("SELECT DISTINCT title FROM movies WHERE id = (?)", moviesids[i])
            
        if mtitle == None:
            continue
            
        mtitle = db.execute("SELECT DISTINCT title FROM movies WHERE id = (?)", moviesids[i])[0]['title']
        myear = db.execute("SELECT DISTINCT year FROM movies WHERE id = (?)", moviesids[i])[0]['year']

        htmltitles.append([mtitle, myear])
        
    moviesnumber = len(htmltitles)
        
    
    if request.method == "POST":
        userreturns = request.form.getlist('movietitles')
        
        if len(userreturns) == 0:
            return redirect("/")
        
        returnnumber = moviesnumber
            
        for utitle in userreturns:
 
            utitleid = db.execute("SELECT DISTINCT id FROM movies WHERE UPPER(title) LIKE UPPER(?)", utitle)[0]['id']
            
            db.execute("UPDATE movies SET isChecked = (?) WHERE id = (?)", 0, utitleid)
            
            returnnumber -= 1
            
            userMovieList = userMovieList.replace(str(utitleid), ' ')
            
            
        if returnnumber <= 0:
            userMovieList = None
            
        db.execute("UPDATE users  SET movielist = (?) WHERE userid = (?)", userMovieList, userid)


        return redirect("/")
 
        
    else:
        
        return render_template("returns.html", htmltitles=htmltitles)
    
        
 
 
@app.route("/login", methods=["GET", "POST"])
def login():
    
    session.clear()
    
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")
        
                
        if not username:
            message = "Enter username."
            return render_template("error.html", message = message)
        
        if not password:
            message = "Enter password."
            return render_template("error.html", message = message)

            
        rows = db.execute("SELECT * FROM users WHERE username = (?)", username)
        
        if len(rows) == 0:
            message = "User not in database."
            return render_template("error.html", message = message)
            
        checkPassword = check_password_hash(rows[0]['hash'], password)
        
        if checkPassword == False:
            message = "Incorrect Password"
            return render_template("error.html", message = message)
            

        session["user_id"] = db.execute("SELECT userid FROM users WHERE username = (?)", username)[0]['userid']
            

        return redirect("/")
        
        
    else:
        return render_template("login.html")
        

@app.route("/logout")
def logout():
    session["user_id"] = None
    session.clear()
    return redirect("/")    
