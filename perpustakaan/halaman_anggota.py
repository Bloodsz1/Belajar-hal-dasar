"""halaman_anggota.py - Halaman Anggota: daftar anggota (tambah, edit, hapus, cari)."""

import tkinter as tk
from datetime import date
from tkinter import messagebox

from anggota import Anggota, validasi_anggota
from komponen import INK, MUTED, DialogForm, Halaman, TabelKartu, inisial, warna_avatar
from util import format_tanggal


def _tanggal(teks):
    try:
        return format_tanggal(date.fromisoformat(teks))
    except (TypeError, ValueError):
        return str(teks)


class HalamanAnggota(Halaman):
    placeholder = "Cari nama, email, atau telepon…"

    def __init__(self, induk, app):
        super().__init__(induk, app)
        self.daftar = self.layanan.anggota
        isi = self.kerangka("Anggota", "Daftar Anggota", "+   Tambah Anggota", self.tambah)
        kolom = [
            {"judul": "Nama", "lebar": 0, "sel": self._sel_nama},
            {"judul": "Kode", "lebar": 80, "teks": lambda a: a.kode, "warna": MUTED},
            {"judul": "Email", "lebar": 210, "teks": lambda a: a.email or "-"},
            {"judul": "Telepon", "lebar": 140, "teks": lambda a: a.telepon or "-"},
            {"judul": "Bergabung", "lebar": 110, "teks": lambda a: _tanggal(a.bergabung)},
            {"judul": "Dipinjam", "lebar": 90,
             "teks": lambda a: f"{len(self.layanan.riwayat.aktif_milik(a.id))} buku"},
        ]
        self.tabel = TabelKartu(
            isi, app, "Semua Anggota", kolom, self._data, lambda a: a.id,
            aksi=[("edit", self._edit), ("hapus", self._hapus)],
            hitung_semua=lambda: len(self.daftar.semua_anggota()), satuan="anggota",
            kosong=("Belum ada anggota", "Tambahkan anggota agar bisa meminjam buku."),
            tombol_kosong=("+   Tambah Anggota", self.tambah))
        self.tabel.pack(fill="both", expand=True, pady=(20, 0))

    def _data(self):
        if self.kata_kunci:
            return self.daftar.cari_anggota(self.kata_kunci)
        return list(self.daftar.semua_anggota())

    def _sel_nama(self, sel, anggota, bg):
        avatar = tk.Canvas(sel, width=36, height=36, bg=bg, highlightthickness=0, bd=0)
        avatar.place(x=6, rely=0.5, anchor="w")
        avatar.create_oval(0, 0, 35, 35, fill=warna_avatar(anggota.id), outline="")
        avatar.create_text(18, 18, text=inisial(anggota.nama), font=self.f.bold, fill="#FFFFFF")
        tk.Label(sel, text=anggota.nama, font=self.f.bold, fg=INK, bg=bg).place(x=54, rely=0.5, anchor="w")

    def segarkan(self):
        self.tabel.render()

    def cari(self, teks):
        self.kata_kunci = teks
        self.tabel.reset()

    # ------------------------------------------------------------ formulir
    @staticmethod
    def _medan(awal=None):
        awal = awal or {}
        return [
            {"kunci": "nama", "label": "Nama lengkap", "nilai": awal.get("nama", "")},
            {"kunci": "email", "label": "Email (opsional)", "nilai": awal.get("email", "")},
            {"kunci": "telepon", "label": "Telepon (opsional)", "nilai": awal.get("telepon", "")},
        ]

    @staticmethod
    def _validasi(v):
        return validasi_anggota(v["nama"], v["email"], v["telepon"])

    def tambah(self):
        DialogForm(self.app, "Tambah Anggota", self._medan(), self._validasi, self._simpan_baru,
                   keterangan="Kode anggota dibuat otomatis.")

    def _edit(self, anggota):
        awal = {"nama": anggota.nama, "email": anggota.email, "telepon": anggota.telepon}
        DialogForm(self.app, "Edit Anggota", self._medan(awal), self._validasi,
                   lambda data: self._simpan_edit(anggota.id, data),
                   keterangan=f"Kode {anggota.kode} tidak dapat diubah.")

    # --------------------------------------------------------------- aksi
    def _simpan_baru(self, data):
        anggota = Anggota(self.daftar.id_berikutnya(), data["nama"], data["email"], data["telepon"])
        if not self.daftar.tambah_anggota(anggota):
            return False, "ID anggota sudah dipakai."
        self.app.simpan(self.layanan.simpan_anggota)
        self.kata_kunci = ""
        self.app.set_cari("")
        self.tabel.ke_akhir()
        self.app.toast(f"{anggota.nama} ({anggota.kode}) berhasil ditambahkan.")
        return True, ""

    def _simpan_edit(self, id_anggota, data):
        if not self.daftar.edit_anggota(id_anggota, nama=data["nama"], email=data["email"],
                                        telepon=data["telepon"]):
            return False, "Anggota tidak ditemukan."
        self.app.simpan(self.layanan.simpan_anggota)
        self.tabel.render()
        self.app.toast("Perubahan berhasil disimpan.")
        return True, ""

    def _hapus(self, anggota):
        boleh, pesan = self.layanan.bisa_hapus_anggota(anggota.id)
        if not boleh:
            messagebox.showinfo("Anggota tidak bisa dihapus", pesan, parent=self.app.root)
            return
        if messagebox.askyesno("Hapus anggota",
                               f"Hapus anggota “{anggota.nama}”?\nRiwayat peminjamannya tetap tersimpan.",
                               icon="warning", parent=self.app.root):
            self.daftar.hapus_anggota(anggota.id)
            self.app.simpan(self.layanan.simpan_anggota)
            self.tabel.render()
            self.app.toast(f"Anggota {anggota.nama} dihapus.")
