from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)  # Title of the book
    authors_input = db.Column(db.String(120), nullable=False)  # Author's name
    isbn = db.Column(db.String(20), nullable=False, unique=True)  # ISBN number, unique for each book
    year = db.Column(db.Integer, nullable=False)  # Year of publication
    price = db.Column(db.Float, nullable=False)  # Price of the book
    quantity = db.Column(db.Integer, nullable=False)  # Number of books available

    def __repr__(self):
        return f"<Book {self.title}>"
