import os.path as osp
import pandas as pd
from flask import Flask, render_template, g, request, redirect, url_for
from db import db, Expense

app = Flask(__name__, template_folder="templates", static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'

db.init_app(app)

# Crear la base de datos y las tablas si no existen
with app.app_context():
    db.create_all()

@app.route("/")
@app.route('/expenses', methods=['GET', 'DELETE'])
def main_page():
    expenses = Expense.query.all()
    return render_template('main_page.html', data=expenses)

@app.route('/add_expense', methods=['POST', 'GET'])
def add_expense():
    if request.method == 'POST':
        data = request.form.to_dict()
        new_expense = Expense(date=data['date'], 
                              name=data['name'], 
                              amount=data['amount'], 
                              category=data['category']
                              )
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('main_page'))
    else:
        return render_template('add_expense_page.html')

@app.route('/delete_expenses', methods=['DELETE', 'GET'])
def delete_expenses():
    if request.method == 'DELETE':
        try:
            db.session.query(Expense).delete()
            db.session.commit()
        except:
            db.session.rollback()
    return redirect(url_for('main_page'))


if __name__ == "__main__":
    app.run(debug=True)