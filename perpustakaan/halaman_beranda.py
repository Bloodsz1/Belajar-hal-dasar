"""halaman_beranda.py - Beranda: ringkasan angka, peminjaman terbaru, sebaran subjek, keterlambatan."""

import tkinter as tk
from datetime import date, datetime

from komponen import (BORDER, DANGER, DANGER_SOFT, INK, MUTED, PRIMARY, PRIMARY_SOFT, SUCCESS,
                      SUCCESS_SOFT, SURFACE, Halaman, KartuStat, Lencana, TombolBulat, titik_bulat)
import laporan
from util import HARI, format_rupiah, format_tanggal


def sapaan(jam):
    if jam < 11:
        return "Selamat pagi"
    if jam < 15:
        return "Selamat siang"
    if jam < 18:
        return "Selamat sore"
    return "Selamat malam"


class Kartu(tk.Frame):
    """Kartu putih dengan judul. Isinya ditaruh di atribut `isi`."""

    def __init__(self, induk, f, judul):
        super().__init__(induk, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER)
        tk.Label(self, text=judul, font=f.h2, fg=INK, bg=SURFACE).pack(anchor="w", padx=24, pady=(20, 8))
        self.isi = tk.Frame(self, bg=SURFACE)
        self.isi.pack(fill="both", expand=True, padx=24, pady=(0, 20))


def kartu(induk, f, judul):
    return Kartu(induk, f, judul)


