# Program Latihan Membuat Aplikasi Daftar Tugas Sederhana
tugas = []
while True:
    print("\n====== DAFTAR TUGAS ======")
    print("1. Tambah Tugas")
    print("2. Lihat Tugas")
    print("3. Hapus Tugas")
    print("4. Edit Tugas")
    print("5. Tandai Selesai")
    print("6. Cari Tugas")
    print("7. Filter tugas berdasarkan prioritas")
    print("8. Statistik tugas")
    print("9. Keluar")

    pilihan = input("Pilih menu (1/2/3/4/5/6/7/8/9):").strip()
#Pengguna memasukkan tugas
    if pilihan == "1":
        nama_tugas = input("\nMasukkan nama tugas: ").strip()
        deadline = input("Masukkan deadline tugas (YYYY-MM-DD): ").strip()
        print("\nPilihan prioritas tugas:")
        print("1. Tinggi")
        print("2. Sedang")
        print("3. Rendah")
        prioritas_input = input("Masukkan prioritas tugas (1/2/3): ").strip()
        if prioritas_input == "1":
            prioritas = "tinggi"
        elif prioritas_input == "2":
            prioritas = "sedang"
        elif prioritas_input == "3":
            prioritas = "rendah"
        else:
            print("Input tidak valid. Tugas akan diberi prioritas 'sedang'.")
            prioritas = "sedang"
        data_tugas = {
            "nama": nama_tugas,
            "deadline": deadline,
            "status": "belum",
            "prioritas": prioritas
        }
        tugas.append(data_tugas)
        print("Tugas berhasil ditambahkan:", nama_tugas)
#Pengguna melihat daftar tugas
    elif pilihan == "2":
        if not tugas:
            print("Tidak ada tugas yang tersedia")
        else:
            print("\nDaftar Tugas:")
            nomor = 1
            for item in tugas:
                print(nomor,item["nama"],"-",item["status"],"-",item["prioritas"],"-",item["deadline"])
                nomor += 1
#Pengguna menghapus tugas
    elif pilihan == "3":
        try:
            hapus_nomor = int(input("\nMasukkan nomor tugas yang ingin dihapus: ").strip())
            if 1 <= hapus_nomor <= len(tugas):
                index = hapus_nomor - 1
                del tugas[index]
                print("Tugas berhasil dihapus:", hapus_nomor)
            else:
                print("Nomor tugas tidak valid")
        except (IndexError, ValueError):
            print("Input tidak valid. Harap masukkan nomor tugas yang benar.")
#Pengguna mengedit tugas
    elif pilihan == "4":
        try:
            edit_nomor = int(input("\nMasukkan nomor tugas yang ingin diedit: ").strip())
            if 1 <= edit_nomor <= len(tugas):
                index = edit_nomor - 1
                nama_baru = input("Masukkan  nama tugas baru: ").strip()
                tugas[index]["nama"] = nama_baru
                deadline_baru = input("Masukkan deadline tugas baru (YYYY-MM-DD): ").strip()
                tugas[index]["deadline"] = deadline_baru
                print("\nPilihan prioritas tugas:")
                print("1. Tinggi")
                print("2. Sedang")
                print("3. Rendah")
                prioritas_input = input("Masukkan prioritas tugas baru (1/2/3): ").strip()
                if prioritas_input == "1":  
                    tugas[index]["prioritas"] = "tinggi"
                elif prioritas_input == "2":
                    tugas[index]["prioritas"] = "sedang"
                elif prioritas_input == "3":
                    tugas[index]["prioritas"] = "rendah"
                else:
                    print("Input tidak valid. Prioritas tugas tidak diubah.")
                print("Tugas berhasil diedit:", edit_nomor)
            else:
                print("Nomor tugas tidak valid")
        except (IndexError, ValueError):
            print("Tugas gagal diedit. Nomor tugas tidak valid.")
#Pengguna menandai tugas sebagai selesai
    elif pilihan == "5":
        try:
            selesai_nomor = int(input("\nMasukkan nomor tugas yang telah selesai: ").strip())
            if 1 <= selesai_nomor <= len(tugas):
                index = selesai_nomor - 1
                tugas[index]["status"] = "selesai"
                print("Tugas berhasil ditandai sebagai selesai:", selesai_nomor)
            else:
                print("Nomor tugas tidak valid")
        except (IndexError, ValueError):
            print("Tugas gagal ditandai sebagai selesai. Nomor tugas tidak valid.")
#Pengguna mencari tugas
    elif pilihan == "6":
        keyword = input("\nMasukkan keyword tugas yang ingin dicari: ").strip()
        ditemukan = False
        for item in tugas:
            if keyword.lower() in item["nama"].lower():
                print(item["nama"], "-", item["status"], "-", item["deadline"])
                ditemukan = True
        if not ditemukan:
            print("Tugas tidak ditemukan")
#Pengguna memfilter tugas berdasarkan prioritas
    elif pilihan == "7":
        while True:
            print("\nPilihan prioritas tugas:")
            print("1. Tinggi")
            print("2. Sedang")
            print("3. Rendah")
            prioritas_filter = input("Masukkan prioritas tugas (1/2/3): ").strip()
            if prioritas_filter not in ["1", "2", "3"]:
                print("Input tidak valid. Harap masukkan 1, 2, atau 3.")
                continue
            break
        if prioritas_filter == "1":
            prioritas = "tinggi"
        elif prioritas_filter == "2":
            prioritas = "sedang"    
        elif prioritas_filter == "3":
            prioritas = "rendah"
        ditemukan = False
        for item in tugas:
            if item["prioritas"] == prioritas:
                print(item["nama"], "-", item["status"], "-", item["deadline"])
                ditemukan = True
        if not ditemukan:
            print("Tidak ada tugas dengan prioritas", prioritas)
#Pengguna ingin melihat statistik tugas
    elif pilihan == "8":
        print("\n" + "=" * 5 + " STATISTIK TUGAS " + "=" * 5)
        total_tugas = len(tugas)
        print("total tugas: ", total_tugas)
        selesai = 0
        for item in tugas:
            if item["status"] == "selesai":
                selesai += 1
        print("tugas yg selesai: ", selesai)
        belum = total_tugas - selesai 
        print("Tugas yg belum selesai: ", belum)
#Pengguna keluar dari program
    elif pilihan == "9":
        break
    else:
        print("Pilihan tidak tersedia")
