import sqlite3
import os
import os.path as osp
import pandas as pd
from datetime import datetime
from Expenses import Expense
from flask import Flask, render_template, g, request, redirect, url_for

# APP
app = Flask(__name__, template_folder="templates", static_folder='static')
# DATABASE
DATABASE = osp.dirname(osp.abspath(__file__)) + '\\' + 'expenses.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
@app.route("/expenses")
def main_page():
    # Get db entries
    cursor = get_db().cursor()
    cursor.execute("SELECT date, name, amount, category FROM expenses")
    data_from_db = cursor.fetchall()

    return render_template('main_page.html', data=data_from_db)


@app.route('/add_expense', methods=['POST', 'GET'])
def add_expense():
    if request.method == 'POST':
        date = datetime.today().date()
        name = request.form.get('name')
        amount = request.form.get('amount')
        category = request.form.get('category')

        data = {"date": date, "name": name, "amount": amount, "category": category}
        write_expenses_to_db(data)

        return redirect(url_for('main_page'))
    else:
        return render_template('add_expense_page.html')

@app.route('/delete_expense', methods=['DELETE', 'POST', 'GET'])
def delete_expense():
    if request.method == 'DELETE':
        delete_expense_query = "DELETE FROM expenses"
        cursor = get_db().cursor()
        cursor.execute(delete_expense_query)
        get_db().commit()
        return redirect(url_for('main_page'))
    else:
         render_template('main_page.html')


def write_expenses_to_db(data):
    cursor = get_db().cursor()
    sql_insert_query = f"INSERT INTO expenses (date, name, amount, category) VALUES ('{data['date']}', '{data['name']}', '{data['amount']}', '{data['category']}')"
    try:
        cursor.execute(sql_insert_query)
        get_db().commit()
    except Exception as e:
        print(f"Error executing query: {e}")


def summarize_expenses():
    cursor = get_db().cursor()
    sql_query = "SELECT category, SUM(amount) FROM expenses GROUP BY category"
    cursor.execute(sql_query)
    df = pd.read_sql_query(sql_query, get_db())
    print (df)

if __name__ == "__main__":
    app.run(debug=True)