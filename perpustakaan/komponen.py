"""komponen.py - Bagian-bagian tampilan yang dipakai bersama oleh semua halaman.

Isinya: warna, font, tombol, checkbox, ikon, lencana status, area gulir, kartu statistik,
tabel dengan pagination (TabelKartu), formulir dialog (DialogForm), dan kelas dasar Halaman.
Semua digambar sendiri supaya tampilannya sama di macOS, Windows, dan Linux.
"""

import math
import sys
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

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
SUCCESS = "#1F9D6B"
SUCCESS_SOFT = "#E6F6EF"
DARK = "#1F1B2E"

AVATAR = ["#6D3BD8", "#2F80ED", "#E2566A", "#F2994A", "#27AE8F", "#9B51E0", "#2D9CDB", "#EB5757"]
STATUS_WARNA = {  # status -> (warna teks, warna latar)
    "Tersedia": (SUCCESS, SUCCESS_SOFT),
    "Dikembalikan": (SUCCESS, SUCCESS_SOFT),
    "Dipinjam": (PRIMARY, PRIMARY_SOFT),
    "Terlambat": (DANGER, DANGER_SOFT),
}

CURSOR = "pointinghand" if sys.platform == "darwin" else "hand2"
TINGGI_BARIS = 56
TINGGI_HEADER = 44
PILIHAN_PER_HALAMAN = [5, 10, 20, 50]


# --------------------------------------------------------------------------
# Fungsi bantu murni
# --------------------------------------------------------------------------
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


def inisial(teks):
    for huruf in str(teks):
        if huruf.isalnum():
            return huruf.upper()
    return "?"


def warna_avatar(kunci):
    try:
        indeks = int(kunci)
    except (TypeError, ValueError):
        indeks = sum(ord(c) for c in str(kunci))
    return AVATAR[indeks % len(AVATAR)]


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


class Gaya:
    """Kumpulan font aplikasi. Dibuat setelah jendela utama ada."""

    def __init__(self):
        tersedia = set(tkfont.families())
        keluarga = None
        for nama in ("Helvetica Neue", "Segoe UI", "Inter", "Roboto", "DejaVu Sans", "Arial"):
            if nama in tersedia:
                keluarga = nama
                break
        if keluarga is None:
            keluarga = tkfont.nametofont("TkDefaultFont").actual("family")
        self.body = tkfont.Font(family=keluarga, size=12)
        self.small = tkfont.Font(family=keluarga, size=11)
        self.tiny = tkfont.Font(family=keluarga, size=10)
        self.bold = tkfont.Font(family=keluarga, size=12, weight="bold")
        self.head = tkfont.Font(family=keluarga, size=11, weight="bold")
        self.h2 = tkfont.Font(family=keluarga, size=15, weight="bold")
        self.title = tkfont.Font(family=keluarga, size=24, weight="bold")
        self.logo = tkfont.Font(family=keluarga, size=20, weight="bold")


def gambar_ikon(k, nama, cx, cy, w):
    """Menggambar ikon sederhana (garis) berpusat di (cx, cy) pada kanvas k."""
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
    else:  # setelan
        k.create_line(cx - 8, cy - 4, cx + 8, cy - 4, fill=w, width=2)
        k.create_line(cx - 8, cy + 4, cx + 8, cy + 4, fill=w, width=2)
        k.create_oval(cx - 5, cy - 7, cx + 1, cy - 1, fill=SURFACE, outline=w, width=2)
        k.create_oval(cx, cy + 1, cx + 6, cy + 7, fill=SURFACE, outline=w, width=2)


# --------------------------------------------------------------------------
# Komponen kecil
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
        self._poli = self.create_polygon(
            titik_bulat(1, 1, lebar - 1, tinggi - 1, radius),
            smooth=True, fill=bg, outline=garis or bg, width=1)
        self.create_text(lebar / 2, tinggi / 2, text=teks, font=font, fill=fg)
        if command:
            self.bind("<Enter>", lambda e: self.itemconfigure(self._poli, fill=self._hover))
            self.bind("<Leave>", lambda e: self.itemconfigure(self._poli, fill=self._bg))
            self.bind("<ButtonRelease-1>", lambda e: command())


