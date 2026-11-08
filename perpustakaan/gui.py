"""
gui.py - Tampilan grafis (GUI) untuk Sistem Perpustakaan.

Cara pakai:
    python gui.py

File ini hanya mengurus TAMPILAN. Semua data dan aturan (tambah, cari, edit,
hapus, simpan, muat) dikerjakan oleh class Perpustakaan di models.py.
Bagian yang memanggil backend ditandai dengan komentar "# BACKEND:".

Hanya memakai pustaka bawaan Python (tkinter), jadi tidak perlu instalasi.
"""

import math
import sys
import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import font as tkfont
from tkinter import messagebox, ttk

from models import DAFTAR_SUBJEK, Buku, Perpustakaan

# Sama dengan file data yang dipakai versi terminal (daftar-buku.py).
FILE_BUKU = Path(__file__).resolve().parent / "perpustakaan.json"

# --------------------------------------------------------------------------
# Warna dan ukuran
# --------------------------------------------------------------------------
BG = "#F5F3FA"
SURFACE = "#FFFFFF"
BORDER = "#ECE8F4"
BORDER_STRONG = "#D9D3E8"
INK = "#1F1B2E"
MUTED = "#8A85A0"
PRIMARY = "#6D3BD8"
PRIMARY_DARK = "#5A2DBA"
PRIMARY_SOFT = "#F1EBFF"
HEAD = "#F8F6FC"
ROW_SEL = "#F3EDFF"
DANGER = "#D6455D"
DANGER_SOFT = "#FDECEF"
DANGER_HOVER = "#FBDDE3"
DARK = "#1F1B2E"

AVATAR = ["#6D3BD8", "#2F80ED", "#E2566A", "#F2994A", "#27AE8F", "#9B51E0", "#2D9CDB", "#EB5757"]

CURSOR = "pointinghand" if sys.platform == "darwin" else "hand2"
SEMUA_SUBJEK = "Semua subjek"
PILIHAN_PER_HALAMAN = [5, 10, 20, 50]
TINGGI_BARIS = 56
TINGGI_HEADER = 44

# Lebar kolom dalam piksel. Nilai 0 berarti "isi sisa ruang".
LEBAR_KOLOM = {"cek": 56, "judul": 0, "penulis": 180, "id": 90, "subjek": 140, "tahun": 110, "aksi": 96}


# --------------------------------------------------------------------------
# Fungsi murni (tanpa tampilan) - mudah diuji
# --------------------------------------------------------------------------
def format_id(nilai):
    """1 -> '#0001'."""
    try:
        return f"#{int(nilai):04d}"
    except (TypeError, ValueError):
        return str(nilai)


def jumlah_halaman(total, per_halaman):
    """Jumlah halaman minimal 1, meskipun datanya kosong."""
    return max(1, math.ceil(total / per_halaman))


def nomor_halaman(aktif, total):
    """Daftar tombol pagination, mis. [1, 2, 3, 4, 5, '…', 100]."""
    if total <= 7:
        return list(range(1, total + 1))
    if aktif <= 4:
        return [1, 2, 3, 4, 5, "…", total]
    if aktif >= total - 3:
        return [1, "…"] + list(range(total - 4, total + 1))
    return [1, "…", aktif - 1, aktif, aktif + 1, "…", total]


def inisial(judul):
    for huruf in str(judul):
        if huruf.isalnum():
            return huruf.upper()
    return "?"


def warna_avatar(kunci):
    try:
        indeks = int(kunci)
    except (TypeError, ValueError):
        indeks = sum(ord(c) for c in str(kunci))
    return AVATAR[indeks % len(AVATAR)]


def samakan_subjek(teks):
    """Mencocokkan subjek tanpa peduli huruf besar-kecil: 'fiksi' -> 'Fiksi'."""
    bersih = str(teks).strip()
    for pilihan in DAFTAR_SUBJEK:
        if pilihan.lower() == bersih.lower():
            return pilihan
    return bersih


def validasi_buku(judul, penulis, subjek, tahun_teks):
    """Memeriksa isian formulir.

    Mengembalikan (data, pesan). Kalau valid, data berupa dict dan pesan kosong.
    Kalau tidak valid, data = None dan pesan berisi alasannya.
    """
    judul = judul.strip()
    penulis = penulis.strip()
    subjek = subjek.strip()
    tahun_teks = tahun_teks.strip()

    if not judul:
        return None, "Judul buku tidak boleh kosong."
    if not penulis:
        return None, "Nama penulis tidak boleh kosong."
    subjek = samakan_subjek(subjek)
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


def potong_teks(teks, font, lebar_maks):
    """Memotong teks yang kepanjangan dan menambahkan '…'."""
    teks = str(teks)
    if font.measure(teks) <= lebar_maks:
        return teks
    while teks and font.measure(teks + "…") > lebar_maks:
        teks = teks[:-1]
    return teks.rstrip() + "…"


def titik_bulat(x1, y1, x2, y2, r):
    """Titik-titik poligon untuk persegi panjang bersudut membulat."""
    return [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
            x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]


