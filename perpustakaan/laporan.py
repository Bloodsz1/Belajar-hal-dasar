"""laporan.py - Perhitungan statistik dan ekspor CSV. Tanpa tampilan, jadi mudah diuji."""

import csv
import os
from collections import Counter
from datetime import date

from models import DAFTAR_SUBJEK
from util import BULAN, format_id, format_tanggal, samakan_subjek


def ringkasan(layanan, hari_ini=None):
    hari_ini = hari_ini or date.today()
    semua = layanan.riwayat.semua_peminjaman()
    aktif = layanan.riwayat.aktif()
    terlambat = [p for p in aktif if p.hari_terlambat(hari_ini) > 0]
    denda = layanan.pengaturan.ambil("denda_per_hari")
    return {
        "total_buku": len(layanan.perpus.semua_buku()),
        "total_anggota": len(layanan.anggota.semua_anggota()),
        "total_peminjaman": len(semua),
        "dipinjam": len(aktif),
        "terlambat": len(terlambat),
        "denda_berjalan": sum(p.denda(denda, hari_ini) for p in terlambat),
    }


def buku_per_subjek(layanan):
    """[('Fiksi', 3), ('Non-fiksi', 1)] dengan urutan sesuai DAFTAR_SUBJEK."""
    hitung = Counter(samakan_subjek(b.subjek) for b in layanan.perpus.semua_buku())
    hasil = [(s, hitung.get(s, 0)) for s in DAFTAR_SUBJEK]
    hasil += [(s, n) for s, n in hitung.items() if s not in DAFTAR_SUBJEK]
    return hasil


def _geser_bulan(tahun, bulan, selisih):
    indeks = tahun * 12 + (bulan - 1) + selisih
    return indeks // 12, indeks % 12 + 1


def peminjaman_per_bulan(layanan, jumlah=6, hari_ini=None):
    """Jumlah peminjaman tiap bulan, dari yang terlama ke bulan ini: [('Jun', 2), ...]."""
    hari_ini = hari_ini or date.today()
    hitung = Counter((p.tgl_pinjam.year, p.tgl_pinjam.month) for p in layanan.riwayat.semua_peminjaman())
    hasil = []
    for mundur in range(jumlah - 1, -1, -1):
        tahun, bulan = _geser_bulan(hari_ini.year, hari_ini.month, -mundur)
        hasil.append((BULAN[bulan - 1], hitung.get((tahun, bulan), 0)))
    return hasil


def buku_terpopuler(layanan, jumlah=5):
    hitung = Counter(p.id_buku for p in layanan.riwayat.semua_peminjaman())
    urut = sorted(hitung.items(), key=lambda x: (-x[1], layanan.judul_buku(x[0]).lower()))
    return [(layanan.judul_buku(i), n) for i, n in urut[:jumlah]]


def anggota_teraktif(layanan, jumlah=5):
    hitung = Counter(p.id_anggota for p in layanan.riwayat.semua_peminjaman())
    urut = sorted(hitung.items(), key=lambda x: (-x[1], layanan.nama_anggota(x[0]).lower()))
    return [(layanan.nama_anggota(i), n) for i, n in urut[:jumlah]]


def daftar_terlambat(layanan, hari_ini=None):
    """Peminjaman yang terlambat, dari yang paling lama."""
    hari_ini = hari_ini or date.today()
    return sorted(layanan.riwayat.terlambat(hari_ini), key=lambda p: -p.hari_terlambat(hari_ini))


# ------------------------------------------------------------------ ekspor CSV
def tabel_buku(layanan):
    kepala = ["ID", "Judul", "Penulis", "Subjek", "Tahun terbit", "Status"]
    baris = [[format_id(b.id), b.judul, b.penulis, samakan_subjek(b.subjek), b.tahun_terbit,
              layanan.status_buku(b.id)] for b in layanan.perpus.semua_buku()]
    return kepala, baris


def tabel_anggota(layanan):
    kepala = ["Kode", "Nama", "Email", "Telepon", "Bergabung", "Sedang dipinjam"]
    baris = [[a.kode, a.nama, a.email, a.telepon, a.bergabung, len(layanan.riwayat.aktif_milik(a.id))]
             for a in layanan.anggota.semua_anggota()]
    return kepala, baris


def tabel_peminjaman(layanan, hari_ini=None):
    hari_ini = hari_ini or date.today()
    denda = layanan.pengaturan.ambil("denda_per_hari")
    kepala = ["ID", "Buku", "Anggota", "Tanggal pinjam", "Jatuh tempo", "Tanggal kembali",
              "Status", "Hari terlambat", "Denda (Rp)"]
    baris = [[p.id, layanan.judul_buku(p.id_buku), layanan.nama_anggota(p.id_anggota),
              format_tanggal(p.tgl_pinjam), format_tanggal(p.jatuh_tempo), format_tanggal(p.tgl_kembali),
              p.status(hari_ini), p.hari_terlambat(hari_ini), p.denda(denda, hari_ini)]
             for p in layanan.riwayat.semua_peminjaman()]
    return kepala, baris


def ekspor_csv(jalur, kepala, baris):
    """Menulis CSV yang bisa dibuka langsung di Excel atau Numbers."""
    folder = os.path.dirname(str(jalur))
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(jalur, "w", newline="", encoding="utf-8-sig") as f:
        penulis = csv.writer(f)
        penulis.writerow(kepala)
        penulis.writerows(baris)
