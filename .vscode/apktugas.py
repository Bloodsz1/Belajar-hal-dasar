# Program Latihan Membuat Aplikasi Daftar Tugas Sederhana
tugas = []
while True:
    print("====== DAFTAR TUGAS ======")
    print("1. Tambah Tugas")
    print("2. Lihat Tugas")
    print("3. Hapus Tugas")
    print("4. Edit Tugas")
    print("5. Tandai Selesai")
    print("6. Keluar")

    pilihan = input("pilih menu (1/2/3/4/5/6):").strip()
#Pengguna memasukkan tugas
    if pilihan == "1":
        nama_tugas = input("masukkan nama tugas: ").strip()
        data_tugas = {
            "nama": nama_tugas,
            "status": "belum"
                      }
        tugas.append(data_tugas)
        print("tugas berhasil ditambahkan:", nama_tugas)
#Pengguna melihat daftar tugas
    elif pilihan == "2":
        if not tugas:
            print("tidak ada tugas yang tersedia")
        else:
            print("daftar tugas:")
            nomor = 1
            for item in tugas:
                print(nomor,item["nama"],"-",item["status"])
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
        tugas[index]["nama"] = nama_baru
        print("tugas berhasil diedit:", edit_nomor)
#Pengguna menandai tugas sebagai selesai
    elif pilihan == "5":
        selesai_nomor = int(input("masukkan nomor tugas yang telah selesai: ").strip())
        index = selesai_nomor - 1
        tugas[index]["status"] = "selesai"
        print("tugas berhasil ditandai sebagai selesai:", selesai_nomor)
#Pengguna keluar dari program
    elif pilihan == "6":
        break
    else:
        print("pilihan tidak tersedia")

    

