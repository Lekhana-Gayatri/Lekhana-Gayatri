from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__, static_url_path='/static')
# MySQL Configuration
app.config['MYSQL_HOST'] = 'book-store-db.cno3ddrupypu.eu-north-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin123'
app.config['MYSQL_DB'] = 'bookstore_db'
mysql = MySQL(app)

with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS books (
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   title VARCHAR(255) NOT NULL,
                   author VARCHAR(255) NOT NULL,
                   genre VARCHAR(100),
                   price FLOAT
                   )''')
    cur.close()


@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        price = request.form['price']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO books (title, author, genre, price) VALUES (%s, %s, %s, %s)",
                    (title, author, genre, price))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))
    return render_template('add_book.html')

# Read all books
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    cur.close()
    return render_template('index.html', books=books)

# Update a book
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        price = request.form['price']

        cur.execute("UPDATE books SET title=%s, author=%s, genre=%s, price=%s WHERE id=%s", (title, author, genre, price, id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))
    cur.execute("SELECT * FROM books WHERE id = %s", (id,))
    book = cur.fetchone()
    cur.close()
    return render_template('edit_book.html', book=book)

@app.route('/delete/<int:id>')
def delete_book(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM books WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

    
