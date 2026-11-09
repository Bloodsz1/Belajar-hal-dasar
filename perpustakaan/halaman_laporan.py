"""halaman_laporan.py - Laporan: statistik, grafik per bulan, peringkat, dan ekspor CSV."""

import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

import laporan
from halaman_beranda import kartu
from komponen import (DANGER, DANGER_SOFT, INK, MUTED, PRIMARY, PRIMARY_SOFT, SUCCESS, SURFACE, Halaman,
                      KartuStat, titik_bulat)
from util import format_rupiah

FOLDER_EKSPOR = "ekspor"


class HalamanLaporan(Halaman):
    def __init__(self, induk, app):
        super().__init__(induk, app)
        self.isi = self.kerangka(
            "Laporan", "Laporan", "Ekspor Peminjaman", lambda: self._ekspor("peminjaman"),
            tombol_lain=[("Ekspor Buku", lambda: self._ekspor("buku")),
                         ("Ekspor Anggota", lambda: self._ekspor("anggota"))],
            gulir=True)
        self.badan = tk.Frame(self.isi, bg=self["bg"])
        self.badan.pack(fill="both", expand=True, pady=(20, 0))

    def segarkan(self):
        for w in self.badan.winfo_children():
            w.destroy()
        f = self.f
        r = laporan.ringkasan(self.layanan)

        baris = tk.Frame(self.badan, bg=self["bg"])
        baris.pack(fill="x")
        data = [
            ("pinjam", "Total Peminjaman", r["total_peminjaman"], PRIMARY, PRIMARY_SOFT),
            ("buku", "Sedang Dipinjam", r["dipinjam"], "#F2994A", "#FEF1E4"),
            ("laporan", "Terlambat", r["terlambat"], DANGER, DANGER_SOFT),
            ("setelan", "Denda Berjalan", format_rupiah(r["denda_berjalan"]), SUCCESS, "#E6F6EF"),
        ]
        for i, (ikon, judul, nilai, warna, lembut) in enumerate(data):
            baris.columnconfigure(i, weight=1, uniform="stat")
            KartuStat(baris, self.app, ikon, judul, nilai, warna, lembut).grid(
                row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 8, 0 if i == 3 else 8))

        grafik = kartu(self.badan, f, "Peminjaman 6 Bulan Terakhir")
        grafik.pack(fill="x", pady=(20, 0))
        self._grafik(grafik.isi, laporan.peminjaman_per_bulan(self.layanan))

        bawah = tk.Frame(self.badan, bg=self["bg"])
        bawah.pack(fill="x", pady=(20, 0))
        for i in range(2):
            bawah.columnconfigure(i, weight=1, uniform="kol")
        populer = kartu(bawah, f, "Buku Terpopuler")
        populer.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self._peringkat(populer.isi, laporan.buku_terpopuler(self.layanan), "kali")
        aktif = kartu(bawah, f, "Anggota Teraktif")
        aktif.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self._peringkat(aktif.isi, laporan.anggota_teraktif(self.layanan), "pinjaman")

        lambat = kartu(self.badan, f, "Daftar Keterlambatan")
        lambat.pack(fill="x", pady=(20, 0))
        self._terlambat(lambat.isi)

    # ---------------------------------------------------------------- bagian
    def _grafik(self, induk, data):
        kanvas = tk.Canvas(induk, height=260, bg=SURFACE, highlightthickness=0, bd=0)
        kanvas.pack(fill="x")
        f = self.f

        def gambar(_e=None):
            kanvas.delete("all")
            lebar = max(kanvas.winfo_width(), 300)
            tinggi, bawah, atas = 260, 36, 24
            tertinggi = max([n for _, n in data] + [1])
            skala = max(tertinggi, 4)
            for k in range(5):  # garis bantu
                y = atas + (tinggi - bawah - atas) * k / 4
                kanvas.create_line(36, y, lebar, y, fill="#EFEBF7")
                kanvas.create_text(28, y, text=str(round(skala * (4 - k) / 4)), font=f.tiny,
                                   fill=MUTED, anchor="e")
            slot = (lebar - 48) / len(data)
            for i, (nama, n) in enumerate(data):
                tengah = 48 + slot * i + slot / 2
                tinggi_batang = (tinggi - bawah - atas) * n / skala
                y2 = tinggi - bawah
                if n:
                    kanvas.create_polygon(
                        titik_bulat(tengah - 18, y2 - max(tinggi_batang, 8), tengah + 18, y2, 6),
                        smooth=True, fill=PRIMARY, outline="")
                    kanvas.create_text(tengah, y2 - tinggi_batang - 10, text=str(n), font=f.small, fill=INK)
                kanvas.create_text(tengah, tinggi - 14, text=nama, font=f.small, fill=MUTED)
        kanvas.bind("<Configure>", gambar)

    def _peringkat(self, induk, data, satuan):
        if not data:
            tk.Label(induk, text="Belum ada data.", font=self.f.body, fg=MUTED, bg=SURFACE).pack(anchor="w")
            return
        for i, (nama, n) in enumerate(data, 1):
            baris = tk.Frame(induk, bg=SURFACE)
            baris.pack(fill="x", pady=5)
            tk.Label(baris, text=f"{i}", font=self.f.bold, fg=PRIMARY, bg=PRIMARY_SOFT, width=3).pack(side="left")
            tk.Label(baris, text=nama, font=self.f.body, fg=INK, bg=SURFACE).pack(side="left", padx=12)
            tk.Label(baris, text=f"{n} {satuan}", font=self.f.small, fg=MUTED, bg=SURFACE).pack(side="right")

    def _terlambat(self, induk):
        daftar = laporan.daftar_terlambat(self.layanan)
        if not daftar:
            tk.Label(induk, text="Tidak ada buku yang terlambat dikembalikan.", font=self.f.body,
                     fg=SUCCESS, bg=SURFACE).pack(anchor="w")
            return
        per_hari = self.layanan.pengaturan.ambil("denda_per_hari")
        for p in daftar:
            baris = tk.Frame(induk, bg=SURFACE)
            baris.pack(fill="x", pady=6)
            tk.Label(baris, text=self.layanan.judul_buku(p.id_buku), font=self.f.bold, fg=INK,
                     bg=SURFACE).pack(side="left")
            tk.Label(baris, text=f"  {self.layanan.nama_anggota(p.id_anggota)}", font=self.f.body,
                     fg=MUTED, bg=SURFACE).pack(side="left")
            tk.Label(baris, text=f"{p.hari_terlambat()} hari  ·  {format_rupiah(p.denda(per_hari))}",
                     font=self.f.bold, fg=DANGER, bg=SURFACE).pack(side="right")

    # ---------------------------------------------------------------- ekspor
    def _ekspor(self, jenis):
        tabel = {"buku": laporan.tabel_buku, "anggota": laporan.tabel_anggota,
                 "peminjaman": laporan.tabel_peminjaman}[jenis]
        kepala, baris = tabel(self.layanan)
        nama = f"{jenis}_{datetime.now():%Y%m%d_%H%M%S}.csv"
        jalur = os.path.join(self.layanan.folder, FOLDER_EKSPOR, nama)
        try:
            laporan.ekspor_csv(jalur, kepala, baris)
        except OSError as e:
            messagebox.showerror("Gagal mengekspor", f"File tidak dapat ditulis:\n{e}", parent=self.app.root)
            return
        self.app.toast(f"{len(baris)} baris diekspor ke {FOLDER_EKSPOR}/{nama}")
