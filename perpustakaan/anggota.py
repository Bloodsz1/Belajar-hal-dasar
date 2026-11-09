"""anggota.py - Data anggota perpustakaan (pola sama seperti Buku dan Perpustakaan)."""

import os
import re
from datetime import date

from models import DataRusakError
from penyimpanan import muat_json, simpan_json


class Anggota:
    def __init__(self, id, nama, email="", telepon="", bergabung=None):
        self.id = id
        self.nama = nama
        self.email = email
        self.telepon = telepon
        self.bergabung = bergabung or date.today().isoformat()  # teks 'YYYY-MM-DD'

    @property
    def kode(self):
        """1 -> 'AG001'."""
        return f"AG{int(self.id):03d}"

    def __str__(self):
        return f"{self.nama} ({self.kode})"

    def ke_dict(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "email": self.email,
            "telepon": self.telepon,
            "bergabung": self.bergabung,
        }


class DaftarAnggota:
    def __init__(self):
        self.daftar_anggota = []

    def tambah_anggota(self, anggota):
        if self.cari_by_id(anggota.id) is not None:
            return False
        self.daftar_anggota.append(anggota)
        return True

    def semua_anggota(self):
        return self.daftar_anggota

    def cari_by_id(self, id):
        for anggota in self.daftar_anggota:
            if anggota.id == id:
                return anggota
        return None

    def cari_anggota(self, kata):
        """Mencari di nama, email, dan telepon (tidak peduli huruf besar-kecil)."""
        kata = kata.lower()
        return [a for a in self.daftar_anggota
                if kata in a.nama.lower() or kata in a.email.lower() or kata in a.telepon.lower()]

    def hapus_anggota(self, id):
        anggota = self.cari_by_id(id)
        if anggota is None:
            return False
        self.daftar_anggota.remove(anggota)
        return True

    def edit_anggota(self, id, nama=None, email=None, telepon=None):
        anggota = self.cari_by_id(id)
        if anggota is None:
            return False
        if nama is not None:
            anggota.nama = nama
        if email is not None:
            anggota.email = email
        if telepon is not None:
            anggota.telepon = telepon
        return True

    def id_berikutnya(self):
        if not self.daftar_anggota:
            return 1
        return max(a.id for a in self.daftar_anggota) + 1

    def simpan(self, nama_file):
        simpan_json(nama_file, [a.ke_dict() for a in self.daftar_anggota])

    def muat(self, nama_file):
        data = muat_json(nama_file, [])
        try:
            daftar = [Anggota(**d) for d in data]
        except (TypeError, KeyError, ValueError) as error:
            nama = os.path.basename(str(nama_file))
            raise DataRusakError(f"Isi file '{nama}' tidak valid: {error}") from error
        self.daftar_anggota = daftar


def validasi_anggota(nama, email, telepon):
    """Memeriksa isian formulir. Mengembalikan (data, pesan) seperti validasi_buku."""
    nama = nama.strip()
    email = email.strip()
    telepon = telepon.strip()
    if not nama:
        return None, "Nama anggota tidak boleh kosong."
    if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return None, "Format email tidak valid, contoh: nama@email.com."
    if telepon:
        jumlah_digit = sum(1 for c in telepon if c.isdigit())
        if jumlah_digit < 8 or any(c not in "0123456789+-() " for c in telepon):
            return None, "Nomor telepon tidak valid (minimal 8 angka)."
    return {"nama": nama, "email": email, "telepon": telepon}, ""
