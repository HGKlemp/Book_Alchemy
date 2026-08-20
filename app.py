import os
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from data_models import db, Author, Book


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
)

db.init_app(app)


@app.route("/")
def home():
    search = request.args.get("search")
    sort = request.args.get("sort", "title")
    message = request.args.get("message")

    if search:
        books = (
            db.session.query(Book)
            .filter(Book.title.like(f"%{search}%"))
            .all()
        )

    elif sort == "author":
        books = (
            db.session.query(Book)
            .join(Author)
            .order_by(Author.name)
            .all()
        )

    else:
        books = (
            db.session.query(Book)
            .order_by(Book.title)
            .all()
        )

    return render_template(
        "home.html",
        books=books,
        search=search,
        message=message
    )


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    message = None

    if request.method == "POST":
        name = request.form.get("name")
        birthdate = request.form.get("birthdate")
        date_of_death = request.form.get("date_of_death")

        author = Author(
            name=name,
            birth_date=datetime.strptime(
                birthdate,
                "%Y-%m-%d"
            ).date(),
            date_of_death=(
                datetime.strptime(
                    date_of_death,
                    "%Y-%m-%d"
                ).date()
                if date_of_death
                else None
            )
        )

        db.session.add(author)
        db.session.commit()

        message = "Author successfully added."

    return render_template(
        "add_author.html",
        message=message
    )


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    message = None

    authors = (
        db.session.query(Author)
        .order_by(Author.name)
        .all()
    )

    if request.method == "POST":
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        publication_year = request.form.get("publication_year")
        author_id = request.form.get("author_id")

        book = Book(
            isbn=isbn,
            title=title,
            publication_year=int(publication_year),
            author_id=int(author_id)
        )

        db.session.add(book)
        db.session.commit()

        message = "Book successfully added."

    return render_template(
        "add_book.html",
        authors=authors,
        message=message
    )


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    book = db.session.get(Book, book_id)

    if book is None:
        return redirect(url_for("home"))

    author = book.author

    db.session.delete(book)
    db.session.commit()

    remaining_books = (
        db.session.query(Book)
        .filter_by(author_id=author.id)
        .count()
    )

    if remaining_books == 0:
        db.session.delete(author)
        db.session.commit()

    return redirect(
        url_for(
            "home",
            message="Book successfully deleted."
        )
    )


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)