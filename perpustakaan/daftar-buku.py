import os
from pathlib import Path
from models import Buku, Perpustakaan

FILE_BUKU = Path(__file__).resolve().parent / "perpustakaan.json"

def tampilkan_menu():
    """Funsi tampilkan menu"""
    print("\n" + "=" * 35)
    print("       SISTEM PERPUSTAKAAN")
    print("=" * 35)
    print("1. Tambah Buku")
    print("2. Lihat Semua Buku")
    print("3. Cari Buku")
    print("4. Hapus Buku")
    print("5. Edit Buku")
    print("6. Keluar")
    print("=" * 35)


def tambah_buku(perpustakaan):
    """Fungsi tambah buku"""
    judul = input("Judul buku: ").lower().strip()
    penulis = input("Penulis buku: ").lower().strip()
    subjek = input("Subjek buku: ").lower().strip()
    try:
        tahun_terbit = int(input("Tahun terbit buku: ").strip())
    except ValueError:
        print("Tahun harus berupa angka!")
        return False
    if judul == "" or penulis == "" or subjek == "":
        print("data tidak boleh kosong")
        return False
    buku = Buku(perpustakaan.id_berikutnya(), judul, penulis, subjek, tahun_terbit)
    if perpustakaan.tambah_buku(buku):
        print(f"Buku '{judul}' berhasil ditambahkan!")
        return True
    return False


def melihat_buku(perpustakaan):
    """Fungsi melihat buku"""
    print("\n", "=" * 10, "Data buku: ", "=" * 10, "\n")
    if not perpustakaan.semua_buku():
        print("Belum ada koleksi buku di perpustakaan.")
        return
    else:
        print("\n" + "=" * 50)
        print(f"{'No':<4} | {'Judul Buku':<25} | {'Penulis':<15}")
        print("-" * 50)
        for index, buku in enumerate(perpustakaan.semua_buku(), start=1):
            print(f"{index:<4} | {buku.judul:<25} | {buku.penulis:<15}")
        print("=" * 50)


def mencari_buku(perpustakaan):
    if not perpustakaan.semua_buku():
        print("Belum ada buku untuk dicari.")
        return False
    dicari = input("Masukkan judul/kata kunci buku: ").lower().strip()
    if not dicari:
        return
    hasil = [buku for buku in perpustakaan.semua_buku() if dicari in buku.judul.lower()]
    if hasil:
        print(f"\nDitemukan {len(hasil)} buku:")
        for index, buku in enumerate(hasil, start=1):
            print(f"{index}. {buku.judul} (Penulis: {buku.penulis})")
    else:
        print("Buku tidak ditemukan.")


def hapus_buku(perpustakaan):
    if not perpustakaan.semua_buku():
        print("Belum ada buku untuk dihapus")
        return False
    else:
        print("\nDaftar Buku:")
    for index, buku in enumerate(perpustakaan.semua_buku(), start=1):
        print(f"{index}. {buku.judul} - {buku.penulis}")

    try:
        hapus = int(input("\nMasukkan nomor buku yang ingin dihapus: "))
        if 1 <= hapus <= len(perpustakaan.semua_buku()):
            buku_terhapus = perpustakaan.semua_buku()[hapus - 1]
            perpustakaan.hapus_buku(buku_terhapus.id)
            print(f"Buku '{buku_terhapus.judul}' berhasil dihapus!")
            return True
        else:
            print("Masukkan nomor yang tepat!")
    except ValueError:
        print("Harap masukkan nomor dalam bentuk angka!")
        return False


def edit_buku(perpustakaan):
    if not perpustakaan.semua_buku():
        print("Belum ada buku untuk diedit")
        return False
    else:
        print("\nDaftar Buku:")
    for index, buku in enumerate(perpustakaan.semua_buku(), start=1):
        print(f"{index}. {buku.judul} - {buku.penulis}")
    try:
        edit = int(input("\nMasukkan nomor buku yang ingin diedit: "))
        if 1 <= edit <= len(perpustakaan.semua_buku()):
            index_buku = edit - 1
            print("\nTekan enter jika ingin mempertahankan data lama")

            judul_baru = input("Masukkan judul buku yg baru: ").strip()
            penulis_baru = input("Masukkan nama penulis barunya king: ").strip()

            if judul_baru:
                perpustakaan.semua_buku()[index_buku].judul = judul_baru
            if penulis_baru:
                perpustakaan.semua_buku()[index_buku].penulis = penulis_baru

            print(f"Buku {perpustakaan.semua_buku()[index_buku].judul} berhasil diedit")
            return True
        else:
            print("Buku tidak ditemukan")
            return False

    except ValueError:
        print("Harap masukkan nomor buku dengan benar")
        return False


def keluar_program():
    print("\nTerima kasih telah menggunakan program perpustakaan!")


def tunggu_enter():
    input("\nTekan Enter untuk kembali ke menu...")


def main():
    perpustakaan = Perpustakaan()
    perpustakaan.muat(FILE_BUKU)

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        tampilkan_menu()
        pilihan = input("Masukkan pilihan (1-6): ").strip()

        # 1. Menambahkan buku
        if pilihan == "1":
            if tambah_buku(perpustakaan):
                perpustakaan.simpan(FILE_BUKU)
            tunggu_enter()
        # 2. Melihat daftar buku
        elif pilihan == "2":
            melihat_buku(perpustakaan)
            tunggu_enter()
        # 3. Mencari buku
        elif pilihan == "3":
            mencari_buku(perpustakaan)
            tunggu_enter()
        # 4. Menghapus buku
        elif pilihan == "4":
            if hapus_buku(perpustakaan):
                perpustakaan.simpan(FILE_BUKU)
            tunggu_enter()
        # 5. Mengedit buku
        elif pilihan == "5":
            if edit_buku(perpustakaan):
                perpustakaan.simpan(FILE_BUKU)
            tunggu_enter()
        # 6. Keluar dari program
        elif pilihan == "6":
            keluar_program()
            break
        else:
            print("Menu tidak ditemukan")
            tunggu_enter()

    print("Program selesai")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram dihentikan.")
