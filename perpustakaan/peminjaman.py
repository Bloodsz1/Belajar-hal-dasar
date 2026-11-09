"""peminjaman.py - Catatan peminjaman buku, jatuh tempo, keterlambatan, dan denda."""

import os
from datetime import date, timedelta

from models import DataRusakError
from penyimpanan import muat_json, simpan_json


def ke_tanggal(nilai):
    """Teks 'YYYY-MM-DD' -> date. None dan date dibiarkan."""
    if nilai is None or isinstance(nilai, date):
        return nilai
    return date.fromisoformat(nilai)


class Peminjaman:
    def __init__(self, id, id_buku, id_anggota, tgl_pinjam, jatuh_tempo, tgl_kembali=None):
        self.id = id
        self.id_buku = id_buku
        self.id_anggota = id_anggota
        self.tgl_pinjam = ke_tanggal(tgl_pinjam)
        self.jatuh_tempo = ke_tanggal(jatuh_tempo)
        self.tgl_kembali = ke_tanggal(tgl_kembali)

    def sudah_kembali(self):
        return self.tgl_kembali is not None

    def hari_terlambat(self, hari_ini=None):
        """Jumlah hari lewat jatuh tempo. Kalau sudah kembali, dihitung sampai tgl_kembali."""
        akhir = self.tgl_kembali or hari_ini or date.today()
        return max(0, (akhir - self.jatuh_tempo).days)

    def status(self, hari_ini=None):
        if self.sudah_kembali():
            return "Dikembalikan"
        return "Terlambat" if self.hari_terlambat(hari_ini) > 0 else "Dipinjam"

    def denda(self, denda_per_hari, hari_ini=None):
        return self.hari_terlambat(hari_ini) * denda_per_hari

    def ke_dict(self):
        return {
            "id": self.id,
            "id_buku": self.id_buku,
            "id_anggota": self.id_anggota,
            "tgl_pinjam": self.tgl_pinjam.isoformat(),
            "jatuh_tempo": self.jatuh_tempo.isoformat(),
            "tgl_kembali": self.tgl_kembali.isoformat() if self.tgl_kembali else None,
        }


class RiwayatPeminjaman:
    def __init__(self):
        self.daftar_peminjaman = []

    def semua_peminjaman(self):
        return self.daftar_peminjaman

    def cari_by_id(self, id):
        for p in self.daftar_peminjaman:
            if p.id == id:
                return p
        return None

    def id_berikutnya(self):
        if not self.daftar_peminjaman:
            return 1
        return max(p.id for p in self.daftar_peminjaman) + 1

    def aktif(self):
        """Peminjaman yang bukunya belum dikembalikan."""
        return [p for p in self.daftar_peminjaman if not p.sudah_kembali()]

    def buku_sedang_dipinjam(self, id_buku):
        return any(p.id_buku == id_buku for p in self.aktif())

    def aktif_milik(self, id_anggota):
        return [p for p in self.aktif() if p.id_anggota == id_anggota]

    def terlambat(self, hari_ini=None):
        return [p for p in self.aktif() if p.hari_terlambat(hari_ini) > 0]

    def pinjam(self, id_buku, id_anggota, lama_hari, tgl_pinjam=None):
        """Mencatat peminjaman baru. Mengembalikan None kalau buku masih dipinjam orang lain."""
        if self.buku_sedang_dipinjam(id_buku):
            return None
        tgl = tgl_pinjam or date.today()
        p = Peminjaman(self.id_berikutnya(), id_buku, id_anggota, tgl, tgl + timedelta(days=lama_hari))
        self.daftar_peminjaman.append(p)
        return p

    def kembalikan(self, id_peminjaman, tgl_kembali=None):
        p = self.cari_by_id(id_peminjaman)
        if p is None or p.sudah_kembali():
            return False
        p.tgl_kembali = tgl_kembali or date.today()
        return True

    def simpan(self, nama_file):
        simpan_json(nama_file, [p.ke_dict() for p in self.daftar_peminjaman])

    def muat(self, nama_file):
        data = muat_json(nama_file, [])
        try:
            daftar = [Peminjaman(**d) for d in data]
        except (TypeError, KeyError, ValueError) as error:
            nama = os.path.basename(str(nama_file))
            raise DataRusakError(f"Isi file '{nama}' tidak valid: {error}") from error
        self.daftar_peminjaman = daftar
