buku = []

while True:
    
    print("\n" + "=" * 35)
    print("       SISTEM PERPUSTAKAAN")
    print("=" * 35)
    print("1. Tambah Buku")
    print("2. Lihat Semua Buku")
    print("3. Cari Buku")
    print("4. Hapus Buku")
    print("5. Keluar")
    print("=" * 35)

    pilihan = input("Masukkan pilihan (1-5): ").strip()

    # 1. Menambahkan buku
    if pilihan == "1":
        judul = input('Judul buku: ').lower().strip()
        penulis = input('Penulis buku: ').lower().strip()

        if judul == "" or penulis == "" :
            print ("data tidak boleh kosong")
            continue

        data_buku = [judul, penulis]
        buku.append(data_buku)
        print(f"Buku '{judul}' berhasil ditambahkan!")

    # 2. Melihat daftar buku
    elif pilihan == "2":
        print("\n","="*10,"Data buku: ","="*10,"\n")
        if not buku:
            print("Belum ada koleksi buku di perpustakaan.")

    # 3. Mencari buku
    elif pilihan == "3":
        if not buku:
            print("ℹ️  Belum ada buku untuk dicari.")
            continue
    # 4. Menghapus buku
    elif pilihan == "4":
        if not buku:
            print("Belum ada buku untuk dihapus")
            continue

        print("\nDaftar Buku:")
        for index, data in enumerate(buku, start=1):
            print(f"{index}. {data[0]} - {data[1]}")

        try:
            hapus = int(input("\nMasukkan nomor buku yang ingin dihapus: "))
            if 1 <= hapus <= len(buku):
                buku_terhapus = buku.pop(hapus - 1)
                print(f"Buku '{buku_terhapus[0]}' berhasil dihapus!")
            else:
                print("Nomor buku tidak tersedia")
        except ValueError:
            print("Harap masukkan nomor dalam bentuk angka!")

    # 5. Keluar dari program
    elif pilihan == "5":
        print("\nTerima kasih telah menggunakan program perpustakaan!")
        break
    else :
        print ("pilihan tidak tersedia")

print ("Program selesai")