def tombol_garis(induk, teks, command, font, latar, tinggi=44, lebar=None):
    """Tombol putih bergaris (aksi sekunder)."""
    return TombolBulat(induk, teks, command=command, font=font, tinggi=tinggi, lebar=lebar,
                       bg=SURFACE, fg=INK, garis=BORDER_STRONG, hover=HEAD, latar=latar)


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
    """Ikon aksi pada baris tabel: 'edit' (pensil), 'hapus' (tong sampah), 'kembali' (panah)."""

    def __init__(self, induk, jenis, bg, command):
        super().__init__(induk, width=30, height=30, bg=bg, highlightthickness=0, bd=0,
                         cursor=CURSOR)
        self._perintah = command
        self._normal = MUTED
        self._warna, self._lembut = {
            "edit": (PRIMARY, PRIMARY_SOFT),
            "hapus": (DANGER, DANGER_SOFT),
            "kembali": (SUCCESS, SUCCESS_SOFT),
        }[jenis]
        self._lingkaran = self.create_oval(1, 1, 29, 29, fill=bg, outline="")
        self._garis = []
        self._poligon = []
        if jenis == "edit":
            self._poligon.append(self.create_polygon(
                [18, 8, 22, 12, 12, 22, 8, 22, 8, 18], fill="", outline=MUTED, width=2,
                joinstyle="round"))
            self._garis.append(self.create_line(15, 11, 19, 15, fill=MUTED, width=2))
        elif jenis == "hapus":
            self._garis.append(self.create_line(9, 10, 21, 10, fill=MUTED, width=2,
                                                capstyle="round"))
            self._garis.append(self.create_line([13, 10, 13, 8, 17, 8, 17, 10], fill=MUTED,
                                                width=2, joinstyle="round"))
            self._poligon.append(self.create_polygon(
                [11, 10, 19, 10, 18, 22, 12, 22], fill="", outline=MUTED, width=2,
                joinstyle="round"))
            self._garis.append(self.create_line(14, 13, 14, 19, fill=MUTED, width=2))
            self._garis.append(self.create_line(16, 13, 16, 19, fill=MUTED, width=2))
        else:  # kembali: panah ke kiri
            self._garis.append(self.create_line(10, 15, 21, 15, fill=MUTED, width=2,
                                                capstyle="round"))
            self._garis.append(self.create_line([14, 11, 10, 15, 14, 19], fill=MUTED, width=2,
                                                capstyle="round", joinstyle="round"))
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


class Lencana(tk.Canvas):
    """Label status berbentuk pil, mis. 'Terlambat'."""

    def __init__(self, induk, teks, font, latar):
        fg, bg = STATUS_WARNA.get(teks, (MUTED, HEAD))
        lebar = font.measure(teks) + 28
        super().__init__(induk, width=lebar, height=26, bg=latar, highlightthickness=0, bd=0)
        self.create_polygon(titik_bulat(0, 0, lebar - 1, 25, 12), smooth=True, fill=bg, outline=bg)
        self.create_text(lebar / 2, 13, text=teks, font=font, fill=fg)


class AreaGulir(tk.Frame):
    """Wadah yang bisa digulir (scroll). Isi ditaruh di atribut `isi`."""

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
        if not self.winfo_ismapped() or self.kanvas.yview() == (0.0, 1.0):
            return  # halaman tersembunyi, atau isi muat di layar
        if getattr(event, "num", None) == 4:
            langkah = -1
        elif getattr(event, "num", None) == 5:
            langkah = 1
        elif sys.platform == "darwin":
            langkah = -event.delta
        else:
            langkah = -int(event.delta / 120)
        self.kanvas.yview_scroll(langkah, "units")


