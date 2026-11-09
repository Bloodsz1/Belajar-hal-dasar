"""gui.py - Kerangka aplikasi Pustaka: sidebar, kotak cari, dan pergantian halaman.

Jalankan file ini untuk membuka aplikasi:  python gui.py

Susunan file:
  models.py        backend buku (milikmu)            anggota.py     backend anggota
  peminjaman.py    backend peminjaman & denda        pengaturan.py  backend pengaturan
  layanan.py       menyatukan semua backend + aturan lintas data
  laporan.py       statistik & ekspor CSV            util.py, penyimpanan.py  fungsi bantu
  komponen.py      tombol, tabel, dialog (tampilan bersama)
  halaman_*.py     satu file untuk tiap menu di sidebar
Setiap halaman memberi tanda  # BACKEND:  di baris yang memanggil backend.
"""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from halaman_anggota import HalamanAnggota
from halaman_beranda import HalamanBeranda
from halaman_buku import HalamanBuku
from halaman_laporan import HalamanLaporan
from halaman_pengaturan import HalamanPengaturan
from halaman_peminjaman import HalamanPeminjaman
from komponen import (BG, BORDER, CURSOR, DARK, HEAD, INK, MUTED, PRIMARY, PRIMARY_SOFT, SURFACE, Gaya,
                      gambar_ikon, potong_teks, titik_bulat)
from layanan import Layanan
from models import DataRusakError

FOLDER_DATA = Path(__file__).resolve().parent

# (kunci halaman, nama ikon, label menu, kelas halaman)
MENU = [
    ("beranda", "beranda", "Beranda", HalamanBeranda),
    ("buku", "buku", "Perpustakaan", HalamanBuku),
    ("anggota", "anggota", "Anggota", HalamanAnggota),
    ("peminjaman", "pinjam", "Peminjaman", HalamanPeminjaman),
    ("laporan", "laporan", "Laporan", HalamanLaporan),
    ("pengaturan", "setelan", "Pengaturan", HalamanPengaturan),
]


