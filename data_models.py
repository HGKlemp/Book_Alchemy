from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Author(db.Model):
    """Represents an author in the database."""

    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=True)

    books = db.relationship(
        "Book",
        back_populates="author"
    )

    def __str__(self):
        """Returns the name of the author."""
        return self.name

    def __repr__(self):
        """Returns a simple representation of the author."""
        return f"<Author {self.name}>"


class Book(db.Model):
    """Represents a book in the database."""

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)

    isbn = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    publication_year = db.Column(
        db.Integer,
        nullable=False
    )

    author_id = db.Column(
        db.Integer,
        db.ForeignKey("authors.id"),
        nullable=False
    )

    author = db.relationship(
        "Author",
        back_populates="books"
    )

    def __str__(self):
        """Returns the title of the book."""
        return self.title

    def __repr__(self):
        """Returns a simple representation of the book."""
        return f"<Book {self.title}>"