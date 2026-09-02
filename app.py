import os
from datetime import date, datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from data_models import db, Author, Book


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
)

db.init_app(app)


@app.route("/")
def home():
    """Shows all books and allows search and sorting."""

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
    """Adds a new author to the database."""

    message = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        birthdate = request.form.get("birthdate", "").strip()
        date_of_death = request.form.get("date_of_death", "").strip()

        if not name or not birthdate:
            message = "Name and birth date are required."

        else:
            try:
                birth_date = datetime.strptime(
                    birthdate,
                    "%Y-%m-%d"
                ).date()

                death_date = (
                    datetime.strptime(
                        date_of_death,
                        "%Y-%m-%d"
                    ).date()
                    if date_of_death
                    else None
                )

                if birth_date > date.today():
                    message = "Birth date cannot be in the future."

                elif death_date and death_date > date.today():
                    message = "Date of death cannot be in the future."

                elif death_date and death_date < birth_date:
                    message = (
                        "Date of death cannot be before birth date."
                    )

                else:
                    existing_author = (
                        db.session.query(Author)
                        .filter(
                            func.lower(Author.name) == name.lower(),
                            Author.birth_date == birth_date
                        )
                        .first()
                    )

                    if existing_author:
                        message = "This author already exists."

                    else:
                        author = Author(
                            name=name,
                            birth_date=birth_date,
                            date_of_death=death_date
                        )

                        try:
                            db.session.add(author)
                            db.session.commit()
                            message = "Author successfully added."

                        except SQLAlchemyError:
                            db.session.rollback()
                            message = (
                                "An error occurred while saving the author."
                            )

            except ValueError:
                message = "Please enter valid dates."

    return render_template(
        "add_author.html",
        message=message
    )


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """Adds a new book to the database."""

    message = None

    authors = (
        db.session.query(Author)
        .order_by(Author.name)
        .all()
    )

    if request.method == "POST":
        isbn = request.form.get("isbn", "").strip()
        title = request.form.get("title", "").strip()
        publication_year = request.form.get(
            "publication_year",
            ""
        ).strip()
        author_id = request.form.get("author_id", "").strip()

        if not isbn or not title or not publication_year or not author_id:
            message = "All fields are required."

        else:
            try:
                publication_year = int(publication_year)
                author_id = int(author_id)

                if publication_year < 1 or publication_year > date.today().year:
                    message = "Please enter a valid publication year."

                else:
                    author = db.session.get(Author, author_id)

                    if author is None:
                        message = "Author not found."

                    else:
                        existing_isbn = (
                            db.session.query(Book)
                            .filter_by(isbn=isbn)
                            .first()
                        )

                        existing_book = (
                            db.session.query(Book)
                            .filter(
                                func.lower(Book.title) == title.lower(),
                                Book.author_id == author_id
                            )
                            .first()
                        )

                        if existing_isbn:
                            message = "This ISBN already exists."

                        elif existing_book:
                            message = (
                                "This book already exists for this author."
                            )

                        else:
                            book = Book(
                                isbn=isbn,
                                title=title,
                                publication_year=publication_year,
                                author_id=author_id
                            )

                            try:
                                db.session.add(book)
                                db.session.commit()
                                message = "Book successfully added."

                            except SQLAlchemyError:
                                db.session.rollback()
                                message = (
                                    "An error occurred while saving the book."
                                )

            except ValueError:
                message = "Please enter valid values."

    return render_template(
        "add_book.html",
        authors=authors,
        message=message
    )


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """Deletes a book and removes the author if no books remain."""

    book = db.session.get(Book, book_id)

    if book is None:
        return redirect(url_for("home"))

    author = book.author

    try:
        db.session.delete(book)
        db.session.flush()

        remaining_books = (
            db.session.query(Book)
            .filter_by(author_id=author.id)
            .count()
        )

        if remaining_books == 0:
            db.session.delete(author)

        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        return redirect(
            url_for(
                "home",
                message="An error occurred while deleting the book."
            )
        )

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