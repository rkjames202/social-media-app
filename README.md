# Social Website
- A small webapp using Flask, JavaScript and SQLite that allows the user to make, like/dislike posts, and look at other user profiles.
- Video Demo: https://www.youtube.com/watch?v=EFh4Wah0V30&ab_channel=RussellJames

## Description
#
To begin with, I'll give you a brief overview of the source code...
 - The `static` folder contains two files,  `app.js` and `styles.css`
    - `app.js`, contains the javascript used in the search bar `layout.html` and the button    groups in `profile.html` and `visit_profile.html`. The functions in this file include...
        - `changeSearchType`, gets user selected option next search bar in `layout.html` and changes the placeholder to either "Search Posts" or "Search Users" depending on the options posts and users.
        - An event listener function used for the button group in `profile.html` and `vist_profile.html` displaying either the profiles' personal information, liked/disliked posts, or posts made by the user.
    - `style.css`, contains the CSS file that will be used in all the HTML documents.
 - The `templates` folder contains all of the HTML documents used in the project containing...
    - `index.html`, the websites homepage that displays all posts and includes a sort option.
    - `layout.html`, layout of the webpage.
    - `login.html`, where user logs in.
    - `post_search.html`, displays search results for posts.
    - `profile.html`, user's profile page. User can view their personal information with the    option of updating it. As well as view their like/disliked posts and posts made by them.
    - `register.html`, where user makes an account.
    - `user_search.html`, displays search results for users.
    - `visit_profile.html`, similar to `profile.html` but you cannot update another user's personal information.

- Files in the project's main directory include...
    - `app.py`, all of the source code utilizing Python's Flask, CS50's version of SQLite, werkzeug for generating password hashes along with other libraries. The functions in the file include...
        - `index()`, grabs all data of posts from `social.db` which will be displayed in `index.html`.
        - `sort()`, grabs data depending on sort option user selects and grabs data from `social.db`, sorts accordingly and displays posts on `index.html`.
        - `login()`, grabs username and password from form in `login.html` and checks for both in `social.db`.
        - `logout()`, logs user out and returns them back to `login.html`.
        - `register()`, grabs all data from registration form in `register.html` and performs validation on username and password. If both are valid, new user is created in `social.db`.
        - `post()`, adds post to `social.db` and displays it on `index.html`.
        - `delete_post()`, deletes post from `social.db`.
        - `like()`, adds or removes likes from a post and updates the posts that a user has liked in `social.db`.
        - `dislike()`, adds or removes dislikes from a post and update the posts that a user has disliked in `social.db`.
        - `profile()`, grabs all information associated with user and displays it on `profile.html` via a button group. Includes, personal information, liked/disliked posts, and posts made by the user.
        - `update_profile()`, updates user profile via `profile.html` grabs all information enterered by user (using "N/A" placeholder if any input field is empty). User can also change their username if the new username is unqiue.
        - `search()`, performs a search on either the user or posts in `social.db` using the search query provided by the user
        - `visit_profile()`, grabs all information for the profile that the user is visiting. Grabs all information that `profile()` gets but of course, does not allow user to change any information.

    - `helper.py`, contains two helper functions...
        - `login_required()`, prevents user from accessing any webpage that requires them to be logged in (if they aren't already of course).
        - `format_timestamp()`, formats all of the timestamps of posts provided by SQLite.
    - `requirements.txt`, the libraries used accross all Python files in the project.

    - `social.db`, SQLite database file containing the tables...
        - `likes`, records the posts each user likes using post id and user id.
        - `dislikes`, records the posts each user dislikes using post id and user id.
        - `personal_info`, holds the users' personal information. Including their first/last name, favorite color, favorite food, and their bio. References `username` in `users`.
        - `posts`, records all of the posts made by users and information about each one. Contains the timestamp, post id, user id, contents of post, and amount likes/dislikes for the post. Primary key is the post id and references `id` in `users`.
        - `users`, records the username and password hash for each user. Primary key is the user id and there is a unique index on usernames, allowing each user to have unique username.

## Additional Information
#
When making this project there were a couple of features I had in mind but I ultimately  decided to do without.
1. Following other users, which would give the user the ability to perform a sort only seeing posts of the user along with recieving an alert of some kind if a user they followed made a post
2. Implementing a news API, having the user select from a list of interests and displaying any news that pertained to the user's selected interests.

 At first I told myself I would implement these two features after the application was in the state that it's currently in. But, I decided to do without these two features because I believed that an application of this scale probably wouldn't need this. The news API just didn't fit into what I had in mind and following other users didn't seem necessary since they are so little users you could just do a search or visit a user's profile to see any posts made by them.
