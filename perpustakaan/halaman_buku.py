"""halaman_buku.py - Halaman Perpustakaan: daftar buku (tambah, edit, hapus, cari, filter)."""

import tkinter as tk
from datetime import date
from tkinter import messagebox

from komponen import (INK, DialogForm, Halaman, Lencana, TabelKartu, inisial, warna_avatar)
from models import DAFTAR_SUBJEK, Buku
from util import format_id, samakan_subjek

SEMUA_SUBJEK = "Semua subjek"


def validasi_buku(judul, penulis, subjek, tahun_teks):
    """Memeriksa isian formulir.

    Mengembalikan (data, pesan). Kalau valid, data berupa dict dan pesan kosong.
    Kalau tidak valid, data = None dan pesan berisi alasannya.
    """
    judul = judul.strip()
    penulis = penulis.strip()
    subjek = samakan_subjek(subjek)
    tahun_teks = tahun_teks.strip()

    if not judul:
        return None, "Judul buku tidak boleh kosong."
    if not penulis:
        return None, "Nama penulis tidak boleh kosong."
    if subjek not in DAFTAR_SUBJEK:
        return None, "Pilih subjek: " + " atau ".join(DAFTAR_SUBJEK) + "."
    try:
        tahun = int(tahun_teks)
    except ValueError:
        return None, "Tahun terbit harus berupa angka."
    tahun_maks = date.today().year + 1
    if not 1000 <= tahun <= tahun_maks:
        return None, f"Tahun terbit harus antara 1000 dan {tahun_maks}."
    return {"judul": judul, "penulis": penulis, "subjek": subjek, "tahun_terbit": tahun}, ""


