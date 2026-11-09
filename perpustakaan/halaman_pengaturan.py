"""halaman_pengaturan.py - Pengaturan: nama perpustakaan, aturan pinjam, denda, dan cadangan data."""

import os
import shutil
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from komponen import (BORDER, DANGER, INK, MUTED, SUCCESS, SURFACE, Halaman, TombolBulat, kolom_teks,
                      tombol_garis)
from layanan import SEMUA_FILE
from pengaturan import validasi_pengaturan

FOLDER_CADANGAN = "cadangan"


class HalamanPengaturan(Halaman):
    def __init__(self, induk, app):
        super().__init__(induk, app)
        self.isi = self.kerangka("Pengaturan", "Pengaturan", gulir=True)
        self.badan = tk.Frame(self.isi, bg=self["bg"])
        self.badan.pack(fill="both", expand=True, pady=(20, 0))
        self.vars = {}
        self._bangun()

    def _bagian(self, judul, keterangan):
        luar = tk.Frame(self.badan, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER)
        luar.pack(fill="x", pady=(0, 20))
        tk.Label(luar, text=judul, font=self.f.h2, fg=INK, bg=SURFACE).pack(anchor="w", padx=28, pady=(22, 2))
        tk.Label(luar, text=keterangan, font=self.f.small, fg=MUTED, bg=SURFACE).pack(anchor="w", padx=28)
        isi = tk.Frame(luar, bg=SURFACE)
        isi.pack(fill="x", padx=28, pady=(8, 24))
        return isi

    def _isian(self, induk, kunci, label, bantuan):
        tk.Label(induk, text=label, font=self.f.small, fg=MUTED, bg=SURFACE).pack(anchor="w", pady=(14, 4))
        var = tk.StringVar()
        self.vars[kunci] = var
        kolom_teks(induk, self.f, var)
        tk.Label(induk, text=bantuan, font=self.f.tiny, fg=MUTED, bg=SURFACE).pack(anchor="w", pady=(3, 0))

    def _bangun(self):
        f = self.f
        umum = self._bagian("Umum & Aturan Peminjaman", "Berlaku untuk peminjaman berikutnya.")
        self._isian(umum, "nama", "Nama perpustakaan", "Tampil di pojok kiri atas dan judul jendela (maks 24 huruf).")
        self._isian(umum, "lama", "Lama pinjam bawaan (hari)", "Dipakai sebagai isian awal saat meminjamkan buku (1–90).")
        self._isian(umum, "denda", "Denda per hari terlambat (Rp)", "Isi 0 kalau tidak ada denda (0–1.000.000).")
        self._isian(umum, "maks", "Maksimal buku per anggota", "Anggota tidak bisa meminjam lagi bila sudah mencapai batas (1–20).")
        self.lbl_pesan = tk.Label(umum, text="", font=f.small, fg=DANGER, bg=SURFACE)
        self.lbl_pesan.pack(anchor="w", pady=(14, 0))
        tombol = tk.Frame(umum, bg=SURFACE)
        tombol.pack(anchor="w", pady=(12, 0))
        TombolBulat(tombol, "Simpan Pengaturan", command=self._simpan, font=f.bold, tinggi=44,
                    latar=SURFACE).pack(side="left")
        tombol_garis(tombol, "Kembalikan Bawaan", self._bawaan, f.bold, SURFACE).pack(side="left", padx=(10, 0))

        cadang = self._bagian("Cadangan Data",
                              f"Menyalin semua file data ke folder “{FOLDER_CADANGAN}” di samping program.")
        TombolBulat(cadang, "Buat Cadangan Sekarang", command=self._cadangkan, font=f.bold, tinggi=44,
                    latar=SURFACE).pack(anchor="w", pady=(10, 0))
        self.lbl_cadang = tk.Label(cadang, text="", font=f.small, fg=SUCCESS, bg=SURFACE)
        self.lbl_cadang.pack(anchor="w", pady=(10, 0))

    def segarkan(self):
        a = self.layanan.pengaturan
        self.vars["nama"].set(a.ambil("nama_perpustakaan"))
        self.vars["lama"].set(str(a.ambil("lama_pinjam_hari")))
        self.vars["denda"].set(str(a.ambil("denda_per_hari")))
        self.vars["maks"].set(str(a.ambil("maks_pinjam_anggota")))
        self.lbl_pesan.configure(text="")

    def _simpan(self):
        data, pesan = validasi_pengaturan(self.vars["nama"].get(), self.vars["lama"].get(),
                                          self.vars["denda"].get(), self.vars["maks"].get())
        if data is None:
            self.lbl_pesan.configure(text=pesan)
            return
        self.layanan.pengaturan.perbarui(data)  # BACKEND: Pengaturan.perbarui()
        self.app.simpan(self.layanan.simpan_pengaturan)
        self.app.terapkan_pengaturan()
        self.segarkan()
        self.app.toast("Pengaturan disimpan.")

    def _bawaan(self):
        if messagebox.askyesno("Kembalikan bawaan", "Kembalikan semua pengaturan ke nilai awal?",
                               parent=self.app.root):
            from pengaturan import BAWAAN
            self.layanan.pengaturan.perbarui(dict(BAWAAN))
            self.app.simpan(self.layanan.simpan_pengaturan)
            self.app.terapkan_pengaturan()
            self.segarkan()
            self.app.toast("Pengaturan dikembalikan ke bawaan.")

    def _cadangkan(self):
        tujuan = os.path.join(self.layanan.folder, FOLDER_CADANGAN, f"{datetime.now():%Y%m%d_%H%M%S}")
        try:
            os.makedirs(tujuan, exist_ok=True)
            jumlah = 0
            for nama in SEMUA_FILE:
                sumber = self.layanan.jalur(nama)
                if os.path.exists(sumber):
                    shutil.copy2(sumber, tujuan)
                    jumlah += 1
        except OSError as e:
            messagebox.showerror("Gagal mencadangkan", str(e), parent=self.app.root)
            return
        self.lbl_cadang.configure(text=f"{jumlah} file dicadangkan ke {FOLDER_CADANGAN}/{os.path.basename(tujuan)}")
        self.app.toast("Cadangan berhasil dibuat.")
