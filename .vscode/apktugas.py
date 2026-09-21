
tugas = []
while True:
    print("====== DAFTAR TUGAS ======")
    print("1. Tambah Tugas")
    print("2. Lihat Tugas")
    print("3. Hapus Tugas")
    print("4. Keluar")

    pilihan = input("pilih menu (1/2/3/4):").strip()
    if pilihan == "1":
        nama_tugas = input("masukkan nama tugas: ").strip()
        tugas.append(nama_tugas)
        print("tugas berhasil ditambahkan:", nama_tugas)
    elif pilihan == "2":
        if not tugas:
            print("tidak ada tugas yang tersedia")
        else:
            print("daftar tugas:")
            nomor = 1
            for item in tugas:
                print(nomor,item)
                nomor += 1
    elif pilihan == "3":
        hapus_nomor = int(input("masukkan nomor tugas yang ingin dihapus: ").strip())
        index = hapus_nomor - 1
        del tugas[index]
        print("tugas berhasil dihapus:", hapus_nomor)
    elif pilihan == "4":
        break
    else:
        print("pilihan tidak tersedia")
    

