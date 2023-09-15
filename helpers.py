from datetime import datetime
from flask import redirect, session
from functools import wraps


#Function will be used for pages that require a login
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

#Used to format timepstamps of posts
def format_timestamp(posts):
    #Will store post id's with thier appropiate dates
    dates = {}

    #Loops through each time stamp in post dictionary
    for post in posts:
        #Gets the year, month, date and time in hours, minutes and seconds
        timestamp = datetime.strptime(post["timestamp"],'%Y-%m-%d %H:%M:%S')
        #Converts the timestamp into weekday, month, day of month, and time into 12 hour format
        dates[post["post_id"]] = timestamp.strftime("%a, %B %d, %Y %I:%M %p")

    return dates