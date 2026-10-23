import json
import os
from pathlib import Path

FILE_BUKU = Path(__file__).resolve().parent / "buku.json"

def muat_buku():
    """Membaca data buku dari file JSON."""
    if not FILE_BUKU.exists():
        return []

    try:
        with open(FILE_BUKU, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Memastikan format data sesuai
        if not isinstance(data, list):
            raise ValueError("Format data harus berupa list.")

        for buku in data:
            if (
                not isinstance(buku, list)
                or len(buku) != 2
                or not all(isinstance(item, str) for item in buku)
            ):
                raise ValueError("Format data buku tidak valid.")

        return data

    except (json.JSONDecodeError, ValueError, OSError) as error:
        print(f"Gagal membaca data buku: {error}")
        print("Periksa file buku.json sebelum melanjutkan.")
        raise SystemExit(1)


def simpan_buku(daftar_buku):
    """Menyimpan daftar buku ke file JSON."""
    file_sementara = FILE_BUKU.with_suffix(".tmp")

    try:
        with open(file_sementara, "w", encoding="utf-8") as file:
            json.dump(daftar_buku, file, indent=4, ensure_ascii=False)

        # Mengganti file lama setelah penulisan selesai
        os.replace(file_sementara, FILE_BUKU)
        return True

    except (OSError, TypeError, ValueError) as error:
        print(f"Gagal menyimpan data: {error}")
        return False
def tampilkan_menu():
    ''' Funsi tampilkan menu '''
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
def tambah_buku(daftar_buku):
    ''' Fungsi tambah buku '''
    judul = input('Judul buku: ').lower().strip()
    penulis = input('Penulis buku: ').lower().strip()

    if judul == "" or penulis == "" :
        print ("data tidak boleh kosong")
        return False
    else:
        data_buku = [judul, penulis]
        daftar_buku.append(data_buku)
        print(f"Buku '{judul}' berhasil ditambahkan!")
        return True
def melihat_buku(daftar_buku):
    ''' Fungsi melihat buku'''
    print("\n","="*10,"Data buku: ","="*10,"\n")
    if not daftar_buku:
        print("Belum ada koleksi buku di perpustakaan.")
        return 
    else:
        print("\n" + "=" * 50)
        print(f"{'No':<4} | {'Judul Buku':<25} | {'Penulis':<15}")
        print("-" * 50)
        for index, data in enumerate(daftar_buku, start=1):
            print(f"{index:<4} | {data[0]:<25} | {data[1]:<15}")
        print("=" * 50)
def mencari_buku(daftar_buku):
    if not daftar_buku:
        print("Belum ada buku untuk dicari.")
        return False
    dicari = input("Masukkan judul/kata kunci buku: ").lower().strip()
    if not dicari:
        return
    hasil = [data for data in daftar_buku if dicari in data[0].lower()]
    if hasil:
        print(f"\nDitemukan {len(hasil)} buku:")
        for index, data in enumerate(hasil, start=1):
            print(f"{index}. {data[0]} (Penulis: {data[1]})")
    else:
        print("Buku tidak ditemukan.")
def hapus_buku(daftar_buku):
    if not daftar_buku:
        print("Belum ada buku untuk dihapus")
        return False
    else:
        print("\nDaftar Buku:")
    for index, data in enumerate(daftar_buku, start=1):
        print(f"{index}. {data[0]} - {data[1]}")

    try:
        hapus = int(input("\nMasukkan nomor buku yang ingin dihapus: "))
        if 1 <= hapus <= len(daftar_buku):
            buku_terhapus = daftar_buku.pop(hapus - 1)
            print(f"Buku '{buku_terhapus[0]}' berhasil dihapus!")
        else:
            print("Masukkan nomor yang tepat!")
    except ValueError:
        print("Harap masukkan nomor dalam bentuk angka!")
        return False
def edit_buku(daftar_buku):  
    if not daftar_buku:
        print("Belum ada buku untuk diedit")
        return False
    else:    
        print("\nDaftar Buku:")
    for index, data in enumerate(daftar_buku, start=1):
        print(f"{index}. {data[0]} - {data[1]}")
    try:
        edit = int(input("\nMasukkan nomor buku yang ingin diedit: "))
        if 1 <= edit <= len(daftar_buku):
            index_buku = edit - 1
            print("\nTekan enter jika ingin mempertahankan data lama")

            judul_baru = input("Masukkan judul buku yg baru").strip()
            penulis_baru = input("Masukkan nama penulis baru king").strip()

            if judul_baru:
                daftar_buku[index_buku][0]= judul_baru
            if penulis_baru:
                daftar_buku[index_buku][1]= penulis_baru
                    
            print(f"Buku {daftar_buku[index_buku][0]} berhasil diedit")
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
    buku = muat_buku()

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        tampilkan_menu()
        pilihan = input("Masukkan pilihan (1-6): ").strip()

        # 1. Menambahkan buku
        if pilihan == "1":
            if tambah_buku(buku):
                simpan_buku(buku)
            tunggu_enter()
        # 2. Melihat daftar buku
        elif pilihan == "2":
            melihat_buku(buku)
            tunggu_enter()
        # 3. Mencari buku
        elif pilihan == "3":
            mencari_buku(buku)
            tunggu_enter()
        # 4. Menghapus buku
        elif pilihan == "4":
            if hapus_buku(buku):
                simpan_buku(buku)
            tunggu_enter()
        # 5. Mengedit buku
        elif pilihan == "5":
            if edit_buku(buku):
                simpan_buku(buku)
            tunggu_enter()
        # 6. Keluar dari program
        elif pilihan == "6":
            keluar_program()
            break
        else:
            print ("Menu tidak ditemukan")
            tunggu_enter()

    print ("Program selesai")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram dihentikan.")