class Buku:
    def __init__(self, id, judul, penulis, subjek, tahun_terbit):
        self.id = id
        self.judul = judul
        self.penulis = penulis
        self.subjek = subjek
        self.tahun_terbit = tahun_terbit

    def __str__(self):
        return f"{self.judul} - {self.penulis} ({self.tahun_terbit})"


class Perpustakaan:
    def __init__(self):
        self.daftar_buku = []

    def tambah_buku(self, buku):
        self.daftar_buku.append(buku)

    def semua_buku(self):
        return self.daftar_buku

    def cari_by_id(self, id):
        for buku in self.daftar_buku:
            if buku.id == id:
                return buku  # ketemu, langsung keluar
        return None  # sampai habis tidak ketemu


if __name__ == "__main__":
    # semua kode tes ditulis menjorok (indentasi) di sini
    perpustakaan = Perpustakaan()
    perpustakaan.tambah_buku(Buku(1, "Bumi", "Tere Liye", "Fiksi", 2013))
    perpustakaan.tambah_buku(Buku(2, "Bulan", "Tere Liye", "Fiksi", 2014))
    for buku in perpustakaan.semua_buku():
        print(buku)