# --------------------------------------------------------------------------
# Komponen kecil buatan sendiri (supaya tampil sama di macOS, Windows, Linux)
# --------------------------------------------------------------------------
class TombolBulat(tk.Canvas):
    """Tombol dengan sudut membulat dan efek hover."""

    def __init__(self, induk, teks, command=None, font=None, lebar=None, tinggi=40,
                 radius=10, bg=PRIMARY, fg="#FFFFFF", hover=None, garis=None, latar=SURFACE):
        if font is None:
            font = tkfont.nametofont("TkDefaultFont")
        lebar = lebar or (font.measure(teks) + 40)
        super().__init__(induk, width=lebar, height=tinggi, bg=latar,
                         highlightthickness=0, bd=0, cursor=CURSOR if command else "")
        self._bg = bg
        self._hover = hover or PRIMARY_DARK
        self._perintah = command
        self._poli = self.create_polygon(
            titik_bulat(1, 1, lebar - 1, tinggi - 1, radius),
            smooth=True, fill=bg, outline=garis or bg, width=1)
        self.create_text(lebar / 2, tinggi / 2, text=teks, font=font, fill=fg)
        if command:
            self.bind("<Enter>", lambda e: self.itemconfigure(self._poli, fill=self._hover))
            self.bind("<Leave>", lambda e: self.itemconfigure(self._poli, fill=self._bg))
            self.bind("<ButtonRelease-1>", lambda e: command())


class Kotak(tk.Canvas):
    """Checkbox bergaya: status 'kosong', 'penuh', atau 'sebagian'."""

    def __init__(self, induk, bg, status="kosong", command=None):
        super().__init__(induk, width=22, height=22, bg=bg, highlightthickness=0, bd=0,
                         cursor=CURSOR)
        self._perintah = command
        self.atur(status)
        self.bind("<Button-1>", lambda e: self._perintah() if self._perintah else None)

    def atur(self, status):
        self.delete("all")
        isi = PRIMARY if status != "kosong" else SURFACE
        garis = PRIMARY if status != "kosong" else BORDER_STRONG
        self.create_polygon(titik_bulat(2, 2, 20, 20, 5), smooth=True, fill=isi,
                            outline=garis, width=1)
        if status == "penuh":
            self.create_line([6, 11, 10, 15, 16, 7], fill="#FFFFFF", width=2,
                             capstyle="round", joinstyle="round")
        elif status == "sebagian":
            self.create_line(6, 11, 16, 11, fill="#FFFFFF", width=2, capstyle="round")


class TombolIkon(tk.Canvas):
    """Ikon aksi (pensil untuk edit, tong sampah untuk hapus)."""

    def __init__(self, induk, jenis, bg, command):
        super().__init__(induk, width=30, height=30, bg=bg, highlightthickness=0, bd=0,
                         cursor=CURSOR)
        self._perintah = command
        self._normal = MUTED
        self._warna = PRIMARY if jenis == "edit" else DANGER
        self._lembut = PRIMARY_SOFT if jenis == "edit" else DANGER_SOFT
        self._lingkaran = self.create_oval(1, 1, 29, 29, fill=bg, outline="")
        self._garis = []
        self._poligon = []
        if jenis == "edit":
            self._poligon.append(self.create_polygon(
                [18, 8, 22, 12, 12, 22, 8, 22, 8, 18], fill="", outline=MUTED, width=2,
                joinstyle="round"))
            self._garis.append(self.create_line(15, 11, 19, 15, fill=MUTED, width=2))
        else:
            self._garis.append(self.create_line(9, 10, 21, 10, fill=MUTED, width=2,
                                                capstyle="round"))
            self._garis.append(self.create_line([13, 10, 13, 8, 17, 8, 17, 10], fill=MUTED,
                                                width=2, joinstyle="round"))
            self._poligon.append(self.create_polygon(
                [11, 10, 19, 10, 18, 22, 12, 22], fill="", outline=MUTED, width=2,
                joinstyle="round"))
            self._garis.append(self.create_line(14, 13, 14, 19, fill=MUTED, width=2))
            self._garis.append(self.create_line(16, 13, 16, 19, fill=MUTED, width=2))
        self._bg = bg
        self.bind("<Enter>", lambda e: self._warnai(self._warna, self._lembut))
        self.bind("<Leave>", lambda e: self._warnai(self._normal, self._bg))
        self.bind("<ButtonRelease-1>", lambda e: self._perintah())

    def _warnai(self, warna, latar):
        self.itemconfigure(self._lingkaran, fill=latar)
        for i in self._garis:
            self.itemconfigure(i, fill=warna)
        for i in self._poligon:
            self.itemconfigure(i, outline=warna)


class AreaGulir(tk.Frame):
    """Wadah yang bisa digulir (scroll) untuk baris tabel."""

    def __init__(self, induk, bg):
        super().__init__(induk, bg=bg)
        self.kanvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0, yscrollincrement=24)
        self.bar = ttk.Scrollbar(self, orient="vertical", command=self.kanvas.yview)
        self.kanvas.configure(yscrollcommand=self.bar.set)
        self.bar.pack(side="right", fill="y")
        self.kanvas.pack(side="left", fill="both", expand=True)
        self.isi = tk.Frame(self.kanvas, bg=bg)
        self._jendela = self.kanvas.create_window((0, 0), window=self.isi, anchor="nw")
        self.isi.bind("<Configure>", self._atur_area)
        self.kanvas.bind("<Configure>", self._atur_lebar)
        for peristiwa in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.kanvas.bind_all(peristiwa, self._roda, add="+")

    def _atur_area(self, _event=None):
        self.kanvas.configure(scrollregion=self.kanvas.bbox("all"))

    def _atur_lebar(self, event):
        self.kanvas.itemconfigure(self._jendela, width=event.width)

    def _roda(self, event):
        if self.kanvas.yview() == (0.0, 1.0):
            return  # isi muat di layar, tidak perlu digulir
        if getattr(event, "num", None) == 4:
            langkah = -1
        elif getattr(event, "num", None) == 5:
            langkah = 1
        elif sys.platform == "darwin":
            langkah = -event.delta
        else:
            langkah = -int(event.delta / 120)
        self.kanvas.yview_scroll(langkah, "units")


