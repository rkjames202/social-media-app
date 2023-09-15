from cs50 import SQL
import re
from flask import Flask, flash, render_template, redirect, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, format_timestamp

#Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded (dont have to kee re running server)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Configure's CS50's library so SQLite can be used
db = SQL("sqlite:///social.db")


@app.route("/")
@login_required
def index():
    #Gets all of the posts in database sorted by time posted
    posts = db.execute("SELECT timestamp, username, post_text, post_id, user_id, likes, dislikes FROM users JOIN posts ON users.id = posts.user_id ORDER BY timestamp DESC")
    #Stores the dates of all of the posts
    post_dates = format_timestamp(posts)
    #Gets user id
    user_id = session["user_id"]
    return render_template("index.html", posts=posts, post_dates=post_dates, user_id=user_id)

#Sorts posts on homepage
@app.route("/sort")
@login_required
def sort():
    #Get the sort type selected
    sort_type = request.args.get("sort_type")
    #Get id of logged in user
    user_id = session["user_id"]

    #Sorts posts by most recent
    if sort_type == "recent":
        posts = db.execute("SELECT timestamp, username, post_text, post_id, user_id, likes, dislikes FROM posts JOIN users ON users.id = posts.user_id ORDER BY timestamp DESC")
        post_dates = format_timestamp(posts)
        return render_template("index.html", posts=posts, post_dates=post_dates, user_id=user_id)

    #Sorts posts by amount of likes
    if sort_type == "likes":
        posts = db.execute("SELECT timestamp, username, post_text, post_id, user_id, likes, dislikes FROM posts JOIN users ON users.id = posts.user_id ORDER BY likes DESC")
        post_dates = format_timestamp(posts)
        return render_template("index.html", posts=posts, post_dates=post_dates, user_id=user_id)

    #Sorts posts by amount of dislikes
    if sort_type ==  "dislikes":
        posts = db.execute("SELECT timestamp, username, post_text, post_id, user_id, likes, dislikes FROM posts JOIN users ON users.id = posts.user_id ORDER BY dislikes DESC")
        post_dates = format_timestamp(posts)
        return render_template("index.html", posts=posts, post_dates=post_dates, user_id=user_id)
    return redirect("/")

@app.route("/login", methods=["POST", "GET"])
def login():

    #Log out user if logged in
    session.clear()

    if request.method == "POST":

        #Get user input from form
        username = request.form.get("username")
        password = request.form.get("password")

        #Checks if username or password are empty
        if not username or not password:
            flash("Please enter username and password")
            render_template("login.html")

        #Query database for username
        name_check = db.execute("SELECT * FROM users WHERE username = ?", username)

        #If username is not found in database or if password does is incorrect
        if len(name_check) != 1 or not check_password_hash(name_check[0]["hash"], password):
            flash("Invalid username or password")
            return render_template("login.html")

        #Remember user currently logged in
        session["user_id"] = name_check[0]["id"]

        #Let user know they're logged in
        flash("Login successful.")
        return redirect("/")

    else:

        #Default GET route
        return render_template("login.html")

@app.route("/logout")
def logout():

    #Log out user
    session.clear()

    #Let user know they are logged out, return to homepage
    flash("Logged out.")
    return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():

    #Log out user if logged in
    session.clear()

    if request.method == "POST":

        #Get information user enterd in form
        username = request.form.get("username").strip()
        password = request.form.get("password")
        pass_confirm = request.form.get("confirmation")

        pass_num = sum(char.isdigit() for char in password)
        valid_pass = True

        #Checking if username field is empty
        if not username or not password:
            flash("Must provide username and password")
            return render_template("register.html")

        #Checking if username is at least 5 characters long
        if len(username) < 5:
            flash("Username must be at least 5 characters long")
            return render_template("register.html")

        #Checking if password is at least 8 characters long
        if len(password) < 8:
            flash("Password must be at least 8 characters long")
            return render_template("register.html")

        #Checking if password contains any special characters and has at least 5 numbers
        if re.findall('[^A-Za-z0-9]', password) and (pass_num >= 5):
            valid_pass = True
        else:
            valid_pass = False

        #If pass is invalid
        if valid_pass == False:
            flash("Password must include at least 5 numbers and 1 special character")
            return render_template("register.html")

        #If password does not match password confirmation
        if password != pass_confirm:
            flash("Passwords must match")
            return render_template("register.html")

        #Gets all personal information from registration form
        first_name = request.form.get("first_name").strip()
        last_name = request.form.get("last_name").strip()
        fav_color = request.form.get("fav_color").strip()
        fav_food = request.form.get("fav_food").strip()
        bio = request.form.get("bio").strip()

        #Add user to db if username does not already exist
        try:
            #Generates password
            hash = generate_password_hash(request.form.get("password"))
            #Adds username and password hash to database
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            #Adds personal information of user to database
            db.execute("INSERT INTO personal_info (username, first_name, last_name, favorite_color, favorite_food, bio) VALUES (?, ?, ?, ?, ?, ?)", username, first_name, last_name, fav_color, fav_food, bio)

            #Lets user know that registration was successful
            flash("Registeration successful.")
            return render_template("login.html")

        except:

            #Lets user know that username exists
            flash("Username already exists.")
            return render_template("register.html")


    else:
            #Default GET route
            return render_template("register.html")

