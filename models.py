from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='admin')

class Komoditas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    produktivitas = db.Column(db.Float, nullable=False)
    luas_tanam = db.Column(db.Float, nullable=False)
    nilai_ekonomi = db.Column(db.Float, nullable=False)
    permintaan_pasar = db.Column(db.Float, nullable=False)
    kesesuaian_lahan = db.Column(db.Float, nullable=False)

class Kriteria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    bobot = db.Column(db.Float, nullable=False)

class Hasil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    komoditas_id = db.Column(db.Integer, db.ForeignKey('komoditas.id'))
    skor = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    tanggal = db.Column(db.DateTime, default=datetime.utcnow)
    komoditas = db.relationship('Komoditas', backref='hasil')
    
class MatriksPerbandingan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kriteria_baris_id = db.Column(db.Integer, db.ForeignKey('kriteria.id'))
    kriteria_kolom_id = db.Column(db.Integer, db.ForeignKey('kriteria.id'))
    nilai = db.Column(db.Float, nullable=False)
    kriteria_baris = db.relationship('Kriteria', foreign_keys=[kriteria_baris_id])
    kriteria_kolom = db.relationship('Kriteria', foreign_keys=[kriteria_kolom_id])