from app import app

if __name__ == '__main__':
    # ملاحظة: أول مرة تشغل فيها النظام، تأكد من إنشاء قاعدة البيانات
    # يمكنك إضافة db.create_all() هنا لمرة واحدة فقط
    app.run(debug=True)