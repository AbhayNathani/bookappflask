from telnetlib import STATUS
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(10), nullable=True)

    def __repr__(self) -> str:
        # Function prints info when printed object
        return f"{self.no} --> {self.title} -- {self.author} - {self.status}"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        add_title = request.form['title']
        add_author = request.form['author']
        print(add_title + "--"+add_author + "--")
        book = Book(title=add_title, author=add_author, status="Not Reading")
        db.session.add(book)
        db.session.commit()
    allBooks = Book.query.all()

    return render_template('index.html', allBooks=allBooks)


@app.route('/books')
def books():
    allBooks = Book.query.all()
    print(allBooks)
    return 'Here are the list of books...'


@app.route('/delete/<int:no>')
def delete_book(no):
    del_book = Book.query.filter_by(no=no).first()
    db.session.delete(del_book)
    db.session.commit()
    return redirect('/')


@app.route('/change/<int:no>')
def change_status(no):

    return f'Changing Status Of Entery {no}'


if __name__ == '__main__':
    app.run(debug=True, port=8000)
