from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os, shutil

app = Flask(__name__)
app.secret_key = 'smart_erp_pro_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_erp.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), default='عام')

with app.app_context(): db.create_all()

# كود الواجهة المدمج (لا يحتاج ملف HTML منفصل)
HTML_CODE = '''
<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<style>
    body { background: linear-gradient(rgba(10,15,25,0.9), rgba(10,15,25,0.9)), url('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1920&q=80'); background-size: cover; color: #fff; font-family: monospace; padding: 20px; }
    .nav { background: #000; padding: 15px; border-bottom: 2px solid #ff9900; display: flex; justify-content: space-between; }
    input, select { background: #000; border: 1px solid #ff9900; color: #ff9900; padding: 10px; }
    button { background: #ff9900; border: none; padding: 10px 20px; cursor: pointer; color: #000; font-weight: bold; }
    table { width: 100%; border-collapse: collapse; background: rgba(0,0,0,0.6); margin-top:20px; }
    th { background: #ff9900; color: #000; padding: 15px; }
    td { border: 1px solid #444; padding: 15px; text-align: center; }
</style></head><body>
<div style="max-width:900px; margin:auto;">
    <div class="nav"><h2>SYSTEM: Smart ERP</h2><a href="/logout" style="color:#ff9900;">تسجيل خروج</a></div>
    <form action="/add" method="POST" style="margin:20px 0; display:flex; gap:10px;">
        <input type="text" name="name" placeholder="اسم المنتج" required>
        <input type="number" step="0.01" name="price" placeholder="السعر" required>
        <select name="category"><option>مخزن</option><option>مكتب</option></select>
        <button type="submit">إضافة</button>
    </form>
    <table><tr><th>المنتج</th><th>السعر</th><th>-</th></tr>
    {% for p in products %}<tr><td>{{p.name}}</td><td>{{p.price}} $</td><td><a href="/delete/{{p.id}}" style="color:red;">حذف</a></td></tr>{% endfor %}
    </table>
</div></body></html>
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form['password'] == '1234':
        session['logged_in'] = True
        return redirect(url_for('home'))
    return '<body style="background:#000; color:#ff9900; display:flex; justify-content:center; align-items:center; height:100vh;"><form method="POST"><input type="password" name="password" required><button type="submit">دخول</button></form></body>'

@app.route('/')
def home():
    if not session.get('logged_in'): return redirect(url_for('login'))
    return render_template_string(HTML_CODE, products=Product.query.all())

@app.route('/add', methods=['POST'])
def add():
    db.session.add(Product(name=request.form['name'], price=float(request.form['price']), category=request.form['category']))
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:id>')
def delete(id):
    db.session.delete(Product.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__': app.run(debug=True)