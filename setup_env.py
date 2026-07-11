import os
folders = ['app', 'app/templates']
files = {
    'app/__init__.py': "from flask import Flask\nfrom flask_sqlalchemy import SQLAlchemy\n\napp = Flask(__name__, template_folder='templates')\napp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_erp.db'\ndb = SQLAlchemy(app)\n\nfrom app import routes, models\n\nwith app.app_context():\n    db.create_all()",
    'app/routes.py': "from flask import render_template\nfrom app import app\n\n@app.route('/')\n@app.route('/dashboard')\ndef dashboard():\n    return render_template('dashboard.html', insight='النظام يعمل بنجاح!')",
    'app/models.py': "from app import db\n\nclass Sale(db.Model):\n    id = db.Column(db.Integer, primary_key=True)\n    product_name = db.Column(db.String(100))\n    price = db.Column(db.Float)",
    'app/templates/dashboard.html': "<h1>Neural ERP is Running!</h1>"
}
for folder in folders: os.makedirs(folder, exist_ok=True)
for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f: f.write(content)
print('تم البناء بنجاح! الآن اكتب: python run.py')
