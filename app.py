from flask import Flask, render_template, request
from flask import flash, redirect, url_for
from forms import BookForm
from models import db, Book
from flask_wtf.csrf import CSRFProtect



app = Flask(__name__)


app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

csrf = CSRFProtect(app)




@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if request.method == 'POST':
        data = request.form
        title = data.get('title')
        authors = data.get('authors_input')
        isbn = data.get('isbn')
        year = data.get('year')
        price = data.get('price')
        quantity = data.get('quantity')

        new_item = Book(
            title=title,
            authors_input=authors,
            isbn=isbn,
            year=year,
            price=price,
            quantity=quantity
        )

        db.session.add(new_item)
        db.session.commit()

        flash('Book added successfully!', 'success')
        return redirect(url_for('add_book'))

    return render_template('create.html', form = form)



@app.route('/home')
def home():
    books = Book.query.all()
    return render_template('home.html', books = books)


@app.route('/book/<int:id>')
def book(id):
    book = Book.query.get(id)
    if book is None:
        flash('Book not found!', 'error')
        return redirect(url_for('home'))
    return render_template('singel.html', book_details = book)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    book = Book.query.get(id)
    if book is None:
        flash('Book not found!', 'error')
        return redirect(url_for('home'))
    form = BookForm(obj=book)
    if request.method == 'POST':
        data = request.form
        title = data.get('title')
        authors = data.get('authors_input')
        isbn = data.get('isbn')
        year = data.get('year')
        price = data.get('price')
        quantity = data.get('quantity')

        book.title = title
        book.authors_input = authors
        book.isbn = isbn
        book.year = year
        book.price = price
        book.quantity = quantity

        db.session.commit()

        flash('Book updated successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('update.html', form = form, book = book)




@app.route('/delete/<int:id>')
def delete(id):
    book = Book.query.get(id)
    if book is None:
        flash('Book not found!', 'error')
        return redirect(url_for('home'))
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('home'))





if  __name__ == "__main__":
    app.run(debug=True)