# --------------------------------------------------------------------------
# Dialog formulir tambah / edit buku
# --------------------------------------------------------------------------
class DialogBuku:
    def __init__(self, app, judul_dialog, daftar_subjek, awal=None, id_buku=None, saat_simpan=None):
        self.app = app
        self.saat_simpan = saat_simpan
        awal = awal or {}

        top = self.top = tk.Toplevel(app.root)
        top.withdraw()
        top.title(judul_dialog)
        top.configure(bg=SURFACE)
        top.resizable(False, False)
        top.transient(app.root)

        self.v_judul = tk.StringVar(value=str(awal.get("judul", "")))
        self.v_penulis = tk.StringVar(value=str(awal.get("penulis", "")))
        self.v_subjek = tk.StringVar(value=samakan_subjek(awal.get("subjek") or DAFTAR_SUBJEK[0]))
        self.v_tahun = tk.StringVar(value=str(awal.get("tahun_terbit", "")))

        isi = tk.Frame(top, bg=SURFACE)
        isi.pack(fill="both", expand=True, padx=32, pady=(26, 24))
        tk.Label(isi, text=judul_dialog, font=app.f_h2, fg=INK, bg=SURFACE).pack(anchor="w")
        if id_buku is None:
            keterangan = "ID buku dibuat otomatis."
        else:
            keterangan = f"ID {format_id(id_buku)} tidak dapat diubah."
        tk.Label(isi, text=keterangan, font=app.f_small, fg=MUTED, bg=SURFACE).pack(anchor="w", pady=(2, 0))

        self.e_judul = self._kolom(isi, "Judul buku", self.v_judul)
        self.e_penulis = self._kolom(isi, "Penulis", self.v_penulis)

        tk.Label(isi, text="Subjek", font=app.f_small, fg=MUTED, bg=SURFACE).pack(anchor="w", pady=(14, 4))
        self.e_subjek = ttk.Combobox(isi, textvariable=self.v_subjek, values=list(daftar_subjek),
                                     state="readonly", font=app.f_body)
        self.e_subjek.pack(fill="x", ipady=4)

        self.e_tahun = self._kolom(isi, "Tahun terbit", self.v_tahun)

        self.lbl_error = tk.Label(isi, text="", font=app.f_small, fg=DANGER, bg=SURFACE,
                                  wraplength=380, justify="left")
        self.lbl_error.pack(anchor="w", pady=(12, 0))

        tombol = tk.Frame(isi, bg=SURFACE)
        tombol.pack(fill="x", pady=(14, 0))
        TombolBulat(tombol, "Simpan", command=self._kirim, font=app.f_bold, lebar=110,
                    tinggi=42, latar=SURFACE).pack(side="right")
        TombolBulat(tombol, "Batal", command=self.tutup, font=app.f_bold, lebar=96, tinggi=42,
                    bg=SURFACE, fg=INK, garis=BORDER_STRONG, hover=HEAD,
                    latar=SURFACE).pack(side="right", padx=(0, 10))

        top.bind("<Return>", lambda e: self._kirim())
        top.bind("<Escape>", lambda e: self.tutup())
        top.protocol("WM_DELETE_WINDOW", self.tutup)

        top.update_idletasks()
        lebar, tinggi = top.winfo_reqwidth(), top.winfo_reqheight()
        r = app.root
        x = r.winfo_rootx() + (r.winfo_width() - lebar) // 2
        y = r.winfo_rooty() + (r.winfo_height() - tinggi) // 3
        top.geometry(f"+{max(x, 0)}+{max(y, 0)}")
        top.deiconify()
        try:
            top.grab_set()
        except tk.TclError:
            pass
        self.e_judul.focus_set()

    def _kolom(self, induk, label, variabel):
        tk.Label(induk, text=label, font=self.app.f_small, fg=MUTED, bg=SURFACE).pack(anchor="w", pady=(14, 4))
        kotak = tk.Frame(induk, bg=SURFACE, highlightthickness=1,
                         highlightbackground=BORDER_STRONG, highlightcolor=PRIMARY)
        kotak.pack(fill="x")
        isian = tk.Entry(kotak, textvariable=variabel, font=self.app.f_body, width=42, bd=0,
                         relief="flat", highlightthickness=0, bg=SURFACE, fg=INK,
                         insertbackground=INK)
        isian.pack(fill="x", padx=12, pady=9)
        isian.bind("<FocusIn>", lambda e: kotak.configure(highlightbackground=PRIMARY))
        isian.bind("<FocusOut>", lambda e: kotak.configure(highlightbackground=BORDER_STRONG))
        return isian

    def _kirim(self):
        data, pesan = validasi_buku(self.v_judul.get(), self.v_penulis.get(),
                                    self.v_subjek.get(), self.v_tahun.get())
        if data is None:
            self.lbl_error.configure(text=pesan)
            return
        if self.saat_simpan is None:
            return
        berhasil, pesan = self.saat_simpan(data)
        if berhasil:
            self.tutup()
        else:
            self.lbl_error.configure(text=pesan)

    def tutup(self):
        try:
            self.top.grab_release()
        except tk.TclError:
            pass
        self.top.destroy()