@app.route("/post", methods=["POST", "GET"])
@login_required
def post():


    if request.method == "POST":

        #Checks if post form is empty
        if not request.form.get("post_text"):
            flash("Can't submit empty post, don't be shy!")
            return redirect("/")

        #Gets post text
        post_text = request.form.get("post_text")

        #Inserts post into db
        db.execute("INSERT INTO posts (user_id, post_text) VALUES (?, ?)", session["user_id"], post_text)

        #Lets user know post was successful
        flash("Post added")
        return redirect("/")

@app.route("/delete_post", methods=["POST", "GET"])
@login_required
def delete_post():

    if request.method == "POST":
        #Gets post id
        post_id = request.form.get("post_id")

        #Deletes post from database
        db.execute("DELETE FROM posts WHERE post_id = ?", post_id)

        #Lets user know that post was deleted
        flash("Post deleted")
        return redirect(request.referrer)


@app.route("/like", methods=["POST", "GET"])
@login_required
def like():

    if request.method == "POST":

        #Gets post id from like button form
        post_id = request.form.get("like_button")

        #Will execute as long as user has not already liked post
        try:
            #Checks if user already disliked post, if so decrement dislikes of post by 1 and remove from user's disliked posts
            if db.execute("SELECT user_id, post_id FROM dislikes WHERE user_id = ? AND post_id = ?", session["user_id"], post_id):
                db.execute("DELETE FROM dislikes WHERE user_id = ? AND post_id = ?", session["user_id"], post_id)
                db.execute("UPDATE posts SET dislikes = dislikes - 1 WHERE post_id = ?", post_id)

            #Adds posts to user's liked posts and increments likes of post by 1
            db.execute("INSERT INTO likes (user_id, post_id) VALUES (?, ?)", session["user_id"], int(post_id))
            db.execute("UPDATE posts SET likes = likes + 1 WHERE post_id = ?", post_id)

        #If user already liked post...
        except:

            #Remove like from post and remove from user's liked posts
            db.execute("DELETE FROM likes WHERE user_id = ? AND post_id = ?", session["user_id"], post_id)
            db.execute("UPDATE posts SET likes = likes - 1 WHERE post_id = ?", post_id)

            #Lets user know they removed their like
            flash("Like removed from post")

            #Returns to the page the form was called from
            return redirect(request.referrer)

        #Lets user know post was liked successfully
        flash("Post liked")
        return redirect(request.referrer)

@app.route("/dislike", methods=["POST", "GET"])
@login_required
def dislike():
#The following function will perform the same operations as like() but with dislikes instead
    if request.method == "POST":

        #Gets post id
        post_id = request.form.get("dislike_button")


        #Will execute as long as user has not already disiked post
        try:

            #Checks if user already liked post, if so decrement likes of post by 1 and remove from user's liked posts
            if db.execute("SELECT user_id, post_id FROM likes WHERE user_id = ? AND post_id = ?", session["user_id"], post_id):
                db.execute("DELETE FROM likes WHERE user_id = ? AND post_id = ?", session["user_id"], post_id)
                db.execute("UPDATE posts SET likes = likes - 1 WHERE post_id = ?", post_id)

            #Adds posts to user's disliked posts and increments dislikes of post by 1
            db.execute("INSERT INTO dislikes (user_id, post_id) VALUES (?, ?)", session["user_id"], int(post_id))
            db.execute("UPDATE posts SET dislikes = dislikes + 1 WHERE post_id = ?", post_id)

        #If user alread disliked post...
        except:

            #Remove dislike from post and remove from user's disliked posts
            db.execute("DELETE FROM dislikes WHERE user_id = ? AND post_id = ?", session["user_id"], post_id)
            db.execute("UPDATE posts SET dislikes = dislikes - 1 WHERE post_id = ?", post_id)

            #Lets user know that post was disliked
            flash("Dislike removed from post")
            return redirect(request.referrer)

        #Lets user know that post was disliked
        flash("Post disliked")
        return redirect(request.referrer)

@app.route("/profile")
@login_required
def profile():
    #Get all of the user personal information, liked posts, disliked posts, and posts by user
    user_info = db.execute("SELECT * FROM personal_info JOIN users ON personal_info.username = users.username WHERE id = ?", session["user_id"])[0]
    liked_posts = db.execute("SELECT timestamp, username, post_id, user_id, post_text, likes, dislikes FROM posts JOIN users ON users.id = posts.user_id WHERE post_id IN (SELECT post_id FROM likes WHERE user_id = ?)", session["user_id"])
    disliked_posts = db.execute("SELECT timestamp, username, post_id, user_id, post_text, likes, dislikes FROM posts JOIN users ON users.id = posts.user_id WHERE post_id IN (SELECT post_id FROM dislikes WHERE user_id = ?)", session["user_id"])
    user_posts = db.execute("SELECT timestamp, username, post_id, user_id, post_text, likes, dislikes FROM posts JOIN users ON users.id = posts.user_id WHERE user_id = ?", session["user_id"])

    #Gets dates of all posts associated with user
    liked_dates = format_timestamp(liked_posts)
    disliked_dates = format_timestamp(disliked_posts)
    post_dates = format_timestamp(user_posts)

    user_id = session["user_id"]

    #Sends data to profile.html
    return render_template("profile.html", user_info=user_info, liked_posts=liked_posts, disliked_posts=disliked_posts,
                            user_posts=user_posts, liked_dates=liked_dates, disliked_dates=disliked_dates, post_dates=post_dates, user_id=user_id)


