from datetime import datetime, timedelta

from flask import Flask, jsonify, request, render_template

from Models.Movie import Movie
from Models.Reservation import Reservation
from Models.User import User

app = Flask(__name__)

global global_user

# To jest nasza statyczna baza danych
movies = [
    Movie('Movie1', 15.00, 2010),
    Movie('Movie2', 15.00, 2001),
    Movie('Movie3', 13.00, 2018),
    Movie('Movie4', 11.00, 1993)
]

users = [
    User(1, "Jan", "Kowalski"),
    User(2, "Piotr", "Nowak")
]

reservations = []


@app.route('/')
def index():
    # global reservations
    # reservations = []    # czyszczenie listy rezerwacji
    return render_template('set_user.html', users=users)


@app.route('/movies')
def render_movies():
    return render_template('movies.html', movies=movies)


@app.route('/user_reservations')
def render_user_reservations():
    print(global_user.id)
    reser = [reservation for reservation in reservations if reservation.user.id == global_user.id]
    print(reser)
    return render_template('user_reservations.html', reservations=reser)

@app.route('/index')
def render_index():
    return render_template('index.html')

@app.route('/reservation')
def render_reservation():
    return render_template('reservation.html', movies=movies, users=users)


@app.route('/all_user_reservations')
def render_all_user_reservations():
    return render_template('all_user_reservations.html', reservations=reservations)



@app.route('/', methods=['POST'])
def add_item():
    if request.method == 'POST':
        user = next((user for user in users if user.id == int(request.form['id'])), None)

        if user is None:
            return render_template('error.html', error="Nie istnieje taki user")

        global global_user
        global_user = user

        return render_template('index.html')




@app.route('/reservation', methods=['POST'])
def set_user():
    if request.method == 'POST':

        movie = next((movie for movie in movies if movie.title.lower() == request.form['movie_title'].lower()), None)
        date_from_str = request.form['date_from']
        date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
        days = int(request.form['days'])
        date_to = date_from + timedelta(days=days)

        is_conflict = False
        for reservation in reservations:
            if (date_from <= reservation.date_from <= date_to or date_from <= reservation.date_to <= date_to) and reservation.movie == movie:
                is_conflict = True
                break

        if(is_conflict):
            return render_template('error.html', error="rezerwacja koliduje")

        if movie is None:
            return render_template('error.html', error="Nie istniej taki movie")

        cost = movie.price * days
        reservations.append(Reservation(global_user, movie, date_from, date_to, cost))

        return render_template('user_reservations.html', reservations=reservations)




if __name__ == '__main__':
    app.run(debug=True)
