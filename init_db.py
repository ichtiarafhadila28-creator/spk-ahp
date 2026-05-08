from app import app, db
from models import User, Kriteria
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    
    # Cek apakah admin sudah ada
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            password=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ User admin berhasil dibuat!")
        print("   Username: admin")
        print("   Password: admin123")
    
    # Buat kriteria default
    if Kriteria.query.count() == 0:
        kriteria_default = [
            Kriteria(nama='Produktivitas', bobot=0.3),
            Kriteria(nama='Luas Tanam', bobot=0.2),
            Kriteria(nama='Nilai Ekonomi', bobot=0.25),
            Kriteria(nama='Permintaan Pasar', bobot=0.15),
            Kriteria(nama='Kesesuaian Lahan', bobot=0.1),
        ]
        for k in kriteria_default:
            db.session.add(k)
        db.session.commit()
        print("✅ Kriteria default berhasil dibuat!")
    
    print("✅ Database berhasil diinisialisasi!")