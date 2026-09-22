# Program Latihan Membuat Aplikasi Daftar Tugas Sederhana
tugas = []
while True:
    print("====== DAFTAR TUGAS ======")
    print("1. Tambah Tugas")
    print("2. Lihat Tugas")
    print("3. Hapus Tugas")
    print("4. Edit Tugas")
    print("5. Keluar")

    pilihan = input("pilih menu (1/2/3/4):").strip()
#Pengguna memasukkan tugas
    if pilihan == "1":
        nama_tugas = input("masukkan nama tugas: ").strip()
        tugas.append(nama_tugas)
        print("tugas berhasil ditambahkan:", nama_tugas)
#Pengguna melihat daftar tugas
    elif pilihan == "2":
        if not tugas:
            print("tidak ada tugas yang tersedia")
        else:
            print("daftar tugas:")
            nomor = 1
            for item in tugas:
                print(nomor,item)
                nomor += 1
#Pengguna menghapus tugas
    elif pilihan == "3":
        hapus_nomor = int(input("masukkan nomor tugas yang ingin dihapus: ").strip())
        if hapus_nomor <= len(tugas):
            index = hapus_nomor - 1
            del tugas[index]
            print("tugas berhasil dihapus:", hapus_nomor)
        else:
            print("nomor tugas tidak valid")
#Pengguna mengedit tugas
    elif pilihan == "4":
        edit_nomor = int(input("masukkan nomor tugas yang ingin diedit: ").strip())
        index = edit_nomor - 1
        nama_baru = input("masukkan nama tugas baru: ").strip()
        tugas[index] = nama_baru
        print("tugas berhasil diedit:", edit_nomor)
#Pengguna keluar dari program
    elif pilihan == "5":
        break
    else:
        print("pilihan tidak tersedia")

    

