"""halaman_peminjaman.py - Halaman Peminjaman: catat pinjam, kembalikan buku, lihat riwayat."""

from tkinter import messagebox

from komponen import MUTED, DialogForm, Halaman, Lencana, TabelKartu
from util import format_id, format_rupiah, format_tanggal

SEMUA_STATUS = "Semua status"
STATUS = [SEMUA_STATUS, "Dipinjam", "Terlambat", "Dikembalikan"]


class HalamanPeminjaman(Halaman):
    placeholder = "Cari judul buku atau nama anggota…"

    def __init__(self, induk, app):
        super().__init__(induk, app)
        self.riwayat = self.layanan.riwayat
        self.filter_status = SEMUA_STATUS
        isi = self.kerangka("Peminjaman", "Peminjaman", "+   Pinjam Buku", self.tambah)
        kolom = [
            {"judul": "Buku", "lebar": 0, "teks": lambda p: self.layanan.judul_buku(p.id_buku)},
            {"judul": "Anggota", "lebar": 170, "teks": lambda p: self.layanan.nama_anggota(p.id_anggota)},
            {"judul": "Dipinjam", "lebar": 110, "teks": lambda p: format_tanggal(p.tgl_pinjam), "warna": MUTED},
            {"judul": "Jatuh tempo", "lebar": 110, "teks": lambda p: format_tanggal(p.jatuh_tempo), "warna": MUTED},
            {"judul": "Dikembalikan", "lebar": 120,
             "teks": lambda p: format_tanggal(p.tgl_kembali) if p.sudah_kembali() else "-", "warna": MUTED},
            {"judul": "Status", "lebar": 120, "sel": self._sel_status},
            {"judul": "Denda", "lebar": 100, "teks": self._teks_denda},
        ]
        self.tabel = TabelKartu(
            isi, app, "Riwayat Peminjaman", kolom, self._data, lambda p: p.id,
            aksi=[("kembali", self._kembalikan, lambda p: not p.sudah_kembali())],
            opsi_filter=STATUS, saat_filter=self._saat_filter,
            hitung_semua=lambda: len(self.riwayat.semua_peminjaman()), satuan="peminjaman",
            kosong=("Belum ada peminjaman", "Catat peminjaman pertama lewat tombol “Pinjam Buku”."),
            tombol_kosong=("+   Pinjam Buku", self.tambah))
        self.tabel.pack(fill="both", expand=True, pady=(20, 0))

    # ------------------------------------------------------------------ data
    def _data(self):
        urut = sorted(self.riwayat.semua_peminjaman(), key=lambda p: p.id, reverse=True)
        if self.filter_status != SEMUA_STATUS:
            urut = [p for p in urut if p.status() == self.filter_status]
        kata = self.kata_kunci.strip().lower()
        if kata:
            urut = [p for p in urut
                    if kata in self.layanan.judul_buku(p.id_buku).lower()
                    or kata in self.layanan.nama_anggota(p.id_anggota).lower()]
        return urut

    def _sel_status(self, sel, p, bg):
        Lencana(sel, p.status(), self.f.small, bg).place(x=6, rely=0.5, anchor="w")

    def _teks_denda(self, p):
        denda = p.denda(self.layanan.pengaturan.ambil("denda_per_hari"))
        return format_rupiah(denda) if denda else "-"

    def segarkan(self):
        self.tabel.render()

    def cari(self, teks):
        self.kata_kunci = teks
        self.tabel.reset()

    def _saat_filter(self, nilai):
        self.filter_status = nilai

    # ------------------------------------------------------------- pinjam
    def tambah(self):
        buku = self.layanan.buku_tersedia()
        anggota = self.layanan.anggota.semua_anggota()
        if not self.layanan.perpus.semua_buku():
            messagebox.showinfo("Belum ada buku", "Tambahkan buku dulu di halaman Perpustakaan.",
                                parent=self.app.root)
            return
        if not buku:
            messagebox.showinfo("Semua buku sedang dipinjam", "Tidak ada buku yang tersedia saat ini.",
                                parent=self.app.root)
            return
        if not anggota:
            messagebox.showinfo("Belum ada anggota", "Tambahkan anggota dulu di halaman Anggota.",
                                parent=self.app.root)
            return

        peta_buku = {f"{b.judul}  ({format_id(b.id)})": b.id for b in buku}
        peta_anggota = {f"{a.nama}  ({a.kode})": a.id for a in anggota}
        lama = self.layanan.pengaturan.ambil("lama_pinjam_hari")
        medan = [
            {"kunci": "buku", "label": "Buku (hanya yang tersedia)", "jenis": "pilihan",
             "pilihan": list(peta_buku), "nilai": list(peta_buku)[0]},
            {"kunci": "anggota", "label": "Anggota", "jenis": "pilihan",
             "pilihan": list(peta_anggota), "nilai": list(peta_anggota)[0]},
            {"kunci": "lama", "label": "Lama pinjam (hari)", "nilai": lama},
        ]

        def validasi(v):
            if v["buku"] not in peta_buku:
                return None, "Pilih buku dari daftar."
            if v["anggota"] not in peta_anggota:
                return None, "Pilih anggota dari daftar."
            try:
                hari = int(v["lama"])
            except ValueError:
                return None, "Lama pinjam harus berupa angka."
            if not 1 <= hari <= 90:
                return None, "Lama pinjam harus antara 1 dan 90 hari."
            return {"id_buku": peta_buku[v["buku"]], "id_anggota": peta_anggota[v["anggota"]],
                    "lama": hari}, ""

        DialogForm(self.app, "Pinjam Buku", medan, validasi, self._simpan_pinjam,
                   keterangan="Jatuh tempo dihitung dari hari ini.", teks_simpan="Pinjamkan")

    def _simpan_pinjam(self, data):
        # BACKEND: Layanan.pinjam() memeriksa semua aturan sebelum mencatat
        ok, pesan = self.layanan.pinjam(data["id_buku"], data["id_anggota"], data["lama"])
        if not ok:
            return False, pesan
        self.app.simpan(self.layanan.simpan_peminjaman)
        self.filter_status = SEMUA_STATUS
        self.tabel.atur_filter(SEMUA_STATUS)
        self.kata_kunci = ""
        self.app.set_cari("")
        self.tabel.reset()
        self.app.toast(pesan)
        return True, ""

    # ---------------------------------------------------------- kembalikan
    def _kembalikan(self, p):
        judul = self.layanan.judul_buku(p.id_buku)
        isi = f"Terima pengembalian “{judul}” dari {self.layanan.nama_anggota(p.id_anggota)}?"
        denda = p.denda(self.layanan.pengaturan.ambil("denda_per_hari"))
        if denda:
            isi += f"\n\nTerlambat {p.hari_terlambat()} hari. Denda {format_rupiah(denda)}."
        if not messagebox.askyesno("Kembalikan buku", isi, parent=self.app.root):
            return
        ok, pesan, _ = self.layanan.kembalikan(p.id)  # BACKEND: hitung denda & tandai kembali
        if ok:
            self.app.simpan(self.layanan.simpan_peminjaman)
        self.tabel.render()
        self.app.toast(pesan)

