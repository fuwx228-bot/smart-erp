from flask import render_template, redirect, url_for, request, session, flash
from app import app, db
from app.models import Sale, Complaint

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['logged_in'] = True
        username = request.form.get('username')
        session['user_name'] = username
        session['is_admin'] = (username.lower() == 'admin')
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/')
def dashboard():
    if not session.get('logged_in'): return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/sales')
def sales():
    if not session.get('logged_in'): return redirect(url_for('login'))
    page = request.args.get('page', 1, type=int)
    pagination = Sale.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('sales.html', sales=pagination.items, pagination=pagination)

@app.route('/add_sale', methods=['POST'])
def add_sale():
    if not session.get('logged_in'): return redirect(url_for('login'))
    new_sale = Sale(product_name=request.form.get('product'), price=float(request.form.get('price')), added_by=session.get('user_name'))
    db.session.add(new_sale)
    db.session.commit()
    return redirect(url_for('sales'))

@app.route('/edit_sale/<int:id>', methods=['GET', 'POST'])
def edit_sale(id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    sale = Sale.query.get_or_404(id)
    if request.method == 'POST':
        sale.product_name = request.form.get('product')
        sale.price = float(request.form.get('price'))
        db.session.commit()
        return redirect(url_for('sales'))
    return render_template('edit_sale.html', sale=sale)

@app.route('/delete_sale/<int:id>')
def delete_sale(id):
    if not session.get('is_admin'):
        flash('🚫 عذراً، الحذف للمدير فقط!')
        return redirect(url_for('sales'))
    sale = Sale.query.get_or_404(id)
    db.session.delete(sale)
    db.session.commit()
    return redirect(url_for('sales'))

@app.route('/complaints')
def complaints():
    if not session.get('logged_in'): return redirect(url_for('login'))
    all_complaints = Complaint.query.all()
    return render_template('complaints.html', complaints=all_complaints)

@app.route('/add_complaint', methods=['POST'])
def add_complaint():
    if not session.get('logged_in'): return redirect(url_for('login'))
    new_c = Complaint(content=request.form.get('complaint_text'))
    db.session.add(new_c)
    db.session.commit()
    return redirect(url_for('complaints'))

# --- هذه الدالة هي التي كانت مفقودة وتسببت بالخطأ ---
@app.route('/settings')
def settings():
    if not session.get('logged_in'): return redirect(url_for('login'))
    return render_template('settings.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))