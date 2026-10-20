import os
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
    else:
        data_buku = [judul, penulis]
        daftar_buku.append(data_buku)
        print(f"Buku '{judul}' berhasil ditambahkan!")
def melihat_buku(daftar_buku):
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
        return
    dicari = input("Masukkan judul/kata kunci buku: ").lower().strip()
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
        return
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
def edit_buku(daftar_buku):  
    if not daftar_buku:
        print("Belum ada buku untuk diedit")
        return
    else:    
        print("\nDaftar Buku:")
    for index, data in enumerate(daftar_buku, start=1):
        print(f"{index}. {data[0]} - {data[1]}")
    try:
        edit = int(input("\nMasukkan nomor buku yang ingin diedit: "))
        if 1 <= edit <= len(daftar_buku):
            index_buku = edit - 1
            print("\nTekan enter jika ingin memperhatikan data lama")

            judul_baru = input("Masukkan judul buku yg baru").strip()
            penulis_baru = input("Masukkan nama penulis baru king").strip()

            if judul_baru:
                daftar_buku[index_buku][0]= judul_baru
            if penulis_baru:
                daftar_buku[index_buku][1]= penulis_baru
                    
            print(f"Buku {daftar_buku[index_buku[0]]} berhasil diedit")
        else:
            print("Buku tidak ditemukan")
                    
    except ValueError:
        print("Harap masukkan nomor buku dengan benar")
def keluar_program(daftar_buku):    
    if daftar_buku == "6":
        print("\nTerima kasih telah menggunakan program perpustakaan!")
    else :
        print ("pilihan tidak tersedia")

buku = []

while True:
    os._system("clear")
    tampilkan_menu()
    pilihan = input("Masukkan pilihan (1-6): ").strip()

    # 1. Menambahkan buku
    if pilihan == "1":
        tambah_buku(buku)
    # 2. Melihat daftar buku
    elif pilihan == "2":
        melihat_buku(buku)
    # 3. Mencari buku
    elif pilihan == "3":
        mencari_buku(buku)
    # 4. Menghapus buku
    elif pilihan == "4":
        hapus_buku(buku)
    # 5. Mengedit buku
    elif pilihan == "5":
        edit_buku(buku)
    # 6. Keluar dari program
    elif pilihan == "6":
        keluar_program(buku)
        break
print ("Program selesai")