class KartuStat(tk.Frame):
    """Kartu angka ringkasan: ikon bulat, angka besar, dan keterangan."""

    def __init__(self, induk, app, ikon, judul, nilai, warna, lembut):
        super().__init__(induk, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER)
        dalam = tk.Frame(self, bg=SURFACE)
        dalam.pack(fill="both", expand=True, padx=20, pady=18)
        lingkaran = tk.Canvas(dalam, width=48, height=48, bg=SURFACE, highlightthickness=0, bd=0)
        lingkaran.pack(side="left")
        lingkaran.create_oval(0, 0, 47, 47, fill=lembut, outline="")
        gambar_ikon(lingkaran, ikon, 24, 24, warna)
        teks = tk.Frame(dalam, bg=SURFACE)
        teks.pack(side="left", padx=(16, 0))
        tk.Label(teks, text=str(nilai), font=app.f.title, fg=INK, bg=SURFACE).pack(anchor="w")
        tk.Label(teks, text=judul, font=app.f.small, fg=MUTED, bg=SURFACE).pack(anchor="w")


# --------------------------------------------------------------------------
# Tabel dengan pencarian, filter, pilih banyak, dan pagination
# --------------------------------------------------------------------------
class TabelKartu(tk.Frame):
    """Kartu berisi tabel. Halaman cukup menyebutkan kolom dan dari mana datanya.

    kolom       : daftar dict {"judul", "lebar", "teks"(fungsi item -> teks) atau "sel"(fungsi
                  menggambar sendiri), "warna"(opsional)}. Lebar 0 = isi sisa ruang.
    ambil_data  : fungsi tanpa argumen yang mengembalikan daftar item yang SUDAH tersaring.
    kunci_id    : fungsi item -> id unik.
    aksi        : daftar (jenis_ikon, fungsi(item), syarat(item) atau None).
    """

    def __init__(self, induk, app, judul, kolom, ambil_data, kunci_id, aksi=(),
                 saat_hapus_massal=None, opsi_filter=None, saat_filter=None,
                 hitung_semua=None, satuan="data", kosong=None, tombol_kosong=None):
        super().__init__(induk, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER)
        self.app = app
        self.f = app.f
        self.kolom = kolom
        self.ambil_data = ambil_data
        self.kunci_id = kunci_id
        self.aksi = [(tuple(a) + (None,))[:3] for a in aksi]
        self.saat_hapus_massal = saat_hapus_massal
        self.saat_filter = saat_filter
        self.hitung_semua = hitung_semua
        self.satuan = satuan
        self.kosong = kosong or ("Belum ada data", "Data akan muncul di sini.")
        self.tombol_kosong = tombol_kosong
        self.halaman = 1
        self.per_halaman = 10
        self.terpilih = set()
        self._id_halaman = []

        self.lebar = []
        if saat_hapus_massal:
            self.lebar.append(56)
        self.lebar += [k["lebar"] for k in kolom]
        if self.aksi:
            self.lebar.append(40 * len(self.aksi) + 16)
        self._bangun(judul, opsi_filter)

    # ------------------------------------------------------------ kerangka
    def _bangun(self, judul, opsi_filter):
        f = self.f
        kepala = tk.Frame(self, bg=SURFACE, height=76)
        kepala.pack(fill="x")
        kepala.pack_propagate(False)
        tk.Label(kepala, text=judul, font=f.h2, fg=INK, bg=SURFACE).pack(side="left", padx=(28, 0))
        self.lbl_jumlah = tk.Label(kepala, text="", font=f.small, fg=MUTED, bg=SURFACE)
        self.lbl_jumlah.pack(side="left", padx=(10, 0))

        self.var_filter = tk.StringVar(value=opsi_filter[0] if opsi_filter else "")
        if opsi_filter:
            self.cb_filter = ttk.Combobox(kepala, textvariable=self.var_filter, state="readonly",
                                          values=list(opsi_filter), width=18, font=f.body)
            self.cb_filter.pack(side="right", padx=28)
            self.cb_filter.bind("<<ComboboxSelected>>", self._ganti_filter)

        self.bar_pilih = tk.Frame(kepala, bg=SURFACE)
        self.lbl_pilih = tk.Label(self.bar_pilih, text="", font=f.bold, fg=PRIMARY, bg=SURFACE)
        self.lbl_pilih.pack(side="left", padx=(0, 12))
        TombolBulat(self.bar_pilih, "Hapus terpilih", command=self._klik_hapus_massal, font=f.small,
                    tinggi=34, radius=8, bg=DANGER_SOFT, fg=DANGER, hover=DANGER_HOVER,
                    latar=SURFACE).pack(side="left")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        header = tk.Frame(self, bg=HEAD, height=TINGGI_HEADER)
        header.pack(fill="x")
        header.pack_propagate(False)
        lebar = iter(self.lebar)
        self.kotak_semua = None
        if self.saat_hapus_massal:
            sel = self._sel(header, next(lebar), HEAD, TINGGI_HEADER)
            self.kotak_semua = Kotak(sel, HEAD, "kosong", self._ganti_semua)
            self.kotak_semua.place(x=18, rely=0.5, anchor="w")
        for k in self.kolom:
            sel = self._sel(header, next(lebar), HEAD, TINGGI_HEADER)
            tk.Label(sel, text=k["judul"], font=f.head, fg=MUTED, bg=HEAD).place(x=6, rely=0.5, anchor="w")
        if self.aksi:
            sel = self._sel(header, next(lebar), HEAD, TINGGI_HEADER)
            tk.Label(sel, text="Aksi", font=f.head, fg=MUTED, bg=HEAD).place(x=6, rely=0.5, anchor="w")

        # Kaki dipasang sebelum area gulir supaya tidak terpotong saat jendela kecil.
        kaki = tk.Frame(self, bg=SURFACE, height=72)
        kaki.pack(side="bottom", fill="x")
        kaki.pack_propagate(False)
        tk.Frame(self, bg=BORDER, height=1).pack(side="bottom", fill="x")
        self.lbl_info = tk.Label(kaki, text="", font=f.small, fg=MUTED, bg=SURFACE)
        self.lbl_info.pack(side="left", padx=28)
        self.var_per = tk.StringVar(value=f"{self.per_halaman} / halaman")
        self.cb_per = ttk.Combobox(kaki, textvariable=self.var_per, state="readonly", width=12,
                                   values=[f"{n} / halaman" for n in PILIHAN_PER_HALAMAN], font=f.body)
        self.cb_per.pack(side="right", padx=28)
        self.cb_per.bind("<<ComboboxSelected>>", self._ganti_per_halaman)
        self.frm_hal = tk.Frame(kaki, bg=SURFACE)
        self.frm_hal.place(relx=0.5, rely=0.5, anchor="center")

        self.area = AreaGulir(self, SURFACE)
        self.area.pack(fill="both", expand=True)

    @staticmethod
    def _sel(induk, lebar, bg, tinggi):
        sel = tk.Frame(induk, bg=bg, width=lebar or 1, height=tinggi)
        sel.pack_propagate(False)
        if lebar:
            sel.pack(side="left", fill="y")
        else:
            sel.pack(side="left", fill="both", expand=True)
        return sel

    # --------------------------------------------------------------- render
    def render(self):
        data = self.ambil_data()
        total = len(data)
        jml = jumlah_halaman(total, self.per_halaman)
        self.halaman = max(1, min(self.halaman, jml))
        awal = (self.halaman - 1) * self.per_halaman
        tampil = data[awal:awal + self.per_halaman]
        self._id_halaman = [self.kunci_id(i) for i in tampil]
        semua = self.hitung_semua() if self.hitung_semua else total
        self.terpilih &= {self.kunci_id(i) for i in data}

        if total == semua:
            self.lbl_jumlah.configure(text=f"{semua} {self.satuan}")
        else:
            self.lbl_jumlah.configure(text=f"{total} dari {semua} {self.satuan}")

        if self.terpilih:
            self.lbl_pilih.configure(text=f"{len(self.terpilih)} dipilih")
            self.bar_pilih.pack(side="left", padx=28)
        else:
            self.bar_pilih.pack_forget()
        if self.kotak_semua is not None:
            di_halaman = [i for i in self._id_halaman if i in self.terpilih]
            if tampil and len(di_halaman) == len(tampil):
                self.kotak_semua.atur("penuh")
            elif di_halaman:
                self.kotak_semua.atur("sebagian")
            else:
                self.kotak_semua.atur("kosong")

        for w in self.area.isi.winfo_children():
            w.destroy()
        if tampil:
            for item in tampil:
                self._baris(item)
        else:
            self._tampilan_kosong(punya_data=semua > 0)

        if total:
            self.lbl_info.configure(text=f"Menampilkan {awal + 1}–{awal + len(tampil)} dari {total} {self.satuan}")
        else:
            self.lbl_info.configure(text="Tidak ada data")
        self._render_halaman(jml)

    muat_ulang = render

    def _baris(self, item):
        id_item = self.kunci_id(item)
        dipilih = id_item in self.terpilih
        bg = ROW_SEL if dipilih else SURFACE
        baris = tk.Frame(self.area.isi, bg=bg, height=TINGGI_BARIS)
        baris.pack_propagate(False)
        baris.pack(fill="x")
        lebar = iter(self.lebar)
        if self.saat_hapus_massal:
            sel = self._sel(baris, next(lebar), bg, TINGGI_BARIS)
            Kotak(sel, bg, "penuh" if dipilih else "kosong",
                  lambda i=id_item: self._ganti_pilih(i)).place(x=18, rely=0.5, anchor="w")
        for k in self.kolom:
            lb = next(lebar)
            sel = self._sel(baris, lb, bg, TINGGI_BARIS)
            if "sel" in k:
                k["sel"](sel, item, bg)
            else:
                teks = potong_teks(k["teks"](item), self.f.body, lb - 16) if lb else str(k["teks"](item))
                tk.Label(sel, text=teks, font=self.f.body, fg=k.get("warna", INK), bg=bg).place(
                    x=6, rely=0.5, anchor="w")
        if self.aksi:
            sel = self._sel(baris, next(lebar), bg, TINGGI_BARIS)
            x = 2
            for jenis, perintah, syarat in self.aksi:
                if perintah is not None and (syarat is None or syarat(item)):
                    TombolIkon(sel, jenis, bg, lambda it=item, p=perintah: p(it)).place(
                        x=x, rely=0.5, anchor="w")
                x += 40
        tk.Frame(self.area.isi, bg=BORDER, height=1).pack(fill="x")

    def _tampilan_kosong(self, punya_data):
        f = self.f
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
        if punya_data:
            judul, sub = "Tidak ada yang cocok", "Coba kata kunci atau filter yang lain."
        else:
            judul, sub = self.kosong
        tk.Label(isi, text=judul, font=f.h2, fg=INK, bg=SURFACE).pack(pady=(14, 2))
        tk.Label(isi, text=sub, font=f.body, fg=MUTED, bg=SURFACE).pack()
        if not punya_data and self.tombol_kosong:
            teks, perintah = self.tombol_kosong
            TombolBulat(isi, teks, command=perintah, font=f.bold, tinggi=42, latar=SURFACE).pack(pady=(18, 0))

    def _render_halaman(self, jml):
        f = self.f
        for w in self.frm_hal.winfo_children():
            w.destroy()

        def chip(teks, command=None, aktif=False, redup=False):
            if aktif:
                tombol = TombolBulat(self.frm_hal, teks, font=f.bold, lebar=38, tinggi=38,
                                     radius=9, bg=PRIMARY, fg="#FFFFFF")
            else:
                tombol = TombolBulat(self.frm_hal, teks, command=command, font=f.body, lebar=38,
                                     tinggi=38, radius=9, bg=SURFACE, fg=MUTED if redup else INK,
                                     hover=HEAD)
            tombol.pack(side="left", padx=2)

        chip("‹", (lambda: self.ke_halaman(self.halaman - 1)) if self.halaman > 1 else None, redup=True)
        for n in nomor_halaman(self.halaman, jml):
            if n == "…":
                tk.Label(self.frm_hal, text="…", font=f.body, fg=MUTED, bg=SURFACE, width=2).pack(side="left")
            else:
                chip(str(n), lambda x=n: self.ke_halaman(x), aktif=(n == self.halaman))
        chip("›", (lambda: self.ke_halaman(self.halaman + 1)) if self.halaman < jml else None, redup=True)

    # ------------------------------------------------------------ interaksi
    def ke_halaman(self, nomor):
        self.halaman = nomor
        self.render()
        self.area.kanvas.yview_moveto(0)

    def reset(self):
        """Kembali ke halaman 1 (setelah mencari atau menyaring)."""
        self.ke_halaman(1)

    def ke_akhir(self):
        self.halaman = jumlah_halaman(len(self.ambil_data()), self.per_halaman)
        self.render()
        self.area.kanvas.yview_moveto(1)

    def nilai_filter(self):
        return self.var_filter.get()

    def atur_filter(self, nilai):
        self.var_filter.set(nilai)

    def bersihkan_pilihan(self):
        self.terpilih.clear()

    def _ganti_filter(self, _event=None):
        if self.saat_filter:
            self.saat_filter(self.var_filter.get())
        self.terpilih.clear()
        self.reset()

    def _ganti_per_halaman(self, _event=None):
        self.per_halaman = int(self.var_per.get().split()[0])
        self.reset()

    def _ganti_pilih(self, id_item):
        if id_item in self.terpilih:
            self.terpilih.discard(id_item)
        else:
            self.terpilih.add(id_item)
        self.render()

    def _ganti_semua(self):
        ids = set(self._id_halaman)
        if ids and ids <= self.terpilih:
            self.terpilih -= ids
        else:
            self.terpilih |= ids
        self.render()

    def _klik_hapus_massal(self):
        if self.saat_hapus_massal and self.terpilih:
            self.saat_hapus_massal(list(self.terpilih))