class Aplikasi:
    def __init__(self, root, layanan):
        self.root = root
        self.layanan = layanan
        self.f = Gaya()
        self.aktif = None
        self.halaman = {}
        self._menu = {}
        self._after_cari = None
        self._after_toast = None
        self._abaikan_cari = False
        self._fokus_cari = False

        self._bangun_ui()
        self._pasang_pintasan()
        self.terapkan_pengaturan()
        self.tampil("beranda")

    # ------------------------------------------------------------------ UI
    def _bangun_ui(self):
        f = self.f
        self.root.configure(bg=BG)
        self.sidebar = tk.Frame(self.root, bg=SURFACE, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        tk.Frame(self.root, bg=BORDER, width=1).pack(side="left", fill="y")
        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        # Logo
        logo = tk.Frame(self.sidebar, bg=SURFACE, height=84)
        logo.pack(fill="x")
        logo.pack_propagate(False)
        ikon = tk.Canvas(logo, width=40, height=40, bg=SURFACE, highlightthickness=0, bd=0)
        ikon.place(x=24, y=22)
        ikon.create_polygon(titik_bulat(0, 0, 40, 40, 11), smooth=True, fill=PRIMARY, outline=PRIMARY)
        ikon.create_polygon(9, 13, 20, 16, 20, 31, 9, 28, fill="#FFFFFF", outline="")
        ikon.create_polygon(31, 13, 20, 16, 20, 31, 31, 28, fill="#DCCBFF", outline="")
        self.lbl_logo = tk.Label(logo, text="", font=f.logo, fg=PRIMARY, bg=SURFACE)
        self.lbl_logo.place(x=74, rely=0.5, anchor="w")

        tk.Label(self.sidebar, text="MENU", font=f.tiny, fg=MUTED, bg=SURFACE).pack(
            anchor="w", padx=28, pady=(14, 6))
        for kunci, ikon_menu, label, _kelas in MENU:
            kanvas = tk.Canvas(self.sidebar, width=196, height=44, bg=SURFACE, highlightthickness=0,
                               bd=0, cursor=CURSOR)
            kanvas.pack(padx=12, pady=2)
            self._menu[kunci] = (kanvas, ikon_menu, label)
            kanvas.bind("<Enter>", lambda e, k=kunci: self._gambar_menu(k, hover=True))
            kanvas.bind("<Leave>", lambda e, k=kunci: self._gambar_menu(k))
            kanvas.bind("<ButtonRelease-1>", lambda e, k=kunci: self.tampil(k))
            self._gambar_menu(kunci)

        self._bangun_topbar()
        self.isi = tk.Frame(self.main, bg=BG)
        self.isi.pack(fill="both", expand=True)
        self.lbl_toast = tk.Label(self.main, text="", font=f.body, fg="#FFFFFF", bg=DARK, padx=18, pady=10)

    def _gambar_menu(self, kunci, hover=False):
        kanvas, ikon, label = self._menu[kunci]
        aktif = kunci == self.aktif
        latar = PRIMARY_SOFT if aktif else (HEAD if hover else SURFACE)
        kanvas.delete("all")
        kanvas.create_polygon(titik_bulat(0, 0, 196, 44, 10), smooth=True, fill=latar, outline=latar)
        gambar_ikon(kanvas, ikon, 28, 22, PRIMARY if aktif else MUTED)
        kanvas.create_text(54, 22, text=label, anchor="w", fill=PRIMARY if aktif else INK,
                           font=self.f.bold if aktif else self.f.body)

    def _bangun_topbar(self):
        f = self.f
        atas = tk.Frame(self.main, bg=SURFACE, height=72)
        atas.pack(fill="x")
        atas.pack_propagate(False)
        tk.Frame(self.main, bg=BORDER, height=1).pack(fill="x")

        self.kotak_cari = tk.Frame(atas, bg=HEAD, width=400, height=42, highlightthickness=1,
                                   highlightbackground=BORDER, highlightcolor=PRIMARY)
        self.kotak_cari.pack(side="left", padx=32, pady=15)
        self.kotak_cari.pack_propagate(False)
        kaca = tk.Canvas(self.kotak_cari, width=38, height=40, bg=HEAD, highlightthickness=0, bd=0)
        kaca.pack(side="left")
        kaca.create_oval(12, 12, 24, 24, outline=MUTED, width=2)
        kaca.create_line(23, 23, 28, 28, fill=MUTED, width=2, capstyle="round")

        self.var_cari = tk.StringVar()
        self.ent_cari = tk.Entry(self.kotak_cari, textvariable=self.var_cari, font=f.body, bd=0,
                                 relief="flat", highlightthickness=0, bg=HEAD, fg=INK, insertbackground=INK)
        self.ent_cari.pack(side="left", fill="both", expand=True, padx=(0, 12), pady=8)
        self.hint = tk.Label(self.kotak_cari, text="", font=f.body, fg=MUTED, bg=HEAD, cursor="xterm")
        self.hint.place(x=40, rely=0.5, anchor="w")
        self.hint.bind("<Button-1>", lambda e: self.ent_cari.focus_set())
        self.ent_cari.bind("<FocusIn>", lambda e: self._fokus(True))
        self.ent_cari.bind("<FocusOut>", lambda e: self._fokus(False))
        self.var_cari.trace_add("write", self._saat_cari_berubah)

        pengguna = tk.Frame(atas, bg=SURFACE)
        pengguna.pack(side="right", padx=32)
        avatar = tk.Canvas(pengguna, width=40, height=40, bg=SURFACE, highlightthickness=0, bd=0)
        avatar.pack(side="left")
        avatar.create_oval(0, 0, 39, 39, fill=PRIMARY_SOFT, outline="")
        avatar.create_text(20, 20, text="A", font=f.bold, fill=PRIMARY)
        teks = tk.Frame(pengguna, bg=SURFACE)
        teks.pack(side="left", padx=(12, 0))
        tk.Label(teks, text="Admin", font=f.bold, fg=INK, bg=SURFACE).pack(anchor="w")
        tk.Label(teks, text="Pustakawan", font=f.tiny, fg=MUTED, bg=SURFACE).pack(anchor="w")

    def _pasang_pintasan(self):
        mod = "Command" if sys.platform == "darwin" else "Control"
        self.root.bind(f"<{mod}-n>", lambda e: self.aktif and self.halaman[self.aktif].tambah())
        self.root.bind(f"<{mod}-f>", lambda e: self.ent_cari.focus_set())

    # ------------------------------------------------------ pindah halaman
    def tampil(self, kunci):
        """Menampilkan satu halaman (dibuat saat pertama dibuka)."""
        if kunci not in self.halaman:
            kelas = next(k for kk, _i, _l, k in MENU if kk == kunci)
            self.halaman[kunci] = kelas(self.isi, self)
        lama, self.aktif = self.aktif, kunci
        if lama is not None and lama != kunci:
            self.halaman[lama].pack_forget()
            self._gambar_menu(lama)
        self._gambar_menu(kunci)

        halaman = self.halaman[kunci]
        halaman.pack(fill="both", expand=True)
        if halaman.placeholder:
            self.hint.configure(text=halaman.placeholder)
            if not self.kotak_cari.winfo_ismapped():
                self.kotak_cari.pack(side="left", padx=32, pady=15)
            self.set_cari(halaman.kata_kunci)
        else:
            self.kotak_cari.pack_forget()
        halaman.segarkan()

    def set_cari(self, teks):
        """Mengisi kotak cari dari program tanpa memicu pencarian."""
        self._abaikan_cari = True
        try:
            self.var_cari.set(teks)
        finally:
            self._abaikan_cari = False
        if self._after_cari is not None:
            self.root.after_cancel(self._after_cari)
            self._after_cari = None
        self._atur_hint()

    # --------------------------------------------------------------- cari
    def _fokus(self, aktif):
        self._fokus_cari = aktif
        self.kotak_cari.configure(highlightbackground=PRIMARY if aktif else BORDER)
        self._atur_hint()

    def _atur_hint(self):
        if self.var_cari.get() or self._fokus_cari:
            self.hint.place_forget()
        else:
            self.hint.place(x=40, rely=0.5, anchor="w")

    def _saat_cari_berubah(self, *_):
        self._atur_hint()
        if self._abaikan_cari:
            return
        teks = self.var_cari.get().strip()
        if self._after_cari is not None:
            self.root.after_cancel(self._after_cari)
        self._after_cari = self.root.after(180, lambda: self._terapkan_cari(teks))

    def _terapkan_cari(self, teks):
        self._after_cari = None
        if self.aktif is None:
            return
        halaman = self.halaman[self.aktif]
        if teks != halaman.kata_kunci:
            halaman.cari(teks)

    # ------------------------------------------------------------- bantuan
    def simpan(self, fungsi):
        """Menjalankan fungsi simpan dari Layanan. Kalau gagal, tampilkan pesan."""
        try:
            fungsi()
        except OSError as error:
            messagebox.showerror("Gagal menyimpan", f"Perubahan belum tersimpan ke file:\n{error}",
                                 parent=self.root)
            return False
        return True

    def terapkan_pengaturan(self):
        nama = self.layanan.pengaturan.ambil("nama_perpustakaan")
        self.lbl_logo.configure(text=potong_teks(nama, self.f.logo, 130))
        self.root.title(f"{nama} - Sistem Perpustakaan")

    def toast(self, teks):
        self.lbl_toast.configure(text=teks)
        self.lbl_toast.place(relx=0.5, rely=1.0, y=-28, anchor="s")
        self.lbl_toast.lift()
        if self._after_toast is not None:
            self.root.after_cancel(self._after_toast)
        self._after_toast = self.root.after(2800, self.lbl_toast.place_forget)


# --------------------------------------------------------------------------
def main():
    root = tk.Tk()
    root.title("Pustaka - Sistem Perpustakaan")

    layanan = Layanan(FOLDER_DATA)
    try:
        # BACKEND: muat_semua() membaca buku, anggota, peminjaman, dan pengaturan dari JSON
        layanan.muat_semua()
    except (DataRusakError, ValueError, TypeError, KeyError, OSError) as error:
        root.withdraw()
        messagebox.showerror(
            "Gagal membaca data",
            f"Salah satu file data tidak dapat dibaca:\n{error}\n\n"
            "Periksa isi file JSON tersebut, lalu buka aplikasi lagi.")
        root.destroy()
        return

    layar_w, layar_h = root.winfo_screenwidth(), root.winfo_screenheight()
    lebar = min(1360, layar_w - 80)
    tinggi = min(860, layar_h - 120)
    root.geometry(f"{lebar}x{tinggi}+{(layar_w - lebar) // 2}+{(layar_h - tinggi) // 3}")
    root.minsize(min(1240, lebar), min(640, tinggi))

    Aplikasi(root, layanan)

    try:  # bawa jendela ke depan (berguna di macOS)
        root.lift()
        root.attributes("-topmost", True)
        root.after(300, lambda: root.attributes("-topmost", False))
    except tk.TclError:
        pass
    root.mainloop()


if __name__ == "__main__":
    main()
