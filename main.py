from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://movielist:baltoapp@localhost:8889/movielist'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

#class that holds created user

class ListUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    pw_hash = db.Column(db.String(120)) 
    

    def __init__(self, email, password):
        self.email = email
        self.pw_hash = make_pw_hash(password)




#class that wold hold the names of the movies and possibly the plot via the csv file?
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    year = db.Column(db.Boolean)
    

    def __init__(self, name):
        self.name = name
        
    



@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not is_email(email):
            flash(email + '"Not a email address"')
            return redirect('/signup')
        # 'verify' matches password
        # validate that there is no user with that email already
        listuser = ListUser(email=email, password=password)
        db.session.add(listuser)
        db.session.commit()
        session['listuser'] = listuser.email
        return redirect("/")
    else:
        return render_template('signup.html')

def is_email(string):
    # an email string has an '@' followed by a '.'
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present

@app.route("/logout", methods=['POST'])
def logout():
    del session['listuser']
    return redirect("/")


@app.route("/add", methods=['POST'])
def add_movie():
    # look inside the request to figure out what the user typed
    new_movie_name = request.form['new-movie']

    # if the user typed nothing at all, redirect and tell them the error
    if (not new_movie_name) or (new_movie_name.strip() == ""):
        error = "Please specify the movie you want to add."
        return redirect("/?error=" + error)


    movie = Movie(new_movie_name)
    db.session.add(movie)
    db.session.commit()
    return render_template('verifyadd.html', movie=movie)




#allows user to view movie list
        
@app.route('/list') 
def movie_list():
    movies = Movie.query.all()

    return render_template('movielist.html', title="Movie List", movies=movies)





#Allows list user to delete movie

@app.route('/delete', methods=['POST'])
def delete_movie():
    delete_movie= movie

    movie_id = int(request.form['movie-id'])
    movie = Movie.query.get(movie_id)
    db.session.add(movie)
    db.session.commit()

    return redirect('/list')




if __name__ == "__main__":
    app.run()