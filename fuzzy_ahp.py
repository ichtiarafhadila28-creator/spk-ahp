import numpy as np

# Tabel TFN Chang sesuai skripsi
TFN_TABLE = {
    1: (1, 1, 1),
    2: (0.5, 1, 1.5),
    3: (1, 1.5, 2),
    4: (1.5, 2, 2.5),
    5: (2, 2.5, 3),
    6: (2.5, 3, 3.5),
    7: (3, 3.5, 4),
    8: (3.5, 4, 4.5),
    9: (4, 4.5, 4.5),
}

RECIPROCAL_TABLE = {
    1: (1, 1, 1),
    2: (0.6667, 1, 2),
    3: (0.5, 0.6667, 1),
    4: (0.4, 0.5, 0.6667),
    5: (0.3333, 0.4, 0.5),
    6: (0.2857, 0.3333, 0.4),
    7: (0.25, 0.2857, 0.3333),
    8: (0.2222, 0.25, 0.2857),
    9: (0.2222, 0.2222, 0.25),
}

def get_tfn(nilai):
    """Konversi nilai skala ke TFN"""
    if nilai >= 1:
        return TFN_TABLE.get(int(nilai), (1, 1, 1))
    else:
        # Reciprocal
        reciprocal = int(round(1/nilai))
        return RECIPROCAL_TABLE.get(reciprocal, (1, 1, 1))

def hitung_fuzzy_ahp(matriks_nilai, n_kriteria):
    """
    Hitung Fuzzy AHP Chang
    matriks_nilai: dict {(i,j): nilai_skala}
    n_kriteria: jumlah kriteria
    """
    # Step 1: Bangun matriks TFN
    matriks_tfn = []
    for i in range(n_kriteria):
        baris = []
        for j in range(n_kriteria):
            if i == j:
                baris.append((1, 1, 1))
            elif (i, j) in matriks_nilai:
                nilai = matriks_nilai[(i, j)]
                baris.append(get_tfn(nilai))
            elif (j, i) in matriks_nilai:
                nilai = matriks_nilai[(j, i)]
                # Reciprocal
                if nilai >= 1:
                    reciprocal = int(nilai)
                    baris.append(RECIPROCAL_TABLE.get(reciprocal, (1, 1, 1)))
                else:
                    reciprocal = int(round(1/nilai))
                    baris.append(TFN_TABLE.get(reciprocal, (1, 1, 1)))
            else:
                baris.append((1, 1, 1))
        matriks_tfn.append(baris)

    # Step 2: Hitung Fuzzy Synthetic Extent (Si)
    # Si = jumlah baris TFN / jumlah total semua TFN
    jumlah_total_l = sum(matriks_tfn[i][j][0] for i in range(n_kriteria) for j in range(n_kriteria))
    jumlah_total_m = sum(matriks_tfn[i][j][1] for i in range(n_kriteria) for j in range(n_kriteria))
    jumlah_total_u = sum(matriks_tfn[i][j][2] for i in range(n_kriteria) for j in range(n_kriteria))

    Si = []
    for i in range(n_kriteria):
        jumlah_baris_l = sum(matriks_tfn[i][j][0] for j in range(n_kriteria))
        jumlah_baris_m = sum(matriks_tfn[i][j][1] for j in range(n_kriteria))
        jumlah_baris_u = sum(matriks_tfn[i][j][2] for j in range(n_kriteria))
        si_l = jumlah_baris_l / jumlah_total_u
        si_m = jumlah_baris_m / jumlah_total_m
        si_u = jumlah_baris_u / jumlah_total_l
        Si.append((round(si_l, 6), round(si_m, 6), round(si_u, 6)))

    # Step 3: Hitung Degree of Possibility V(Si >= Sj)
    def V(Si, Sj):
        """Hitung V(Si >= Sj)"""
        if Si[1] >= Sj[1]:
            return 1.0
        elif Sj[0] >= Si[2]:
            return 0.0
        else:
            # Formula Chang
            pembilang = Sj[0] - Si[2]
            pembagi = (Si[1] - Si[2]) - (Sj[1] - Sj[0])
            if pembagi == 0:
                return 0.0
            return round(pembilang / pembagi, 6)

    # Step 4: Hitung V(Si >= semua Sj) = min V(Si >= Sj) untuk j != i
    bobot_vektor = []
    for i in range(n_kriteria):
        v_min = min(V(Si[i], Si[j]) for j in range(n_kriteria) if j != i)
        bobot_vektor.append(round(v_min, 6))

    # Step 5: Normalisasi bobot vektor
    total = sum(bobot_vektor)
    if total == 0:
        bobot_normal = [1/n_kriteria] * n_kriteria
    else:
        bobot_normal = [round(b/total, 6) for b in bobot_vektor]

    return {
        'matriks_tfn': matriks_tfn,
        'Si': Si,
        'bobot_vektor': bobot_vektor,
        'bobot_normal': bobot_normal,
    }

def hitung_skor_komoditas(komoditas_list, bobot_normal, urutan_kriteria):
    """Hitung skor akhir komoditas berdasarkan bobot Fuzzy AHP"""
    hasil = []
    for k in komoditas_list:
        nilai = [
            k.produktivitas,
            k.luas_tanam,
            k.nilai_ekonomi,
            k.permintaan_pasar,
            k.kesesuaian_lahan
        ]
        # Normalisasi nilai komoditas
        skor = sum(nilai[i] * bobot_normal[i] for i in range(min(len(nilai), len(bobot_normal))))
        hasil.append({'komoditas': k, 'skor': round(skor, 4)})

    hasil.sort(key=lambda x: x['skor'], reverse=True)
    for i, h in enumerate(hasil):
        h['ranking'] = i + 1

    return hasil