@app.route("/update_profile", methods=["GET", "POST"])
@login_required
def update_profile():

    if request.method == "POST":

        #Gets all of the user information, stripping off any trailing or leading whitespaces
        username = request.form.get("username").strip()
        first_name = request.form.get("first_name").strip()
        last_name = request.form.get("last_name").strip()
        fav_color = request.form.get("fav_color").strip()
        fav_food = request.form.get("fav_food").strip()
        bio = request.form.get("bio").strip()

        #Checks if username is at least 5 characters long
        if len(username) < 5:
            flash("Username must be at least 5 characters long")
            return redirect("profile")

        #If any optional information is empty, insert 'N/A' as placeholder
        if not first_name:
            first_name = "N/A"
        if not last_name:
            last_name = "N/A"
        if not fav_color:
            fav_color = "N/A"
        if not fav_food:
            fav_food = "N/A"
        if not bio:
            bio = "N/A"

        #Checks if user has given unique username
        try:
            db.execute("UPDATE users SET username = ? WHERE id = ?", username, session["user_id"])

        except:
            #Let's user know that username already exits
            flash("Username already exists.")
            return redirect("/profile")

        #Adds updated personal info to db
        db.execute("UPDATE personal_info SET username = ?, first_name = ?, last_name = ?, favorite_color = ?, favorite_food = ?, bio = ? WHERE username = (SELECT username FROM users WHERE id = ?)", username, first_name, last_name, fav_color, fav_food, bio, session["user_id"])

        #Lets user know that profile update was successful
        flash("Profile Updated")
        return redirect("/profile")

@app.route("/search")
def search():

    #Gets search type from select form
    search_type = request.args.get("search_type")
    #Gets user inputted search query
    search_bar =  request.args.get("search_bar").strip()

    #Checks if search bar is empty
    if not search_bar:
        flash("No search query given")
        return redirect(request.referrer)

    #Searches all posts that contain keyword(s) given by user
    if search_type == "posts":
        results = db.execute("SELECT timestamp, username, post_text, post_id, user_id, likes, dislikes FROM users JOIN posts ON users.id = posts.user_id WHERE post_text LIKE ? ORDER BY timestamp DESC", "%" + search_bar + "%")
        dates = format_timestamp(results)
        user_id = session["user_id"]
        return render_template("post_search.html", results=results, dates=dates, user_id=user_id)
    #Searches all username that contain keyword(s) given by user
    elif search_type == "users":
        results = db.execute("SELECT * FROM personal_info WHERE username LIKE ? ORDER BY username DESC", "%" + search_bar + "%")
        return render_template("user_search.html", results=results,)

@app.route("/visit_profile")
def visit_profile():

    #Get the username of the profile being visited
    username = request.args.get("username")
    #Lookup user id of profile
    user_id = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]

    #If user is visiting their own profile
    if user_id == session["user_id"]:
        return redirect ("/profile")

    #Gets user info, liked post, disliked posts, and posts made by user
    user_info = db.execute("SELECT * FROM personal_info WHERE username = ?", username)[0]
    liked_posts = liked_posts = db.execute("SELECT timestamp, username, post_id, user_id, post_text, likes, dislikes FROM posts JOIN users ON users.id = posts.user_id WHERE post_id IN (SELECT post_id FROM likes WHERE user_id = ?)", user_id)
    disliked_posts = db.execute("SELECT timestamp, username, post_id, user_id, post_text, likes, dislikes FROM posts JOIN users ON users.id = posts.user_id WHERE post_id IN (SELECT post_id FROM dislikes WHERE user_id = ?)", user_id)
    user_posts = db.execute("SELECT timestamp, username, post_id, user_id, post_text, likes, dislikes FROM posts JOIN users ON users.id = posts.user_id WHERE user_id = ?", user_id)

    #Gets dates of all the posts
    liked_dates = format_timestamp(liked_posts)
    disliked_dates = format_timestamp(disliked_posts)
    post_dates = format_timestamp(user_posts)

    #Gets user id of user currently logged in
    logged_in_user = session["user_id"]

    #Send all data to visit_profile.html
    return render_template("visit_profile.html", user_info=user_info, liked_posts=liked_posts, disliked_posts=disliked_posts,
                            user_posts=user_posts, liked_dates=liked_dates, disliked_dates=disliked_dates, post_dates=post_dates, logged_in_user=logged_in_user)



