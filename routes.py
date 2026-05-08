from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import User, Komoditas, Kriteria, Hasil, MatriksPerbandingan
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ========== LOGIN ==========
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Username atau password salah!', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    # ========== REGISTER ==========
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        konfirmasi = request.form['konfirmasi']

        if password != konfirmasi:
            flash('Password dan konfirmasi tidak sama!', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan!', 'danger')
            return redirect(url_for('register'))

        user = User(
            username=username,
            password=generate_password_hash(password),
            role='user'
        )
        db.session.add(user)
        db.session.commit()
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# ========== DASHBOARD ==========
@app.route('/dashboard')
@login_required
def dashboard():
    total_komoditas = Komoditas.query.count()
    total_kriteria = Kriteria.query.count()
    total_user = User.query.count()
    return render_template('dashboard.html', 
                           total_komoditas=total_komoditas,
                           total_kriteria=total_kriteria,
                           total_user=total_user)

# ========== KOMODITAS ==========
@app.route('/komoditas')
@login_required
def komoditas():
    data = Komoditas.query.all()
    return render_template('komoditas.html', data=data)

@app.route('/komoditas/tambah', methods=['GET', 'POST'])
@login_required
def tambah_komoditas():
    if request.method == 'POST':
        k = Komoditas(
            nama=request.form['nama'],
            produktivitas=float(request.form['produktivitas']),
            luas_tanam=float(request.form['luas_tanam']),
            nilai_ekonomi=float(request.form['nilai_ekonomi']),
            permintaan_pasar=float(request.form['permintaan_pasar']),
            kesesuaian_lahan=float(request.form['kesesuaian_lahan'])
        )
        db.session.add(k)
        db.session.commit()
        flash('Komoditas berhasil ditambahkan!', 'success')
        return redirect(url_for('komoditas'))
    return render_template('tambah_komoditas.html')

@app.route('/komoditas/ubah/<int:id>', methods=['GET', 'POST'])
@login_required
def ubah_komoditas(id):
    k = Komoditas.query.get_or_404(id)
    if request.method == 'POST':
        k.nama = request.form['nama']
        k.produktivitas = float(request.form['produktivitas'])
        k.luas_tanam = float(request.form['luas_tanam'])
        k.nilai_ekonomi = float(request.form['nilai_ekonomi'])
        k.permintaan_pasar = float(request.form['permintaan_pasar'])
        k.kesesuaian_lahan = float(request.form['kesesuaian_lahan'])
        db.session.commit()
        flash('Komoditas berhasil diubah!', 'success')
        return redirect(url_for('komoditas'))
    return render_template('ubah_komoditas.html', k=k)

@app.route('/komoditas/hapus/<int:id>')
@login_required
def hapus_komoditas(id):
    k = Komoditas.query.get_or_404(id)
    db.session.delete(k)
    db.session.commit()
    flash('Komoditas berhasil dihapus!', 'success')
    return redirect(url_for('komoditas'))

# ========== KRITERIA ==========
@app.route('/kriteria')
@login_required
def kriteria():
    data = Kriteria.query.all()
    return render_template('kriteria.html', data=data)

@app.route('/kriteria/tambah', methods=['GET', 'POST'])
@login_required
def tambah_kriteria():
    if request.method == 'POST':
        k = Kriteria(
            nama=request.form['nama'],
            bobot=float(request.form['bobot'])
        )
        db.session.add(k)
        db.session.commit()
        flash('Kriteria berhasil ditambahkan!', 'success')
        return redirect(url_for('kriteria'))
    return render_template('tambah_kriteria.html')

@app.route('/kriteria/ubah/<int:id>', methods=['GET', 'POST'])
@login_required
def ubah_kriteria(id):
    k = Kriteria.query.get_or_404(id)
    if request.method == 'POST':
        k.nama = request.form['nama']
        k.bobot = float(request.form['bobot'])
        db.session.commit()
        flash('Kriteria berhasil diubah!', 'success')
        return redirect(url_for('kriteria'))
    return render_template('ubah_kriteria.html', k=k)

@app.route('/kriteria/hapus/<int:id>')
@login_required
def hapus_kriteria(id):
    k = Kriteria.query.get_or_404(id)
    db.session.delete(k)
    db.session.commit()
    flash('Kriteria berhasil dihapus!', 'success')
    return redirect(url_for('kriteria'))

# ========== USER ==========
@app.route('/user')
@login_required
def user():
    data = User.query.all()
    return render_template('user.html', data=data)

@app.route('/user/tambah', methods=['GET', 'POST'])
@login_required
def tambah_user():
    if request.method == 'POST':
        u = User(
            username=request.form['username'],
            password=generate_password_hash(request.form['password']),
            role=request.form['role']
        )
        db.session.add(u)
        db.session.commit()
        flash('User berhasil ditambahkan!', 'success')
        return redirect(url_for('user'))
    return render_template('tambah_user.html')

@app.route('/user/hapus/<int:id>')
@login_required
def hapus_user(id):
    u = User.query.get_or_404(id)
    db.session.delete(u)
    db.session.commit()
    flash('User berhasil dihapus!', 'success')
    return redirect(url_for('user'))

# ========== PERHITUNGAN FUZZY AHP ==========
@app.route('/perhitungan')
@login_required
def perhitungan():
    import numpy as np
    komoditas_list = Komoditas.query.all()
    kriteria_list = Kriteria.query.all()

    if not komoditas_list or not kriteria_list:
        flash('Data komoditas atau kriteria belum lengkap!', 'warning')
        return redirect(url_for('dashboard'))

    bobot = [k.bobot for k in kriteria_list]
    total_bobot = sum(bobot)
    bobot_normal = [b/total_bobot for b in bobot]

    hasil_list = []
    for k in komoditas_list:
        nilai = [
            k.produktivitas,
            k.luas_tanam,
            k.nilai_ekonomi,
            k.permintaan_pasar,
            k.kesesuaian_lahan
        ]
        skor = sum(nilai[i] * bobot_normal[i] for i in range(min(len(nilai), len(bobot_normal))))
        hasil_list.append({'komoditas': k, 'skor': round(skor, 4)})

    hasil_list.sort(key=lambda x: x['skor'], reverse=True)
    for i, h in enumerate(hasil_list):
        h['ranking'] = i + 1

    return render_template('perhitungan.html', 
                           hasil_list=hasil_list,
                           kriteria_list=kriteria_list,
                           bobot_normal=bobot_normal,
                           enumerate=enumerate)
                          # ========== CETAK PDF ==========
@app.route('/cetak-pdf')
@login_required
def cetak_pdf():
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.units import cm
    from flask import make_response
    from fuzzy_ahp import hitung_fuzzy_ahp, hitung_skor_komoditas
    import io

    kriteria_list = Kriteria.query.all()
    komoditas_list = Komoditas.query.all()
    data_matriks = MatriksPerbandingan.query.all()

    matriks_nilai = {}
    for m in data_matriks:
        idx_baris = next((i for i, k in enumerate(kriteria_list) if k.id == m.kriteria_baris_id), None)
        idx_kolom = next((i for i, k in enumerate(kriteria_list) if k.id == m.kriteria_kolom_id), None)
        if idx_baris is not None and idx_kolom is not None and idx_baris < idx_kolom:
            matriks_nilai[(idx_baris, idx_kolom)] = m.nilai

    hasil = hitung_fuzzy_ahp(matriks_nilai, len(kriteria_list))
    skor_komoditas = hitung_skor_komoditas(komoditas_list, hasil['bobot_normal'], kriteria_list)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('title', fontSize=14, fontName='Helvetica-Bold', alignment=1, spaceAfter=4)
    subtitle_style = ParagraphStyle('subtitle', fontSize=10, fontName='Helvetica', alignment=1, spaceAfter=4)
    heading_style = ParagraphStyle('heading', fontSize=11, fontName='Helvetica-Bold', spaceAfter=6, spaceBefore=10)
    normal_style = ParagraphStyle('normal', fontSize=9, fontName='Helvetica', spaceAfter=4)
    center_style = ParagraphStyle('center', fontSize=9, fontName='Helvetica', alignment=1)

    header_color = colors.HexColor('#1a5276')
    alt_color = colors.HexColor('#d6eaf8')
    green_color = colors.HexColor('#d5f5e3')

    content = []

    # ===== HEADER =====
    content.append(Paragraph('SISTEM PENDUKUNG KEPUTUSAN', title_style))
    content.append(Paragraph('PENENTUAN KOMODITAS PERTANIAN UNGGULAN', title_style))
    content.append(Paragraph('KABUPATEN BENER MERIAH', title_style))
    content.append(Paragraph('Metode: Fuzzy Analytical Hierarchy Process (Fuzzy AHP) - Chang (1996)', subtitle_style))
    content.append(Spacer(1, 0.3*cm))

    from datetime import datetime
    content.append(Paragraph(f'Tanggal Cetak: {datetime.now().strftime("%d %B %Y %H:%M")}', normal_style))
    content.append(Spacer(1, 0.3*cm))

    # ===== MATRIKS TFN =====
    content.append(Paragraph('1. Matriks Perbandingan Berpasangan dengan TFN', heading_style))
    
    tfn_header = ['Kriteria'] + [k.nama for k in kriteria_list]
    tfn_data = [tfn_header]
    for i, ki in enumerate(kriteria_list):
        baris = [ki.nama]
        for j in range(len(kriteria_list)):
            l, m, u = hasil['matriks_tfn'][i][j]
            baris.append(f'({l},{m},{u})')
        tfn_data.append(baris)

    col_width = 2.2*cm
    tfn_table = Table(tfn_data, colWidths=[3*cm] + [col_width]*len(kriteria_list))
    tfn_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_color),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, alt_color]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    content.append(tfn_table)

    # ===== NILAI Si =====
    content.append(Paragraph('2. Nilai Fuzzy Synthetic Extent (Si)', heading_style))
    si_data = [['No', 'Kriteria', 'l', 'm', 'u']]
    for i, k in enumerate(kriteria_list):
        l, m, u = hasil['Si'][i]
        si_data.append([str(i+1), k.nama, str(l), str(m), str(u)])

    si_table = Table(si_data, colWidths=[1.5*cm, 6*cm, 3*cm, 3*cm, 3*cm])
    si_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_color),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, alt_color]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    content.append(si_table)

    # ===== BOBOT VEKTOR =====
    content.append(Paragraph('3. Bobot Vektor dan Normalisasi', heading_style))
    bobot_data = [['No', 'Kriteria', 'Bobot Vektor (d\')', 'Bobot Normal (W)']]
    for i, k in enumerate(kriteria_list):
        bobot_data.append([
            str(i+1),
            k.nama,
            str(hasil['bobot_vektor'][i]),
            str(hasil['bobot_normal'][i])
        ])

    bobot_table = Table(bobot_data, colWidths=[1.5*cm, 6*cm, 4*cm, 4*cm])
    bobot_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_color),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, alt_color]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    content.append(bobot_table)

    # ===== HASIL PERANKINGAN =====
    content.append(Paragraph('4. Hasil Perankingan Komoditas Pertanian', heading_style))
    hasil_data = [['Ranking', 'Komoditas', 'Produktivitas', 'Luas Tanam', 'Nilai Ekonomi', 'Permintaan Pasar', 'Kesesuaian Lahan', 'Skor']]
    for h in skor_komoditas:
        hasil_data.append([
            str(h['ranking']),
            h['komoditas'].nama,
            str(h['komoditas'].produktivitas),
            str(h['komoditas'].luas_tanam),
            str(h['komoditas'].nilai_ekonomi),
            str(h['komoditas'].permintaan_pasar),
            str(h['komoditas'].kesesuaian_lahan),
            str(h['skor'])
        ])

    hasil_table = Table(hasil_data, colWidths=[1.5*cm, 3*cm, 2.2*cm, 2.2*cm, 2.2*cm, 2.5*cm, 2.5*cm, 1.9*cm])
    hasil_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_color),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, alt_color]),
        ('BACKGROUND', (0,1), (-1,1), green_color),
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    content.append(hasil_table)

    # ===== KESIMPULAN =====
    if skor_komoditas:
        content.append(Spacer(1, 0.5*cm))
        content.append(Paragraph(
            f'Kesimpulan: Berdasarkan perhitungan Fuzzy AHP Chang (1996), komoditas pertanian unggulan '
            f'di Kabupaten Bener Meriah adalah <b>{skor_komoditas[0]["komoditas"].nama}</b> '
            f'dengan skor tertinggi <b>{skor_komoditas[0]["skor"]}</b>.',
            normal_style
        ))

    doc.build(content)
    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=hasil-spk-fuzzy-ahp.pdf'
    return response
    # ========== KUESIONER & FUZZY AHP ==========
