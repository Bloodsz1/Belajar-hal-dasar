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
        judul = input("Judul buku   : ").strip()
        penulis = input("Penulis buku : ").strip()

        if not judul or not penulis:
            print("⚠️  Data tidak boleh kosong!")
            continue

        buku.append([judul, penulis])
        print(f"✅ Buku '{judul}' berhasil ditambahkan!")

    # 2. Melihat daftar buku
    elif pilihan == "2":
        if not buku:
            print("ℹ️  Belum ada koleksi buku di perpustakaan.")
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
            print("ℹ️  Belum ada buku untuk dicari.")
            continue

        dicari = input("Masukkan judul/kata kunci buku: ").lower().strip()
        hasil = [data for data in buku if dicari in data[0].lower()]

        if hasil:
            print(f"\n🔍 Ditemukan {len(hasil)} buku:")
            for index, data in enumerate(hasil, start=1):
                print(f"{index}. {data[0]} (Penulis: {data[1]})")
        else:
            print("❌ Buku tidak ditemukan.")

    # 4. Menghapus buku
    elif pilihan == "4":
        if not buku:
            print("ℹ️  Belum ada buku untuk dihapus.")
            continue

        print("\nDaftar Buku:")
        for index, data in enumerate(buku, start=1):
            print(f"{index}. {data[0]} - {data[1]}")

        try:
            hapus = int(input("\nMasukkan nomor buku yang ingin dihapus: "))
            if 1 <= hapus <= len(buku):
                buku_terhapus = buku.pop(hapus - 1)
                print(f"✅ Buku '{buku_terhapus[0]}' berhasil dihapus!")
            else:
                print("⚠️  Nomor buku tidak tersedia.")
        except ValueError:
            print("⚠️  Harap masukkan nomor dalam bentuk angka!")

    # 5. Keluar dari program
    elif pilihan == "5":
        print("\nTerima kasih telah menggunakan program perpustakaan!")
        break

    else:
        print("⚠️  Pilihan tidak valid, silakan masukkan angka 1 sampai 5.")