# --------------------------------------------------------------------------
# Aplikasi utama
# --------------------------------------------------------------------------
class AplikasiPerpustakaan:
    def __init__(self, root, perpustakaan, file_data):
        self.root = root
        self.perpus = perpustakaan
        self.file = file_data

        self.kata_kunci = ""
        self.filter_subjek = SEMUA_SUBJEK
        self.halaman = 1
        self.per_halaman = 10
        self.terpilih = set()
        self._id_halaman = []
        self._after_cari = None
        self._after_toast = None
        self._fokus_cari = False

        self._siapkan_font()
        self._bangun_ui()
        self._pasang_pintasan()
        self._render()

    # ---------------------------------------------------------------- font
    def _siapkan_font(self):
        tersedia = set(tkfont.families())
        keluarga = None
        for nama in ("Helvetica Neue", "Segoe UI", "Inter", "Roboto", "DejaVu Sans", "Arial"):
            if nama in tersedia:
                keluarga = nama
                break
        if keluarga is None:
            keluarga = tkfont.nametofont("TkDefaultFont").actual("family")
        self.f_body = tkfont.Font(family=keluarga, size=12)
        self.f_small = tkfont.Font(family=keluarga, size=11)
        self.f_tiny = tkfont.Font(family=keluarga, size=10)
        self.f_bold = tkfont.Font(family=keluarga, size=12, weight="bold")
        self.f_head = tkfont.Font(family=keluarga, size=11, weight="bold")
        self.f_h2 = tkfont.Font(family=keluarga, size=15, weight="bold")
        self.f_title = tkfont.Font(family=keluarga, size=24, weight="bold")
        self.f_logo = tkfont.Font(family=keluarga, size=20, weight="bold")

    # ------------------------------------------------------------------ UI
    def _bangun_ui(self):
        self.root.configure(bg=BG)
        self.sidebar = tk.Frame(self.root, bg=SURFACE, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        tk.Frame(self.root, bg=BORDER, width=1).pack(side="left", fill="y")
        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        self._bangun_sidebar()
        self._bangun_topbar()
        self._bangun_konten()

        self.lbl_toast = tk.Label(self.main, text="", font=self.f_body, fg="#FFFFFF", bg=DARK,
                                  padx=18, pady=10)

    def _bangun_sidebar(self):
        logo = tk.Frame(self.sidebar, bg=SURFACE, height=84)
        logo.pack(fill="x")
        logo.pack_propagate(False)
        ikon = tk.Canvas(logo, width=40, height=40, bg=SURFACE, highlightthickness=0, bd=0)
        ikon.place(x=24, y=22)
        ikon.create_polygon(titik_bulat(0, 0, 40, 40, 11), smooth=True, fill=PRIMARY, outline=PRIMARY)
        ikon.create_polygon(9, 13, 20, 16, 20, 31, 9, 28, fill="#FFFFFF", outline="")
        ikon.create_polygon(31, 13, 20, 16, 20, 31, 31, 28, fill="#DCCBFF", outline="")
        tk.Label(logo, text="Pustaka", font=self.f_logo, fg=PRIMARY, bg=SURFACE).place(x=74, y=26)

        tk.Label(self.sidebar, text="MENU", font=self.f_tiny, fg=MUTED, bg=SURFACE).pack(
            anchor="w", padx=28, pady=(14, 6))
        menu = [("beranda", "Beranda"), ("buku", "Perpustakaan"), ("anggota", "Anggota"),
                ("pinjam", "Peminjaman"), ("laporan", "Laporan"), ("setelan", "Pengaturan")]
        for kunci, label in menu:
            self._item_menu(kunci, label, aktif=(kunci == "buku"))

    def _item_menu(self, kunci, label, aktif):
        kanvas = tk.Canvas(self.sidebar, width=196, height=44, bg=SURFACE, highlightthickness=0,
                           bd=0, cursor=CURSOR)
        kanvas.pack(padx=12, pady=2)
        latar = kanvas.create_polygon(titik_bulat(0, 0, 196, 44, 10), smooth=True,
                                      fill=PRIMARY_SOFT if aktif else SURFACE,
                                      outline=PRIMARY_SOFT if aktif else SURFACE)
        warna = PRIMARY if aktif else MUTED
        self._gambar_ikon(kanvas, kunci, 28, 22, warna)
        kanvas.create_text(54, 22, text=label, anchor="w", fill=PRIMARY if aktif else INK,
                           font=self.f_bold if aktif else self.f_body)
        if aktif:
            return
        kanvas.bind("<Enter>", lambda e: kanvas.itemconfigure(latar, fill=HEAD, outline=HEAD))
        kanvas.bind("<Leave>", lambda e: kanvas.itemconfigure(latar, fill=SURFACE, outline=SURFACE))
        kanvas.bind("<ButtonRelease-1>", lambda e: self._toast(f"Menu “{label}” belum tersedia."))

    @staticmethod
    def _gambar_ikon(k, nama, cx, cy, w):
        if nama == "beranda":
            k.create_line([cx - 9, cy, cx, cy - 8, cx + 9, cy], fill=w, width=2, joinstyle="round")
            k.create_line([cx - 6, cy - 2, cx - 6, cy + 8, cx + 6, cy + 8, cx + 6, cy - 2],
                          fill=w, width=2, joinstyle="round")
        elif nama == "buku":
            k.create_rectangle(cx - 8, cy - 8, cx + 8, cy + 8, outline=w, width=2)
            k.create_line(cx - 4, cy - 3, cx + 4, cy - 3, fill=w, width=2)
            k.create_line(cx - 4, cy + 2, cx + 4, cy + 2, fill=w, width=2)
        elif nama == "anggota":
            k.create_oval(cx - 4, cy - 8, cx + 4, cy, outline=w, width=2)
            k.create_arc(cx - 9, cy + 2, cx + 9, cy + 18, start=0, extent=180, style="arc",
                         outline=w, width=2)
        elif nama == "pinjam":
            k.create_oval(cx - 8, cy - 8, cx + 8, cy + 8, outline=w, width=2)
            k.create_line([cx, cy - 4, cx, cy, cx + 4, cy + 2], fill=w, width=2, joinstyle="round")
        elif nama == "laporan":
            k.create_rectangle(cx - 8, cy, cx - 4, cy + 8, fill=w, outline=w)
            k.create_rectangle(cx - 2, cy - 5, cx + 2, cy + 8, fill=w, outline=w)
            k.create_rectangle(cx + 4, cy - 9, cx + 8, cy + 8, fill=w, outline=w)
        else:
            k.create_line(cx - 8, cy - 4, cx + 8, cy - 4, fill=w, width=2)
            k.create_line(cx - 8, cy + 4, cx + 8, cy + 4, fill=w, width=2)
            k.create_oval(cx - 5, cy - 7, cx + 1, cy - 1, fill=SURFACE, outline=w, width=2)
            k.create_oval(cx, cy + 1, cx + 6, cy + 7, fill=SURFACE, outline=w, width=2)

    def _bangun_topbar(self):
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
        self.ent_cari = tk.Entry(self.kotak_cari, textvariable=self.var_cari, font=self.f_body,
                                 bd=0, relief="flat", highlightthickness=0, bg=HEAD, fg=INK,
                                 insertbackground=INK)
        self.ent_cari.pack(side="left", fill="both", expand=True, padx=(0, 12), pady=8)
        self.hint = tk.Label(self.kotak_cari, text="Cari judul buku…", font=self.f_body,
                             fg=MUTED, bg=HEAD, cursor="xterm")
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
        avatar.create_text(20, 20, text="A", font=self.f_bold, fill=PRIMARY)
        teks = tk.Frame(pengguna, bg=SURFACE)
        teks.pack(side="left", padx=(12, 0))
        tk.Label(teks, text="Admin", font=self.f_bold, fg=INK, bg=SURFACE).pack(anchor="w")
        tk.Label(teks, text="Pustakawan", font=self.f_tiny, fg=MUTED, bg=SURFACE).pack(anchor="w")

    def _bangun_konten(self):
        konten = tk.Frame(self.main, bg=BG)
        konten.pack(fill="both", expand=True, padx=32, pady=(24, 24))

        judul = tk.Frame(konten, bg=BG)
        judul.pack(fill="x")
        kiri = tk.Frame(judul, bg=BG)
        kiri.pack(side="left")
        tk.Label(kiri, text="Perpustakaan", font=self.f_title, fg=INK, bg=BG).pack(anchor="w")
        remah = tk.Frame(kiri, bg=BG)
        remah.pack(anchor="w", pady=(4, 0))
        tk.Label(remah, text="Beranda", font=self.f_small, fg=MUTED, bg=BG).pack(side="left")
        tk.Label(remah, text="  /  ", font=self.f_small, fg=MUTED, bg=BG).pack(side="left")
        tk.Label(remah, text="Daftar Buku", font=self.f_small, fg=INK, bg=BG).pack(side="left")
        TombolBulat(judul, "+   Tambah Buku", command=self._klik_tambah, font=self.f_bold,
                    tinggi=44, latar=BG).pack(side="right")

        kartu = tk.Frame(konten, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER)
        kartu.pack(fill="both", expand=True, pady=(20, 0))

        # Kepala kartu: judul, jumlah, aksi massal, filter subjek
        kepala = tk.Frame(kartu, bg=SURFACE, height=76)
        kepala.pack(fill="x")
        kepala.pack_propagate(False)
        tk.Label(kepala, text="Semua Buku", font=self.f_h2, fg=INK, bg=SURFACE).pack(
            side="left", padx=(28, 0))
        self.lbl_jumlah = tk.Label(kepala, text="", font=self.f_small, fg=MUTED, bg=SURFACE)
        self.lbl_jumlah.pack(side="left", padx=(10, 0))

        self.var_subjek = tk.StringVar(value=SEMUA_SUBJEK)
        self.cb_subjek = ttk.Combobox(kepala, textvariable=self.var_subjek, state="readonly",
                                      values=[SEMUA_SUBJEK], width=18, font=self.f_body)
        self.cb_subjek.pack(side="right", padx=28)
        self.cb_subjek.bind("<<ComboboxSelected>>", self._ganti_filter)

        self.bar_pilih = tk.Frame(kepala, bg=SURFACE)
        self.lbl_pilih = tk.Label(self.bar_pilih, text="", font=self.f_bold, fg=PRIMARY, bg=SURFACE)
        self.lbl_pilih.pack(side="left", padx=(0, 12))
        TombolBulat(self.bar_pilih, "Hapus terpilih", command=self._klik_hapus_terpilih,
                    font=self.f_small, tinggi=34, radius=8, bg=DANGER_SOFT, fg=DANGER,
                    hover=DANGER_HOVER, latar=SURFACE).pack(side="left")

        tk.Frame(kartu, bg=BORDER, height=1).pack(fill="x")

        # Header tabel
        header = tk.Frame(kartu, bg=HEAD, height=TINGGI_HEADER)
        header.pack(fill="x")
        header.pack_propagate(False)
        sel = self._sel(header, "cek", HEAD, TINGGI_HEADER)
        self.kotak_semua = Kotak(sel, HEAD, "kosong", self._ganti_semua)
        self.kotak_semua.place(x=18, rely=0.5, anchor="w")
        for kunci, label in (("judul", "Nama Buku"), ("penulis", "Penulis"), ("id", "ID"),
                             ("subjek", "Subjek"), ("tahun", "Tahun Terbit"), ("aksi", "Aksi")):
            sel = self._sel(header, kunci, HEAD, TINGGI_HEADER)
            tk.Label(sel, text=label, font=self.f_head, fg=MUTED, bg=HEAD).place(
                x=6, rely=0.5, anchor="w")

        # Kaki kartu (dipasang sebelum area gulir supaya tidak terpotong)
        kaki = tk.Frame(kartu, bg=SURFACE, height=72)
        kaki.pack(side="bottom", fill="x")
        kaki.pack_propagate(False)
        tk.Frame(kartu, bg=BORDER, height=1).pack(side="bottom", fill="x")

        self.lbl_info = tk.Label(kaki, text="", font=self.f_small, fg=MUTED, bg=SURFACE)
        self.lbl_info.pack(side="left", padx=28)
        self.var_per = tk.StringVar(value=f"{self.per_halaman} / halaman")
        self.cb_per = ttk.Combobox(kaki, textvariable=self.var_per, state="readonly", width=12,
                                   values=[f"{n} / halaman" for n in PILIHAN_PER_HALAMAN],
                                   font=self.f_body)
        self.cb_per.pack(side="right", padx=28)
        self.cb_per.bind("<<ComboboxSelected>>", self._ganti_per_halaman)
        self.frm_hal = tk.Frame(kaki, bg=SURFACE)
        self.frm_hal.place(relx=0.5, rely=0.5, anchor="center")

        self.area = AreaGulir(kartu, SURFACE)
        self.area.pack(fill="both", expand=True)

    def _pasang_pintasan(self):
        mod = "Command" if sys.platform == "darwin" else "Control"
        self.root.bind(f"<{mod}-n>", lambda e: self._klik_tambah())
        self.root.bind(f"<{mod}-f>", lambda e: self.ent_cari.focus_set())

    # --------------------------------------------------- sel tabel (grid palsu)
    @staticmethod
    def _sel(induk, kunci, bg, tinggi):
        lebar = LEBAR_KOLOM[kunci]
        sel = tk.Frame(induk, bg=bg, width=lebar or 1, height=tinggi)
        sel.pack_propagate(False)
        if lebar:
            sel.pack(side="left", fill="y")
        else:
            sel.pack(side="left", fill="both", expand=True)
        return sel

    # ----------------------------------------------------------- data tampil
    def _daftar_subjek(self):
        # Subjek bukan teks bebas: hanya pilihan tetap dari models.py.
        return list(DAFTAR_SUBJEK)

    def _data_tampil(self):
        # BACKEND: cari_by_judul() untuk pencarian, semua_buku() untuk daftar lengkap
        if self.kata_kunci:
            sumber = self.perpus.cari_by_judul(self.kata_kunci)
        else:
            sumber = list(self.perpus.semua_buku())
        if self.filter_subjek != SEMUA_SUBJEK:
            sumber = [b for b in sumber if samakan_subjek(b.subjek) == self.filter_subjek]
        return sumber

    # --------------------------------------------------------------- render
    def _render(self):
        semua = self.perpus.semua_buku()
        subjek = self._daftar_subjek()
        if self.filter_subjek != SEMUA_SUBJEK and self.filter_subjek not in subjek:
            self.filter_subjek = SEMUA_SUBJEK
            self.var_subjek.set(SEMUA_SUBJEK)
        self.cb_subjek.configure(values=[SEMUA_SUBJEK] + subjek)
        self.terpilih &= {b.id for b in semua}

        data = self._data_tampil()
        total = len(data)
        jml = jumlah_halaman(total, self.per_halaman)
        self.halaman = max(1, min(self.halaman, jml))
        awal = (self.halaman - 1) * self.per_halaman
        tampil = data[awal:awal + self.per_halaman]
        self._id_halaman = [b.id for b in tampil]

        if total == len(semua):
            self.lbl_jumlah.configure(text=f"{len(semua)} buku")
        else:
            self.lbl_jumlah.configure(text=f"{total} dari {len(semua)} buku")

        if self.terpilih:
            self.lbl_pilih.configure(text=f"{len(self.terpilih)} dipilih")
            self.bar_pilih.pack(side="left", padx=28)
        else:
            self.bar_pilih.pack_forget()

        terpilih_di_halaman = [i for i in self._id_halaman if i in self.terpilih]
        if tampil and len(terpilih_di_halaman) == len(tampil):
            self.kotak_semua.atur("penuh")
        elif terpilih_di_halaman:
            self.kotak_semua.atur("sebagian")
        else:
            self.kotak_semua.atur("kosong")

        for w in self.area.isi.winfo_children():
            w.destroy()
        if tampil:
            for buku in tampil:
                self._baris(buku)
        else:
            self._tampilan_kosong(punya_buku=bool(semua))

        if total:
            self.lbl_info.configure(
                text=f"Menampilkan {awal + 1}–{awal + len(tampil)} dari {total} buku")
        else:
            self.lbl_info.configure(text="Tidak ada data")
        self._render_halaman(jml)

    def _baris(self, buku):
        dipilih = buku.id in self.terpilih
        bg = ROW_SEL if dipilih else SURFACE
        baris = tk.Frame(self.area.isi, bg=bg, height=TINGGI_BARIS)
        baris.pack_propagate(False)
        baris.pack(fill="x")

        sel = self._sel(baris, "cek", bg, TINGGI_BARIS)
        Kotak(sel, bg, "penuh" if dipilih else "kosong",
              lambda i=buku.id: self._ganti_pilih(i)).place(x=18, rely=0.5, anchor="w")

        sel = self._sel(baris, "judul", bg, TINGGI_BARIS)
        avatar = tk.Canvas(sel, width=36, height=36, bg=bg, highlightthickness=0, bd=0)
        avatar.place(x=6, rely=0.5, anchor="w")
        avatar.create_oval(0, 0, 35, 35, fill=warna_avatar(buku.id), outline="")
        avatar.create_text(18, 18, text=inisial(buku.judul), font=self.f_bold, fill="#FFFFFF")
        tk.Label(sel, text=buku.judul, font=self.f_bold, fg=INK, bg=bg).place(
            x=54, rely=0.5, anchor="w")

        self._teks_sel(baris, "penulis", bg, buku.penulis, INK)
        self._teks_sel(baris, "id", bg, format_id(buku.id), MUTED)
        self._teks_sel(baris, "subjek", bg, samakan_subjek(buku.subjek), INK)
        self._teks_sel(baris, "tahun", bg, buku.tahun_terbit, INK)

        sel = self._sel(baris, "aksi", bg, TINGGI_BARIS)
        TombolIkon(sel, "edit", bg, lambda b=buku: self._klik_edit(b)).place(
            x=2, rely=0.5, anchor="w")
        TombolIkon(sel, "hapus", bg, lambda b=buku: self._klik_hapus(b)).place(
            x=42, rely=0.5, anchor="w")

        tk.Frame(self.area.isi, bg=BORDER, height=1).pack(fill="x")

    def _teks_sel(self, baris, kunci, bg, teks, warna):
        sel = self._sel(baris, kunci, bg, TINGGI_BARIS)
        teks = potong_teks(teks, self.f_body, LEBAR_KOLOM[kunci] - 16)
        tk.Label(sel, text=teks, font=self.f_body, fg=warna, bg=bg).place(
            x=6, rely=0.5, anchor="w")

    def _tampilan_kosong(self, punya_buku):
        kotak = tk.Frame(self.area.isi, bg=SURFACE, height=300)
        kotak.pack(fill="x")
        kotak.pack_propagate(False)
        isi = tk.Frame(kotak, bg=SURFACE)
        isi.place(relx=0.5, rely=0.5, anchor="center")
        lingkaran = tk.Canvas(isi, width=64, height=64, bg=SURFACE, highlightthickness=0, bd=0)
        lingkaran.pack()
        lingkaran.create_oval(0, 0, 63, 63, fill=PRIMARY_SOFT, outline="")
        lingkaran.create_rectangle(20, 18, 44, 46, outline=PRIMARY, width=2)
        lingkaran.create_line(26, 26, 38, 26, fill=PRIMARY, width=2)
        lingkaran.create_line(26, 33, 38, 33, fill=PRIMARY, width=2)
        if punya_buku:
            judul, sub = "Tidak ada buku yang cocok", "Coba kata kunci atau filter subjek yang lain."
        else:
            judul, sub = "Belum ada buku", "Tambahkan buku pertama untuk mulai mengisi perpustakaan."
        tk.Label(isi, text=judul, font=self.f_h2, fg=INK, bg=SURFACE).pack(pady=(14, 2))
        tk.Label(isi, text=sub, font=self.f_body, fg=MUTED, bg=SURFACE).pack()
        if not punya_buku:
            TombolBulat(isi, "+   Tambah Buku", command=self._klik_tambah, font=self.f_bold,
                        tinggi=42, latar=SURFACE).pack(pady=(18, 0))

    def _render_halaman(self, jml):
        for w in self.frm_hal.winfo_children():
            w.destroy()

        def chip(teks, command=None, aktif=False, redup=False):
            if aktif:
                tombol = TombolBulat(self.frm_hal, teks, command=None, font=self.f_bold,
                                     lebar=38, tinggi=38, radius=9, bg=PRIMARY, fg="#FFFFFF")
            else:
                tombol = TombolBulat(self.frm_hal, teks, command=command, font=self.f_body,
                                     lebar=38, tinggi=38, radius=9, bg=SURFACE,
                                     fg=MUTED if redup else INK, hover=HEAD)
            tombol.pack(side="left", padx=2)

        chip("‹", (lambda: self._ke_halaman(self.halaman - 1)) if self.halaman > 1 else None,
             redup=True)
        for n in nomor_halaman(self.halaman, jml):
            if n == "…":
                tk.Label(self.frm_hal, text="…", font=self.f_body, fg=MUTED, bg=SURFACE,
                         width=2).pack(side="left")
            else:
                chip(str(n), lambda x=n: self._ke_halaman(x), aktif=(n == self.halaman))
        chip("›", (lambda: self._ke_halaman(self.halaman + 1)) if self.halaman < jml else None,
             redup=True)

    # ------------------------------------------------------------ interaksi
    def _ke_halaman(self, nomor):
        self.halaman = nomor
        self._render()
        self.area.kanvas.yview_moveto(0)

    def _ganti_per_halaman(self, _event=None):
        self.per_halaman = int(self.var_per.get().split()[0])
        self.halaman = 1
        self._render()
        self.area.kanvas.yview_moveto(0)

    def _ganti_filter(self, _event=None):
        self.filter_subjek = self.var_subjek.get()
        self.halaman = 1
        self._render()
        self.area.kanvas.yview_moveto(0)

    def _ganti_pilih(self, id_buku):
        if id_buku in self.terpilih:
            self.terpilih.discard(id_buku)
        else:
            self.terpilih.add(id_buku)
        self._render()

    def _ganti_semua(self):
        ids = set(self._id_halaman)
        if ids and ids <= self.terpilih:
            self.terpilih -= ids
        else:
            self.terpilih |= ids
        self._render()

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
        teks = self.var_cari.get().strip()
        self._atur_hint()
        if self._after_cari is not None:
            self.root.after_cancel(self._after_cari)
        self._after_cari = self.root.after(180, lambda: self._terapkan_cari(teks))

    def _terapkan_cari(self, teks):
        self._after_cari = None
        if teks == self.kata_kunci:
            return
        self.kata_kunci = teks
        self.halaman = 1
        self._render()
        self.area.kanvas.yview_moveto(0)

    # --------------------------------------------------- klik tombol -> dialog
    def _klik_tambah(self):
        DialogBuku(self, "Tambah Buku", self._daftar_subjek(), saat_simpan=self.aksi_tambah)

    def _klik_edit(self, buku):
        awal = {"judul": buku.judul, "penulis": buku.penulis, "subjek": buku.subjek,
                "tahun_terbit": buku.tahun_terbit}
        DialogBuku(self, "Edit Buku", self._daftar_subjek(), awal=awal, id_buku=buku.id,
                   saat_simpan=lambda data: self.aksi_edit(buku.id, data))

    def _klik_hapus(self, buku):
        if messagebox.askyesno("Hapus buku", f"Hapus “{buku.judul}”?\nTindakan ini tidak dapat dibatalkan.",
                               icon="warning", parent=self.root):
            self.aksi_hapus([buku.id])

    def _klik_hapus_terpilih(self):
        n = len(self.terpilih)
        if n and messagebox.askyesno("Hapus buku", f"Hapus {n} buku yang dipilih?\nTindakan ini tidak dapat dibatalkan.",
                                     icon="warning", parent=self.root):
            self.aksi_hapus(list(self.terpilih))

    # ------------------------------------------------ aksi (memanggil backend)
    def _simpan(self):
        # BACKEND: simpan(nama_file) menulis seluruh data ke JSON
        try:
            self.perpus.simpan(self.file)
        except OSError as error:
            messagebox.showerror("Gagal menyimpan",
                                 f"Perubahan belum tersimpan ke file:\n{error}", parent=self.root)
            return False
        return True

    def aksi_tambah(self, data):
        # BACKEND: id_berikutnya() membuat id otomatis, tambah_buku() menolak id ganda
        buku = Buku(self.perpus.id_berikutnya(), data["judul"], data["penulis"],
                    data["subjek"], data["tahun_terbit"])
        if not self.perpus.tambah_buku(buku):
            return False, "ID buku sudah dipakai."
        self._simpan()

        # Tampilkan buku baru: bersihkan pencarian/filter, lompat ke halaman terakhir.
        self.kata_kunci = ""
        self.var_cari.set("")
        self.filter_subjek = SEMUA_SUBJEK
        self.var_subjek.set(SEMUA_SUBJEK)
        self.terpilih.clear()
        self.halaman = jumlah_halaman(len(self.perpus.semua_buku()), self.per_halaman)
        self._render()
        self.area.kanvas.yview_moveto(1)
        self._toast(f"Buku “{buku.judul}” berhasil ditambahkan.")
        return True, ""

    def aksi_edit(self, id_buku, data):
        # BACKEND: edit_buku(id, ...) hanya mengubah field yang diberikan
        if not self.perpus.edit_buku(id_buku, judul=data["judul"], penulis=data["penulis"],
                                     subjek=data["subjek"], tahun_terbit=data["tahun_terbit"]):
            return False, "Buku tidak ditemukan."
        self._simpan()
        self._render()
        self._toast("Perubahan berhasil disimpan.")
        return True, ""

    def aksi_hapus(self, daftar_id):
        # BACKEND: hapus_buku(id)
        jumlah = sum(1 for i in daftar_id if self.perpus.hapus_buku(i))
        self.terpilih -= set(daftar_id)
        self._simpan()
        self._render()
        self._toast(f"{jumlah} buku dihapus.")

    # ---------------------------------------------------------------- toast
    def _toast(self, teks):
        self.lbl_toast.configure(text=teks)
        self.lbl_toast.place(relx=0.5, rely=1.0, y=-28, anchor="s")
        self.lbl_toast.lift()
        if self._after_toast is not None:
            self.root.after_cancel(self._after_toast)
        self._after_toast = self.root.after(2600, self.lbl_toast.place_forget)


# --------------------------------------------------------------------------
def main():
    root = tk.Tk()
    root.title("Pustaka - Sistem Perpustakaan")

    perpus = Perpustakaan()
    try:
        # BACKEND: muat(nama_file) mengisi daftar buku dari JSON
        perpus.muat(FILE_BUKU)
    except (ValueError, TypeError, KeyError, OSError) as error:
        root.withdraw()
        messagebox.showerror(
            "Gagal membaca data",
            f"File {FILE_BUKU.name} tidak dapat dibaca:\n{error}\n\n"
            "Periksa isi file tersebut, lalu buka aplikasi lagi.")
        root.destroy()
        return

    lebar = min(1280, root.winfo_screenwidth() - 80)
    tinggi = min(820, root.winfo_screenheight() - 120)
    x = (root.winfo_screenwidth() - lebar) // 2
    y = (root.winfo_screenheight() - tinggi) // 3
    root.geometry(f"{lebar}x{tinggi}+{x}+{y}")
    root.minsize(1180, 640)

    AplikasiPerpustakaan(root, perpus, FILE_BUKU)

    try:  # bawa jendela ke depan (berguna di macOS)
        root.lift()
        root.attributes("-topmost", True)
        root.after(300, lambda: root.attributes("-topmost", False))
    except tk.TclError:
        pass
    root.mainloop()


if __name__ == "__main__":
    main()
