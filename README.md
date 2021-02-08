# iMDb Movie Library
#### Video Demo:  [https://www.youtube.com/watch?v=ukMxIYb31A0](https://www.youtube.com/watch?v=ukMxIYb31A0).
#### Description: This application allows users to checkout movies and other diigital content of iMDb.

[imdb.db](imdb.db)
This database has two tables - `users` and `movies`. `users` include a primary integer key of `userid`, a text of `username`, and hash text password of `hash`. The hash is used for safety and confidentiality of passwords.
`movies` include a primary integer key of `id` for each content, a text of `title`, a numeric of `year`, and a boolean of `isChecked` to see if the movie is available for checkout or if someone else checked out.

[static](static)
The css file in static is taken and referred from pset 8 finances assignment from 2020.

[templates](templates)
- [layout.html](templates/layout.html)
    Most of the document is taken and referred from pset 8 finances assignment from 2020. The `checkout` and `returns` buttons in the menu are used for the circulation of iMDb content. The  `login`, `register`, and `logout` are used for users' accounts. I have posted links to my bio and iMDb website in the footer.
- [homepage.html](templates/homepage.html)
    This webpage is the homepage and it displays an intro of the website and project. Users without an account can access this webpage. Users with account will be directed to [index.html](templates/index.html)
- [index.html](templates/index.html)
	This webpage is home to users. After a big heading of welcoming users with their username, there is a table that displays the user’s account and content they have checked out and the year it was released. Users with an empty checked out list will be directed to [noreturnsindex.html](templates/noreturnsindex.html).
- [noreturnsindex.html](templates/noreturnsindex.html)
	This webpage is very similar to `index.html` but instead of a table, it asks them to visit `\checkout` to checkout content.
- [register.html](templates/register.html)
	This webpage allows people to register. It uses a `post` method in the form and it asks users to enter username and password two times. Failure to do so, different repeated password, and existing username entries will be directed to [error.html](templates/error.html). If registration is successful, users will be logged in and directed to [index.html](templates/index.html) or [noreturnsindex.html](templates/noreturnsindex.html)
- [login.html](templates/login.html)
	This webpage allows users to login. It uses a `post` method in the form and it asks users to enter username and password. Failure to do so, different repeated password, and existing username entries will be directed to [error.html](templates/error.html). If login is successful, they will be logged in and directed to [index.html](templates/index.html) or [noreturnsindex.html](templates/noreturnsindex.html)
- [bio.html](templates/bio.html)
	This webpage has a bio of me, including my education, location, and access to my Github portfolio and LinkedIn.
- [checkout.html](templates/checkout.html)
	This webpage allows users to checkout content. There is a search bar in the form section. Users can enter anything they are looking for. If it is available, it will be checked out and redirected back to [index.html](templates/index.html). If not, then users will be directed to [error.html](templates/error.html).
- [returns.html](templates/returns.html)
	This webpage allows users to return their content. Using a checkbox input form, users can return the iMDb content. If they didn’t checkout anything, users will be directed to [noreturns.html](templates/noreturns.html).
- [noreturns.html](templates/noreturns.html)
	This webpage is like [returns.html](templates/returns.html) but for users that didn’t checkout anything. It asks users to checkout.
- [error.html](templates/error.html)
	This webpage has a `message`. Any error from forms will be directed to here and it displays the error that happened. It has a button that takes users to the previous page.
- [logout.html](templates/logout.html)
	This webpage allows users to logout. Their session is cleared and they will be sent to [homepage.html](templates/homepage.html).

[application.py](application.py)
- `@app.route("/")`
- `def index():`
	If the user is not logged in, they would be directed to `homepage.html`.
	Using SQL and userid, username and userMovieList are gathered. If userMovieList is empty, they would be directed to `noreturnsindex.html`.
    After that, userMovieList is broken into a list of movie ids which are later used to get movie title and year released. The title and year are paired as a list and appended into htmltitles, which is later passed along with username to `index.html.
- `@app.route("/bio")`
- `def bio():`
	This would direct the user to `bio.html`.
- `@app.route("/register", methods=["GET", "POST"])`
- `def register():`
	This function is used to register users. The session is cleared to avoid confusion. If `request.method == "POST"`, then username, password, and rpassword are collected.
	The inputs are tested if they are empty, have spaces, if username already exists, and if password and repeat of password are different. Failure of this shall be sent to `error.html` with the appropriate message of error explanation.
	Then, using SQL, the new values of username and `generate_password_hash` of password are inserted into the database. Using the new userid, they are now logged in and they are redirected to `@app.route("/")`.
- `@app.route("/checkout", methods=["GET", "POST"])`
- `def checkout():`
	If the user is not logged in, they will be directed to `error.html`.
    If `request.method == "POST"`, then the entry is collected. Ignoring the case, it is then found in the database. Then it is checked whether the title is available for check out. If not found or unavailable, then user will be directed to `error.html`.
    Using SQL, the app will get userMovieList. If the string is NULL, then the id of the movie will be added in the string. Else, the id is added to the string followed by an empty space. Then, the database updates isChecked value to 1 from movies table and movielist value to userMovieList from users table. Finally, the user is directed to `@app.route("/")`.
- `@app.route("/returns", methods=["GET", "POST"])`
- `def returns():`
	If the user is not logged in, they will be directed to `error.html`.
	Using SQL and userid and userMovieList are gathered. If userMovieList is empty, they would be directed to `noreturns.html`.
    After that, userMovieList is broken into a list of movie ids which are later used to get movie title and year released. The title and year are paired as a list and appended into htmltitles, which is later passed along with username to `index.html. Moviesnumber, the length of htmltitles is created.
    If `request.method == "POST"`, then the userreturns is collected as a list. If the list is empty, then the user is redirected to `@app.route("/")`. A new variable, returnnumber is created and set to moviesnumber. In a loop, each title is removed from the userMovieList, the status of each movie is set to 0, and returnnumber is decremented by 1. If return number is less than 1, then userMovieList is set to NULL. At last, userMovieList is updated into the database by SQL. Finally, user is directed to `@app.route("/")`.
- `@app.route("/login", methods=["GET", "POST"])`
- `def login():`
	This function is used to login users. The session is cleared to avoid confusion. If `request.method == "POST"`, then username and password are collected.
	The inputs are tested if they are empty, if username exists, and username and password are corrected. Password is tested by comparing the hash value from database and user input using `check_password_hash` function. Failure of this shall be sent to `error.html` with the appropriate message of error explanation.
	Using the userid from SQL, they are now logged in and they are redirected to `@app.route("/")`.
- `@app.route("/logout")`
- `def logout():`
	This function is used to log out users. The user session is cleared and they are redirected to `@app.route("/")`.




