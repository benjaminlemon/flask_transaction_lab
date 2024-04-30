# Import libraries
from flask import Flask, request, url_for, redirect, render_template

from transactions import transactions

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data

# Read operation
@app.route('/')
def get_transactions():
    return render_template('transactions.html', transactions = transactions, total = '')

# Create operation
@app.route('/add', methods = ['GET', 'POST'])
def add_transaction():
    if request.method == 'GET':
        return render_template('form.html')
    
    else:
        newTransaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }

        transactions.append(newTransaction)

    return redirect(url_for('get_transactions'))

# Update operation
@app.route('/edit/<int:transaction_id>', methods = ['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'GET':
        for transaction in transactions:
            if transaction_id == transaction['id']:
                return render_template('edit.html', transaction=transaction)
    else:
        date = request.form['date']
        amount = float(request.form['amount'])

        for transaction in transactions:
            if transaction_id == transaction['id']:
                transaction['date'] = date

                transaction['amount'] = amount

                break
            
    return redirect(url_for('get_transactions'))

# Delete operation
@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction_id == transaction['id']:
            transactions.remove(transaction)
            break

    return redirect(url_for('get_transactions'))

# Search Function
@app.route('/search', methods = ['POST', 'GET'])
def search_transactions():
    if request.method == 'POST':
        maximum = float(request.form['max_amount'])
        minimum = float(request.form['min_amount'])

        filtered_transactions = []

        for transaction in transactions:
            if float(transaction['amount']) >= minimum and float(transaction['amount']) <= maximum:

                filtered_transactions.append(transaction)
        
        return render_template('transactions.html', transactions=filtered_transactions)
    
    return render_template('search.html')

# Total Balance Function
@app.route('/balance')
def total_balance():
    total = float(0)
    for transaction in transactions:
        total += float(transaction['amount'])
        
    return render_template('transactions.html', transactions = transactions, total = total)

    
        

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
    