def kolom_teks(induk, f, variabel):
    """Kotak isian teks dengan garis tepi yang berubah ungu saat difokuskan."""
    kotak = tk.Frame(induk, bg=SURFACE, highlightthickness=1,
                     highlightbackground=BORDER_STRONG, highlightcolor=PRIMARY)
    kotak.pack(fill="x")
    isian = tk.Entry(kotak, textvariable=variabel, font=f.body, width=42, bd=0,
                     relief="flat", highlightthickness=0, bg=SURFACE, fg=INK,
                     insertbackground=INK)
    isian.pack(fill="x", padx=12, pady=9)
    isian.bind("<FocusIn>", lambda e: kotak.configure(highlightbackground=PRIMARY))
    isian.bind("<FocusOut>", lambda e: kotak.configure(highlightbackground=BORDER_STRONG))
    return isian


# --------------------------------------------------------------------------
# Dialog formulir (dipakai untuk tambah/edit/pinjam)
# --------------------------------------------------------------------------
class DialogForm:
    """Jendela formulir.

    medan       : daftar dict {"kunci", "label", "jenis": "teks" atau "pilihan", "pilihan": [...], "nilai"}
    validasi    : fungsi(dict isian) -> (data, pesan). data None berarti isian salah.
    saat_simpan : fungsi(data) -> (berhasil, pesan). Kalau berhasil, dialog ditutup.
    """

    def __init__(self, app, judul, medan, validasi, saat_simpan, keterangan="", teks_simpan="Simpan"):
        self.app = app
        self.validasi = validasi
        self.saat_simpan = saat_simpan
        f = app.f

        top = self.top = tk.Toplevel(app.root)
        top.withdraw()
        top.title(judul)
        top.configure(bg=SURFACE)
        top.resizable(False, False)
        top.transient(app.root)

        isi = tk.Frame(top, bg=SURFACE)
        isi.pack(fill="both", expand=True, padx=32, pady=(26, 24))
        tk.Label(isi, text=judul, font=f.h2, fg=INK, bg=SURFACE).pack(anchor="w")
        if keterangan:
            tk.Label(isi, text=keterangan, font=f.small, fg=MUTED, bg=SURFACE, wraplength=400,
                     justify="left").pack(anchor="w", pady=(2, 0))

        self.vars = {}
        pertama = None
        for m in medan:
            var = tk.StringVar(value=str(m.get("nilai", "")))
            self.vars[m["kunci"]] = var
            tk.Label(isi, text=m["label"], font=f.small, fg=MUTED, bg=SURFACE).pack(anchor="w", pady=(14, 4))
            if m.get("jenis") == "pilihan":
                isian = ttk.Combobox(isi, textvariable=var, values=list(m["pilihan"]),
                                     state="readonly", font=f.body)
                isian.pack(fill="x", ipady=4)
            else:
                isian = kolom_teks(isi, f, var)
            if pertama is None:
                pertama = isian

        self.lbl_error = tk.Label(isi, text="", font=f.small, fg=DANGER, bg=SURFACE,
                                  wraplength=400, justify="left")
        self.lbl_error.pack(anchor="w", pady=(12, 0))

        tombol = tk.Frame(isi, bg=SURFACE)
        tombol.pack(fill="x", pady=(14, 0))
        TombolBulat(tombol, teks_simpan, command=self._kirim, font=f.bold, lebar=110, tinggi=42,
                    latar=SURFACE).pack(side="right")
        tombol_garis(tombol, "Batal", self.tutup, f.bold, SURFACE, tinggi=42, lebar=96).pack(
            side="right", padx=(0, 10))

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
        if pertama is not None:
            pertama.focus_set()

    def _kirim(self):
        data, pesan = self.validasi({k: v.get() for k, v in self.vars.items()})
        if data is None:
            self.lbl_error.configure(text=pesan)
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
# Kelas dasar halaman
# --------------------------------------------------------------------------
class Halaman(tk.Frame):
    """Dasar semua halaman. Sub-kelas mengisi `placeholder` dan method yang diperlukan."""

    placeholder = None  # teks petunjuk kotak cari; None = kotak cari disembunyikan

    def __init__(self, induk, app):
        super().__init__(induk, bg=BG)
        self.app = app
        self.f = app.f
        self.layanan = app.layanan
        self.kata_kunci = ""
        self.gulir = None

    def kerangka(self, judul, remah, teks_tombol=None, perintah=None, tombol_lain=(), gulir=False):
        """Membuat judul halaman + tombol aksi. Mengembalikan frame untuk isi halaman."""
        if gulir:
            self.gulir = AreaGulir(self, BG)
            self.gulir.pack(fill="both", expand=True)
            wadah = self.gulir.isi
        else:
            wadah = self
        isi = tk.Frame(wadah, bg=BG)
        isi.pack(fill="both", expand=True, padx=32, pady=(24, 24))
        atas = tk.Frame(isi, bg=BG)
        atas.pack(fill="x")
        kiri = tk.Frame(atas, bg=BG)
        kiri.pack(side="left")
        tk.Label(kiri, text=judul, font=self.f.title, fg=INK, bg=BG).pack(anchor="w")
        baris = tk.Frame(kiri, bg=BG)
        baris.pack(anchor="w", pady=(4, 0))
        tk.Label(baris, text="Beranda", font=self.f.small, fg=MUTED, bg=BG).pack(side="left")
        tk.Label(baris, text="  /  ", font=self.f.small, fg=MUTED, bg=BG).pack(side="left")
        tk.Label(baris, text=remah, font=self.f.small, fg=INK, bg=BG).pack(side="left")
        kanan = tk.Frame(atas, bg=BG)
        kanan.pack(side="right")
        for teks, cmd in tombol_lain:
            tombol_garis(kanan, teks, cmd, self.f.bold, BG).pack(side="left", padx=(0, 10))
        if teks_tombol:
            TombolBulat(kanan, teks_tombol, command=perintah, font=self.f.bold, tinggi=44,
                        latar=BG).pack(side="left")
        return isi

    def segarkan(self):
        """Dipanggil setiap kali halaman ditampilkan."""

    def cari(self, teks):
        """Dipanggil saat kotak cari di atas berubah."""

    def tambah(self):
        """Dipanggil oleh pintasan Cmd/Ctrl+N."""
