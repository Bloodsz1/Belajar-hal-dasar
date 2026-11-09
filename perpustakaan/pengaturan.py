"""pengaturan.py - Pengaturan aplikasi yang bisa diubah dari halaman Pengaturan."""

import os

from models import DataRusakError
from penyimpanan import muat_json, simpan_json

BAWAAN = {
    "nama_perpustakaan": "Pustaka",
    "lama_pinjam_hari": 7,
    "denda_per_hari": 1000,
    "maks_pinjam_anggota": 3,
}


def _angka(teks, label, terkecil, terbesar):
    try:
        nilai = int(str(teks).strip())
    except ValueError:
        return None, f"{label} harus berupa angka."
    if not terkecil <= nilai <= terbesar:
        return None, f"{label} harus antara {terkecil} dan {terbesar}."
    return nilai, ""


def validasi_pengaturan(nama, lama, denda, maks):
    """Memeriksa isian formulir. Mengembalikan (data, pesan)."""
    nama = nama.strip()
    if not nama:
        return None, "Nama perpustakaan tidak boleh kosong."
    if len(nama) > 24:
        return None, "Nama perpustakaan maksimal 24 karakter."
    lama, pesan = _angka(lama, "Lama pinjam (hari)", 1, 90)
    if lama is None:
        return None, pesan
    denda, pesan = _angka(denda, "Denda per hari", 0, 1_000_000)
    if denda is None:
        return None, pesan
    maks, pesan = _angka(maks, "Batas pinjaman per anggota", 1, 20)
    if maks is None:
        return None, pesan
    return {"nama_perpustakaan": nama, "lama_pinjam_hari": lama,
            "denda_per_hari": denda, "maks_pinjam_anggota": maks}, ""


class Pengaturan:
    def __init__(self):
        self.nilai = dict(BAWAAN)

    def ambil(self, kunci):
        return self.nilai[kunci]

    def perbarui(self, data):
        for kunci in BAWAAN:
            if kunci in data:
                self.nilai[kunci] = data[kunci]

    def simpan(self, nama_file):
        simpan_json(nama_file, self.nilai)

    def muat(self, nama_file):
        data = muat_json(nama_file, None)
        if data is None:
            return
        nama = os.path.basename(str(nama_file))
        if not isinstance(data, dict):
            raise DataRusakError(f"Isi file '{nama}' tidak valid: harus berupa objek JSON.")
        baru = dict(BAWAAN)
        for kunci, bawaan in BAWAAN.items():
            if kunci in data:
                if type(data[kunci]) is not type(bawaan):
                    raise DataRusakError(f"Isi file '{nama}' tidak valid: pengaturan '{kunci}' salah jenis.")
                baru[kunci] = data[kunci]
        self.nilai = baru
