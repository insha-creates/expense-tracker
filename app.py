from flask import Flask, render_template, request, redirect, flash 
import sqlite3

app = Flask(__name__)
app.secret_key = "expense123"

# Database setup
def init_db():

    conn = sqlite3.connect('expenses.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        amount REAL,
        category TEXT,
        date TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():

    conn = sqlite3.connect('expenses.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()

    conn.close()

    total = sum(expense[2] for expense in expenses)

    return render_template(
        'index.html',
        expenses=expenses,
        total=total
    )

@app.route('/add', methods=['POST'])
def add():

    title = request.form['title']
    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']

    conn = sqlite3.connect('expenses.db')
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO expenses(title, amount, category, date) VALUES(?,?,?,?)",
        (title, amount, category, date)
    )

    conn.commit()
    conn.close()

    flash("Expense Added Successfully 🎉")

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect('expenses.db')
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM expenses WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')

# Edit page
@app.route('/edit/<int:id>')
def edit(id):

    conn = sqlite3.connect('expenses.db')
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM expenses WHERE id=?",
        (id,)
    )

    expense = cur.fetchone()

    conn.close()

    return render_template(
        'edit.html',
        expense=expense
    )

# Update expense
@app.route('/update/<int:id>', methods=['POST'])
def update(id):

    title = request.form['title']
    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']

    conn = sqlite3.connect('expenses.db')
    cur = conn.cursor()

    cur.execute(
        '''
        UPDATE expenses
        SET title=?,
            amount=?,
            category=?,
            date=?
        WHERE id=?
        ''',
        (title, amount, category, date, id)
    )

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)