class HalamanBuku(Halaman):
    placeholder = "Cari judul buku…"

    def __init__(self, induk, app):
        super().__init__(induk, app)
        self.perpus = self.layanan.perpus
        self.filter_subjek = SEMUA_SUBJEK
        isi = self.kerangka("Perpustakaan", "Daftar Buku", "+   Tambah Buku", self.tambah)
        kolom = [
            {"judul": "Nama Buku", "lebar": 0, "sel": self._sel_judul},
            {"judul": "Penulis", "lebar": 150, "teks": lambda b: b.penulis},
            {"judul": "ID", "lebar": 80, "teks": lambda b: format_id(b.id), "warna": "#8A85A0"},
            {"judul": "Subjek", "lebar": 110, "teks": lambda b: samakan_subjek(b.subjek)},
            {"judul": "Tahun", "lebar": 80, "teks": lambda b: b.tahun_terbit},
            {"judul": "Status", "lebar": 130, "sel": self._sel_status},
        ]
        self.tabel = TabelKartu(
            isi, app, "Semua Buku", kolom, self._data, lambda b: b.id,
            aksi=[("edit", self._edit), ("hapus", self._hapus)],
            saat_hapus_massal=self._hapus_massal,
            opsi_filter=[SEMUA_SUBJEK] + list(DAFTAR_SUBJEK), saat_filter=self._saat_filter,
            hitung_semua=lambda: len(self.perpus.semua_buku()), satuan="buku",
            kosong=("Belum ada buku", "Tambahkan buku pertama untuk mulai mengisi perpustakaan."),
            tombol_kosong=("+   Tambah Buku", self.tambah))
        self.tabel.pack(fill="both", expand=True, pady=(20, 0))

    # ------------------------------------------------------------------ data
    def _data(self):
        # BACKEND: cari_by_judul() untuk pencarian, semua_buku() untuk daftar lengkap
        if self.kata_kunci:
            sumber = self.perpus.cari_by_judul(self.kata_kunci)
        else:
            sumber = list(self.perpus.semua_buku())
        if self.filter_subjek != SEMUA_SUBJEK:
            sumber = [b for b in sumber if samakan_subjek(b.subjek) == self.filter_subjek]
        return sumber

    def _sel_judul(self, sel, buku, bg):
        avatar = tk.Canvas(sel, width=36, height=36, bg=bg, highlightthickness=0, bd=0)
        avatar.place(x=6, rely=0.5, anchor="w")
        avatar.create_oval(0, 0, 35, 35, fill=warna_avatar(buku.id), outline="")
        avatar.create_text(18, 18, text=inisial(buku.judul), font=self.f.bold, fill="#FFFFFF")
        tk.Label(sel, text=buku.judul, font=self.f.bold, fg=INK, bg=bg).place(x=54, rely=0.5, anchor="w")

    def _sel_status(self, sel, buku, bg):
        Lencana(sel, self.layanan.status_buku(buku.id), self.f.small, bg).place(x=6, rely=0.5, anchor="w")

    # ----------------------------------------------------- dari kerangka aplikasi
    def segarkan(self):
        self.tabel.render()

    def cari(self, teks):
        self.kata_kunci = teks
        self.tabel.reset()

    def _saat_filter(self, nilai):
        self.filter_subjek = nilai

    # ------------------------------------------------------------ formulir
    def _medan(self, awal=None):
        awal = awal or {}
        return [
            {"kunci": "judul", "label": "Judul buku", "nilai": awal.get("judul", "")},
            {"kunci": "penulis", "label": "Penulis", "nilai": awal.get("penulis", "")},
            {"kunci": "subjek", "label": "Subjek", "jenis": "pilihan", "pilihan": list(DAFTAR_SUBJEK),
             "nilai": samakan_subjek(awal.get("subjek") or DAFTAR_SUBJEK[0])},
            {"kunci": "tahun", "label": "Tahun terbit", "nilai": awal.get("tahun_terbit", "")},
        ]

    @staticmethod
    def _validasi(v):
        return validasi_buku(v["judul"], v["penulis"], v["subjek"], v["tahun"])

    def tambah(self):
        DialogForm(self.app, "Tambah Buku", self._medan(), self._validasi, self._simpan_baru,
                   keterangan="ID buku dibuat otomatis.")

    def _edit(self, buku):
        awal = {"judul": buku.judul, "penulis": buku.penulis, "subjek": buku.subjek,
                "tahun_terbit": buku.tahun_terbit}
        DialogForm(self.app, "Edit Buku", self._medan(awal), self._validasi,
                   lambda data: self._simpan_edit(buku.id, data),
                   keterangan=f"ID {format_id(buku.id)} tidak dapat diubah.")

    # --------------------------------------------------------------- aksi
    def _simpan_baru(self, data):
        # BACKEND: id_berikutnya() membuat id otomatis, tambah_buku() menolak id ganda
        buku = Buku(self.perpus.id_berikutnya(), data["judul"], data["penulis"],
                    data["subjek"], data["tahun_terbit"])
        if not self.perpus.tambah_buku(buku):
            return False, "ID buku sudah dipakai."
        self.app.simpan(self.layanan.simpan_buku)
        # Tampilkan buku baru: bersihkan pencarian dan filter, lompat ke halaman terakhir.
        self.kata_kunci = ""
        self.app.set_cari("")
        self.filter_subjek = SEMUA_SUBJEK
        self.tabel.atur_filter(SEMUA_SUBJEK)
        self.tabel.bersihkan_pilihan()
        self.tabel.ke_akhir()
        self.app.toast(f"Buku “{buku.judul}” berhasil ditambahkan.")
        return True, ""

    def _simpan_edit(self, id_buku, data):
        # BACKEND: edit_buku(id, ...) hanya mengubah field yang diberikan
        if not self.perpus.edit_buku(id_buku, judul=data["judul"], penulis=data["penulis"],
                                     subjek=data["subjek"], tahun_terbit=data["tahun_terbit"]):
            return False, "Buku tidak ditemukan."
        self.app.simpan(self.layanan.simpan_buku)
        self.tabel.render()
        self.app.toast("Perubahan berhasil disimpan.")
        return True, ""

    def _hapus(self, buku):
        boleh, pesan = self.layanan.bisa_hapus_buku(buku.id)
        if not boleh:
            messagebox.showinfo("Buku tidak bisa dihapus", pesan, parent=self.app.root)
            return
        if messagebox.askyesno("Hapus buku", f"Hapus “{buku.judul}”?\nTindakan ini tidak dapat dibatalkan.",
                               icon="warning", parent=self.app.root):
            self._hapus_ids([buku.id])

    def _hapus_massal(self, daftar_id):
        n = len(daftar_id)
        if messagebox.askyesno("Hapus buku", f"Hapus {n} buku yang dipilih?\nTindakan ini tidak dapat dibatalkan.",
                               icon="warning", parent=self.app.root):
            self._hapus_ids(daftar_id)

    def _hapus_ids(self, daftar_id):
        dihapus = dilewati = 0
        for i in daftar_id:
            if not self.layanan.bisa_hapus_buku(i)[0]:
                dilewati += 1
            elif self.perpus.hapus_buku(i):  # BACKEND: hapus_buku(id)
                dihapus += 1
        self.tabel.bersihkan_pilihan()
        self.app.simpan(self.layanan.simpan_buku)
        self.tabel.render()
        pesan = f"{dihapus} buku dihapus."
        if dilewati:
            pesan += f" {dilewati} dilewati karena sedang dipinjam."
        self.app.toast(pesan)