class HalamanBeranda(Halaman):
    def __init__(self, induk, app):
        super().__init__(induk, app)
        self.isi = self.kerangka("Beranda", "Beranda", "+   Pinjam Buku", lambda: app.tampil("peminjaman"),
                                 gulir=True)
        self.badan = tk.Frame(self.isi, bg=self["bg"])
        self.badan.pack(fill="both", expand=True, pady=(20, 0))

    def segarkan(self):
        for w in self.badan.winfo_children():
            w.destroy()
        f = self.f
        r = laporan.ringkasan(self.layanan)
        hari = date.today()

        tk.Label(self.badan, text=f"{sapaan(datetime.now().hour)}, "
                 f"selamat datang di {self.layanan.pengaturan.ambil('nama_perpustakaan')}",
                 font=f.h2, fg=INK, bg=self["bg"]).pack(anchor="w")
        tk.Label(self.badan, text=f"{HARI[hari.weekday()]}, {format_tanggal(hari)}",
                 font=f.body, fg=MUTED, bg=self["bg"]).pack(anchor="w", pady=(2, 16))

        # Empat kartu angka (grid + uniform supaya lebarnya sama)
        baris = tk.Frame(self.badan, bg=self["bg"])
        baris.pack(fill="x")
        data = [
            ("buku", "Total Buku", r["total_buku"], PRIMARY, PRIMARY_SOFT),
            ("anggota", "Anggota", r["total_anggota"], "#2F80ED", "#E8F1FD"),
            ("pinjam", "Sedang Dipinjam", r["dipinjam"], "#F2994A", "#FEF1E4"),
            ("laporan", "Terlambat", r["terlambat"], DANGER, DANGER_SOFT),
        ]
        for i, (ikon, judul, nilai, warna, lembut) in enumerate(data):
            baris.columnconfigure(i, weight=1, uniform="stat")
            KartuStat(baris, self.app, ikon, judul, nilai, warna, lembut).grid(
                row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 8, 0 if i == 3 else 8))

        # Dua kolom: peminjaman terbaru | sebaran subjek + terlambat
        bawah = tk.Frame(self.badan, bg=self["bg"])
        bawah.pack(fill="both", expand=True, pady=(20, 0))
        bawah.columnconfigure(0, weight=3, uniform="kol")
        bawah.columnconfigure(1, weight=2, uniform="kol")

        kiri = kartu(bawah, f, "Peminjaman Terbaru")
        kiri.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self._terbaru(kiri.isi)

        kanan = tk.Frame(bawah, bg=self["bg"])
        kanan.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        k_subjek = kartu(kanan, f, "Buku per Subjek")
        k_subjek.pack(fill="x")
        self._subjek(k_subjek.isi)
        k_lambat = kartu(kanan, f, "Perlu Ditagih")
        k_lambat.pack(fill="x", pady=(20, 0))
        self._terlambat(k_lambat.isi, r["denda_berjalan"])

    def _kosong(self, induk, teks):
        tk.Label(induk, text=teks, font=self.f.body, fg=MUTED, bg=SURFACE).pack(anchor="w", pady=8)

    def _terbaru(self, induk):
        daftar = sorted(self.layanan.riwayat.semua_peminjaman(), key=lambda p: p.id, reverse=True)[:6]
        if not daftar:
            self._kosong(induk, "Belum ada peminjaman.")
            return
        for p in daftar:
            baris = tk.Frame(induk, bg=SURFACE)
            baris.pack(fill="x", pady=7)
            teks = tk.Frame(baris, bg=SURFACE)
            teks.pack(side="left")
            tk.Label(teks, text=self.layanan.judul_buku(p.id_buku), font=self.f.bold, fg=INK,
                     bg=SURFACE).pack(anchor="w")
            tk.Label(teks, text=f"{self.layanan.nama_anggota(p.id_anggota)}  ·  {format_tanggal(p.tgl_pinjam)}",
                     font=self.f.small, fg=MUTED, bg=SURFACE).pack(anchor="w")
            Lencana(baris, p.status(), self.f.small, SURFACE).pack(side="right")
        TombolBulat(induk, "Lihat semua", command=lambda: self.app.tampil("peminjaman"),
                    font=self.f.small, tinggi=34, radius=8, bg=PRIMARY_SOFT, fg=PRIMARY,
                    hover="#E4D9FB", latar=SURFACE).pack(anchor="w", pady=(10, 0))

    def _subjek(self, induk):
        data = laporan.buku_per_subjek(self.layanan)
        total = sum(n for _, n in data)
        if not total:
            self._kosong(induk, "Belum ada buku.")
            return
        warna = [PRIMARY, "#2F80ED", "#F2994A", SUCCESS]
        for i, (nama, n) in enumerate(data):
            tk.Label(induk, text=f"{nama}  ·  {n} buku", font=self.f.small, fg=INK,
                     bg=SURFACE).pack(anchor="w", pady=(8 if i else 0, 4))
            batang = tk.Canvas(induk, height=10, bg=SURFACE, highlightthickness=0, bd=0)
            batang.pack(fill="x")
            persen = n / total
            isi_warna = warna[i % len(warna)]

            def gambar(_e=None, b=batang, p=persen, w=isi_warna):
                lebar = max(b.winfo_width(), 20)
                b.delete("all")
                b.create_polygon(titik_bulat(0, 0, lebar - 1, 9, 4), smooth=True, fill="#EFEBF7", outline="")
                if p > 0:
                    b.create_polygon(titik_bulat(0, 0, max(lebar * p, 10), 9, 4), smooth=True, fill=w, outline="")
            batang.bind("<Configure>", gambar)

    def _terlambat(self, induk, denda):
        daftar = laporan.daftar_terlambat(self.layanan)
        if not daftar:
            tk.Label(induk, text="Tidak ada keterlambatan. Bagus!", font=self.f.body, fg=SUCCESS,
                     bg=SUCCESS_SOFT).pack(fill="x", ipady=10)
            return
        for p in daftar[:4]:
            baris = tk.Frame(induk, bg=SURFACE)
            baris.pack(fill="x", pady=5)
            tk.Label(baris, text=self.layanan.judul_buku(p.id_buku), font=self.f.bold, fg=INK,
                     bg=SURFACE).pack(anchor="w")
            tk.Label(baris, text=f"{self.layanan.nama_anggota(p.id_anggota)}  ·  terlambat {p.hari_terlambat()} hari",
                     font=self.f.small, fg=DANGER, bg=SURFACE).pack(anchor="w")
        tk.Label(induk, text=f"Denda berjalan: {format_rupiah(denda)}", font=self.f.bold, fg=INK,
                 bg=SURFACE).pack(anchor="w", pady=(10, 0))

