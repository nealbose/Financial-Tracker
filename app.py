from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Initialize database
db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class Transaction(db.Model):
    """Model for income and expense transactions"""
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # 'income' or 'expense'
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500))
    date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'category': self.category,
            'amount': self.amount,
            'description': self.description,
            'date': self.date.strftime('%Y-%m-%d'),
        }


class Budget(db.Model):
    """Model for budget management"""
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    limit = db.Column(db.Float, nullable=False)
    month = db.Column(db.String(7), nullable=False)  # Format: YYYY-MM
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'limit': self.limit,
            'month': self.month,
        }


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Dashboard - shows overview of finances"""
    # Get summary data
    transactions = Transaction.query.all()
    
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expenses
    
    # Get recent transactions
    recent = Transaction.query.order_by(Transaction.date.desc()).limit(5).all()
    
    return render_template('index.html',
                          total_income=total_income,
                          total_expenses=total_expenses,
                          balance=balance,
                          recent_transactions=recent)


@app.route('/add-transaction', methods=['GET', 'POST'])
def add_transaction():
    """Add a new transaction"""
    if request.method == 'POST':
        try:
            transaction = Transaction(
                type=request.form.get('type'),
                category=request.form.get('category'),
                amount=float(request.form.get('amount')),
                description=request.form.get('description'),
                date=datetime.strptime(request.form.get('date'), '%Y-%m-%d')
            )
            db.session.add(transaction)
            db.session.commit()
            return redirect(url_for('view_transactions'))
        except Exception as e:
            return f"Error adding transaction: {str(e)}", 400
    
    return render_template('add_transaction.html')


@app.route('/transactions')
def view_transactions():
    """View all transactions"""
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    return render_template('view_transactions.html', transactions=transactions)


@app.route('/budgets', methods=['GET', 'POST'])
def budgets():
    """Manage budgets"""
    if request.method == 'POST':
        try:
            budget = Budget(
                category=request.form.get('category'),
                limit=float(request.form.get('limit')),
                month=request.form.get('month')
            )
            db.session.add(budget)
            db.session.commit()
            return redirect(url_for('budgets'))
        except Exception as e:
            return f"Error adding budget: {str(e)}", 400
    
    all_budgets = Budget.query.all()
    return render_template('budgets.html', budgets=all_budgets)


@app.route('/reports')
def reports():
    """View financial reports and charts"""
    transactions = Transaction.query.all()
    
    # Calculate data for charts
    expense_by_category = {}
    for t in transactions:
        if t.type == 'expense':
            if t.category not in expense_by_category:
                expense_by_category[t.category] = 0
            expense_by_category[t.category] += t.amount
    
    return render_template('reports.html', expense_data=expense_by_category)


@app.route('/api/transactions', methods=['GET'])
def api_transactions():
    """API endpoint to get transactions as JSON"""
    transactions = Transaction.query.all()
    return jsonify([t.to_dict() for t in transactions])


@app.route('/delete-transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    """Delete a transaction"""
    try:
        transaction = Transaction.query.get(transaction_id)
        if transaction:
            db.session.delete(transaction)
            db.session.commit()
        return redirect(url_for('view_transactions'))
    except Exception as e:
        return f"Error deleting transaction: {str(e)}", 400


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
