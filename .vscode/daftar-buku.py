buku = []

while True:
    
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

    pilihan = input("Masukkan pilihan (1-6): ").strip()

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
        else:
            print("\n" + "=" * 50)
            print(f"{'No':<4} | {'Judul Buku':<25} | {'Penulis':<15}")
            print("-" * 50)
            for index, data in enumerate(buku, start=1):
                print(f"{index:<4} | {data[0]:<25} | {data[1]:<15}")
            print("=" * 50)

    # 3. Mencari buku
    elif pilihan == "3":
        if not buku:
            print("Belum ada buku untuk dicari.")
            continue
        dicari = input("Masukkan judul/kata kunci buku: ").lower().strip()
        hasil = [data for data in buku if dicari in data[0].lower()]

        if hasil:
            print(f"\nDitemukan {len(hasil)} buku:")
            for index, data in enumerate(hasil, start=1):
                print(f"{index}. {data[0]} (Penulis: {data[1]})")
        else:
            print("Buku tidak ditemukan.")
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
        except ValueError:
            print("Harap masukkan nomor dalam bentuk angka!")

    # 5. Mengedit buku
    elif pilihan == "5":
        if not buku:
            print("Belum ada buku untuk diedit")
            continue
        
        print("\nDaftar Buku:")
        for index, data in enumerate(buku, start=1):
            print(f"{index}. {data[0]} - {data[1]}")
        try:
            edit = int(input("\nMasukkan nomor buku yang ingin diedit: "))
            if 1 <= edit <= len(buku):
                index_buku = edit - 1
                print("\nTekan enter jika ingin memperhatikan data lama")

                judul_baru = input("Masukkan judul buku yg baru").strip()
                penulis_baru = input("Masukkan nama penulis baru king").strip()

                if judul_baru:
                    buku[index_buku][0]= judul_baru
                if penulis_baru:
                    buku[index_buku][1]= penulis_baru
                    
                print(f"Buku {judul_baru} berhasil diedit")
            else:
                print("Buku tidak ditemukan")
                    
        except ValueError:
            print("Harap masukkan nomor buku dengan benar")

    # 6. Keluar dari program
    elif pilihan == "6":
        print("\nTerima kasih telah menggunakan program perpustakaan!")
        break
    else :
        print ("pilihan tidak tersedia")

print ("Program selesai")