@app.route('/kuesioner', methods=['GET', 'POST'])
@login_required
def kuesioner():
    from fuzzy_ahp import hitung_fuzzy_ahp
    kriteria_list = Kriteria.query.all()

    # Ambil data existing
    existing = {}
    data_matriks = MatriksPerbandingan.query.all()
    for m in data_matriks:
        existing[(m.kriteria_baris_id, m.kriteria_kolom_id)] = m.nilai

    if request.method == 'POST':
        # Hapus data lama
        MatriksPerbandingan.query.delete()
        db.session.commit()

        # Simpan data baru
        for ki in kriteria_list:
            for kj in kriteria_list:
                key = f'nilai_{ki.id}_{kj.id}'
                if key in request.form:
                    nilai = float(request.form[key])
                    m = MatriksPerbandingan(
                        kriteria_baris_id=ki.id,
                        kriteria_kolom_id=kj.id,
                        nilai=nilai
                    )
                    db.session.add(m)
        db.session.commit()
        flash('Kuesioner berhasil disimpan!', 'success')
        return redirect(url_for('perhitungan_fuzzy'))

    return render_template('kuesioner.html',
                           kriteria_list=kriteria_list,
                           existing=existing,
                           enumerate=enumerate)

@app.route('/perhitungan-fuzzy')
@login_required
def perhitungan_fuzzy():
    from fuzzy_ahp import hitung_fuzzy_ahp, hitung_skor_komoditas
    kriteria_list = Kriteria.query.all()
    komoditas_list = Komoditas.query.all()

    if not kriteria_list or not komoditas_list:
        flash('Data kriteria atau komoditas belum lengkap!', 'warning')
        return redirect(url_for('dashboard'))

    # Ambil data matriks
    data_matriks = MatriksPerbandingan.query.all()
    if not data_matriks:
        flash('Silakan isi kuesioner terlebih dahulu!', 'warning')
        return redirect(url_for('kuesioner'))

    matriks_nilai = {}
    for m in data_matriks:
        # Cari index kriteria
        idx_baris = next((i for i, k in enumerate(kriteria_list) if k.id == m.kriteria_baris_id), None)
        idx_kolom = next((i for i, k in enumerate(kriteria_list) if k.id == m.kriteria_kolom_id), None)
        if idx_baris is not None and idx_kolom is not None and idx_baris < idx_kolom:
            matriks_nilai[(idx_baris, idx_kolom)] = m.nilai

    hasil = hitung_fuzzy_ahp(matriks_nilai, len(kriteria_list))
    skor_komoditas = hitung_skor_komoditas(komoditas_list, hasil['bobot_normal'], kriteria_list)

    # Update bobot kriteria di database
    for i, k in enumerate(kriteria_list):
        k.bobot = hasil['bobot_normal'][i]
    db.session.commit()

    return render_template('perhitungan_fuzzy.html',
                           kriteria_list=kriteria_list,
                           komoditas_list=komoditas_list,
                           hasil=hasil,
                           skor_komoditas=skor_komoditas,
                           enumerate=enumerate)