class Buku:
    def __init__(self, id, judul, penulis, subjek, tahun_terbit):
        self.id = id
        self.judul = judul
        self.penulis = penulis
        self.subjek = subjek
        self.tahun_terbit = tahun_terbit

    def __str__(self):
        return f"{self.judul} - {self.penulis} ({self.tahun_terbit})"

    def ke_dict(self):
        return {
            "id": self.id,
            "judul": self.judul,
            "penulis": self.penulis,
            "subjek": self.subjek,
            "tahun_terbit": self.tahun_terbit,
        }


class Perpustakaan:
    def __init__(self):
        self.daftar_buku = []

    def tambah_buku(self, buku):
        if self.cari_by_id(buku.id) is not None:
            return False

        self.daftar_buku.append(buku)
        return True

    def semua_buku(self):
        return self.daftar_buku

    def cari_by_id(self, id):
        for buku in self.daftar_buku:
            if buku.id == id:
                return buku  # ketemu, langsung keluar
        return None  # sampai habis tidak ketemu

    def cari_by_judul(self, kata):
        return [buku for buku in self.daftar_buku if kata.lower() in buku.judul.lower()]

    def hapus_buku(self, id):
        buku = self.cari_by_id(id)
        if buku is None:
            return False  # tidak ada yang dihapus
        self.daftar_buku.remove(buku)  # hapus objek itu dari list
        return True

    def edit_buku(self, id, judul=None, penulis=None, subjek=None, tahun_terbit=None):
        buku = self.cari_by_id(id)
        if buku is None:
            return False  # buku tidak ada

        if judul is not None:
            buku.judul = judul
        if penulis is not None:
            buku.penulis = penulis
        if subjek is not None:
            buku.subjek = subjek
        if tahun_terbit is not None:
            buku.tahun_terbit = tahun_terbit
        return True


if __name__ == "__main__":
    # semua kode tes ditulis menjorok (indentasi) di sini
    perpustakaan = Perpustakaan()
    perpustakaan.tambah_buku(Buku(1, "Bumi", "Tere Liye", "Fiksi", 2013))
    perpustakaan.tambah_buku(Buku(2, "Bulan", "Tere Liye", "Fiksi", 2014))
    perpustakaan.tambah_buku(Buku(3, "Matahari", "Tere Liye", "Fiksi", 2015))
    perpustakaan.tambah_buku(Buku(4, "Bintang", "Tere Liye", "Fiksi", 2016))
    for buku in perpustakaan.semua_buku():
        d = perpustakaan.cari_by_id(2).ke_dict()
        print(d)
        salinan = Buku(**d)
        print(salinan)
        print(buku)
