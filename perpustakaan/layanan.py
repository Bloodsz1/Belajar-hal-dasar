"""layanan.py - Menyatukan semua data dan menjaga aturan yang melibatkan lebih dari satu jenis data.

Contoh aturan lintas data:
  - Buku yang sedang dipinjam tidak boleh dihapus.
  - Anggota yang masih punya pinjaman tidak boleh dihapus.
  - Anggota yang punya buku terlambat tidak boleh meminjam lagi.

Tampilan (GUI) cukup memanggil method di sini dan menampilkan pesannya.
"""

import os

from anggota import DaftarAnggota
from models import Perpustakaan
from pengaturan import Pengaturan
from peminjaman import RiwayatPeminjaman
from util import format_rupiah, format_tanggal

FILE_BUKU = "perpustakaan.json"
FILE_ANGGOTA = "anggota.json"
FILE_PEMINJAMAN = "peminjaman.json"
FILE_PENGATURAN = "pengaturan.json"
SEMUA_FILE = (FILE_BUKU, FILE_ANGGOTA, FILE_PEMINJAMAN, FILE_PENGATURAN)


class Layanan:
    def __init__(self, folder):
        self.folder = str(folder)
        self.perpus = Perpustakaan()
        self.anggota = DaftarAnggota()
        self.riwayat = RiwayatPeminjaman()
        self.pengaturan = Pengaturan()

    def jalur(self, nama_file):
        return os.path.join(self.folder, nama_file)

    # ------------------------------------------------------------ simpan / muat
    def muat_semua(self):
        """Memuat semua data. Kalau ada file rusak, muncul DataRusakError."""
        self.perpus.muat(self.jalur(FILE_BUKU))
        self.anggota.muat(self.jalur(FILE_ANGGOTA))
        self.riwayat.muat(self.jalur(FILE_PEMINJAMAN))
        self.pengaturan.muat(self.jalur(FILE_PENGATURAN))

    def simpan_buku(self):
        self.perpus.simpan(self.jalur(FILE_BUKU))

    def simpan_anggota(self):
        self.anggota.simpan(self.jalur(FILE_ANGGOTA))

    def simpan_peminjaman(self):
        self.riwayat.simpan(self.jalur(FILE_PEMINJAMAN))

    def simpan_pengaturan(self):
        self.pengaturan.simpan(self.jalur(FILE_PENGATURAN))

    # ------------------------------------------------------------- bantuan nama
    def judul_buku(self, id_buku):
        buku = self.perpus.cari_by_id(id_buku)
        return buku.judul if buku else "(buku dihapus)"

    def nama_anggota(self, id_anggota):
        anggota = self.anggota.cari_by_id(id_anggota)
        return anggota.nama if anggota else "(anggota dihapus)"

    def status_buku(self, id_buku):
        """'Tersedia', 'Dipinjam', atau 'Terlambat'."""
        for p in self.riwayat.aktif():
            if p.id_buku == id_buku:
                return p.status()
        return "Tersedia"

    def buku_tersedia(self):
        return [b for b in self.perpus.semua_buku() if not self.riwayat.buku_sedang_dipinjam(b.id)]

    # ---------------------------------------------------------------- aturan
    def bisa_hapus_buku(self, id_buku):
        if self.riwayat.buku_sedang_dipinjam(id_buku):
            return False, f"“{self.judul_buku(id_buku)}” sedang dipinjam, kembalikan dulu sebelum dihapus."
        return True, ""

    def bisa_hapus_anggota(self, id_anggota):
        if self.riwayat.aktif_milik(id_anggota):
            return False, f"{self.nama_anggota(id_anggota)} masih meminjam buku, kembalikan dulu sebelum dihapus."
        return True, ""

    def pinjam(self, id_buku, id_anggota, lama_hari=None):
        """Meminjamkan buku. Mengembalikan (berhasil, pesan).

        lama_hari kosong berarti memakai lama pinjam dari Pengaturan.
        """
        buku = self.perpus.cari_by_id(id_buku)
        anggota = self.anggota.cari_by_id(id_anggota)
        if buku is None:
            return False, "Buku tidak ditemukan."
        if anggota is None:
            return False, "Anggota tidak ditemukan."
        if self.riwayat.buku_sedang_dipinjam(id_buku):
            return False, f"“{buku.judul}” sedang dipinjam."

        milik = self.riwayat.aktif_milik(id_anggota)
        if any(p.hari_terlambat() > 0 for p in milik):
            return False, f"{anggota.nama} masih punya buku yang terlambat dikembalikan."
        batas = self.pengaturan.ambil("maks_pinjam_anggota")
        if len(milik) >= batas:
            return False, f"{anggota.nama} sudah meminjam {batas} buku (batas maksimum)."

        lama = lama_hari or self.pengaturan.ambil("lama_pinjam_hari")
        p = self.riwayat.pinjam(id_buku, id_anggota, lama)
        if p is None:
            return False, f"“{buku.judul}” sedang dipinjam."
        return True, f"“{buku.judul}” dipinjam {anggota.nama}. Jatuh tempo {format_tanggal(p.jatuh_tempo)}."

    def kembalikan(self, id_peminjaman):
        """Mengembalikan buku. Mengembalikan (berhasil, pesan, denda)."""
        p = self.riwayat.cari_by_id(id_peminjaman)
        if p is None or p.sudah_kembali():
            return False, "Peminjaman tidak ditemukan atau sudah dikembalikan.", 0
        self.riwayat.kembalikan(id_peminjaman)
        denda = p.denda(self.pengaturan.ambil("denda_per_hari"))
        pesan = f"“{self.judul_buku(p.id_buku)}” dikembalikan."
        if denda:
            pesan += f" Denda {format_rupiah(denda)} ({p.hari_terlambat()} hari)."
        return True, pesan, denda
