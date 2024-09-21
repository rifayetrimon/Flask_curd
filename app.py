from flask import Flask, render_template
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
    if form.validate_on_submit():
        title = form.title.data
        authors_input = form.authors_input.data
        isbn = form.isbn.data
        year = form.year.data
        price = form.price.data
        quantity = form.quantity.data

        new_book = Book(
            title=title, 
            authors_input=authors_input, 
            isbn=isbn, 
            year=year, 
            price=price, 
            quantity=quantity
        )
        db.session.add(new_book)
        db.session.commit()

        flash('Book added successfully!', 'success')
        return redirect(url_for('add_book'))

    return render_template('create.html', form=form)





if  __name__ == "__main__":
    app.run(debug=True)