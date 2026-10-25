# Program Latihan Membuat Aplikasi Daftar Tugas Sederhana
from datetime import datetime
from pathlib import Path
import os
import json

FILE_TUGAS = Path(__file__).resolve().parent / "tugas.json"

def muat_tugas():
    """Membaca data tugas dari file JSON."""
    if not FILE_TUGAS.exists():
        return []

    try:
        with open(FILE_TUGAS, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Memastikan format data sesuai
        if not isinstance(data, list):
            raise ValueError("Format data harus berupa list.")

        for tugas in data:
            for item in data:
                if not isinstance(item, dict):
                    raise ValueError("Format data tugas tidak valid.")

        return data

    except (json.JSONDecodeError, ValueError, OSError) as error:
        print(f"Gagal membaca data tugas: {error}")
        print("Periksa file tugas.json sebelum melanjutkan.")
        raise SystemExit(1)
def simpan_tugas(daftar_tugas):
    """Menyimpan daftar tugas ke file JSON."""
    file_sementara = FILE_TUGAS.with_suffix(".tmp")

    try:
        with open(file_sementara, "w", encoding="utf-8") as file:
            json.dump(daftar_tugas, file, indent=4, ensure_ascii=False)

        # Mengganti file lama setelah penulisan selesai
        os.replace(file_sementara, FILE_TUGAS)
        return True

    except (OSError, TypeError, ValueError) as error:
        print(f"Gagal menyimpan data: {error}")
        return False
def tunggu_enter():
    input("\nTekan enter untuk kembali ke menu")
def bersihkan_terminal():
    os.system("cls" if os.name == "nt" else "clear")
tugas = muat_tugas()

while True:
    bersihkan_terminal()
    print("\n"*2)
    print("\n====== DAFTAR TUGAS ======")
    print("1.  Tambah Tugas")
    print("2.  Lihat Tugas")
    print("3.  Hapus Tugas")
    print("4.  Edit Tugas")
    print("5.  Tandai Selesai")
    print("6.  Cari Tugas")
    print("7.  Filter tugas berdasarkan prioritas")
    print("8.  Filter tugas berdasarkan status")
    print("9.  Statistik tugas")
    print("10. Batalkan status selesai")
    print("11. Keluar")

    pilihan = input("Pilih menu (1-11):").strip()
#Pengguna memasukkan tugas
    if pilihan == "1":
        nama_tugas = input("\nMasukkan nama tugas: ").strip()
        if not nama_tugas:
            print("nama tugas tidak boleh kosong")
            tunggu_enter()
            continue
        while True:
            deadline_input = input("Masukkan deadline tugas (YYYY-MM-DD): ").strip()
            try:
                deadline = datetime.strptime(deadline_input, "%Y-%m-%d").date().isoformat()
                break
            except ValueError:
                print("Format tanggal tidak valid. Harap masukkan dalam format YYYY-MM-DD.")
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
        simpan_tugas(tugas)
        print("Tugas berhasil ditambahkan:", nama_tugas)
        tunggu_enter()
        continue

#Pengguna melihat daftar tugas
    elif pilihan == "2":
        if not tugas:
            print("Tidak ada tugas yang tersedia")
        else:
            print(f"\nDaftar Tugas (Total: {len(tugas)}):")
            print("\nDaftar Tugas:")
            nomor = 1
            for item in tugas:
                print(nomor,item["nama"],"-",item["status"],"-",item["prioritas"],"-",item["deadline"])
                nomor += 1
        tunggu_enter()
        continue
#Pengguna menghapus tugas
    elif pilihan == "3":
        try:
            if not tugas:
                print("Tidak ada tugas yang tersedia")
                tunggu_enter()
                continue
            else:
                print(f"\nDaftar Tugas (Total: {len(tugas)}):")
                print("\nDaftar Tugas:")
                nomor = 1
                for item in tugas:
                    print(nomor,item["nama"],"-",item["status"],"-",item["prioritas"],"-",item["deadline"])
                    nomor += 1
            hapus_nomor = int(input("\nMasukkan nomor tugas yang ingin dihapus: ").strip())
            if 1 <= hapus_nomor <= len(tugas):
                index = hapus_nomor - 1
                yakin = input("Apakah Anda yakin ingin menghapus tugas ini? (y/n): ").strip().lower()
                if yakin == 'y':
                    del tugas[index]
                    simpan_tugas(tugas)
                    print("Tugas berhasil dihapus:", hapus_nomor)
                else:
                    print("Penghapusan tugas dibatalkan.")
            else:
                print("Nomor tugas tidak valid")
        except (IndexError, ValueError):
            print("Input tidak valid. Harap masukkan nomor tugas yang benar.")
        tunggu_enter()
        continue
#Pengguna mengedit tugas
    elif pilihan == "4":
        try:
            if tugas:
                print(f"\nDaftar Tugas (Total: {len(tugas)}):")
                print("\nDaftar Tugas:")
                nomor = 1
                for item in tugas:
                    print(nomor,item["nama"],"-",item["status"],"-",item["prioritas"],"-",item["deadline"])
                    nomor += 1
            else :
                print("Tugas belum ditambahkan")
            edit_nomor = int(input("\nMasukkan nomor tugas yang ingin diedit: ").strip())
            if 1 <= edit_nomor <= len(tugas):
                index = edit_nomor - 1
                nama_baru = input("Masukkan  nama tugas baru: ").strip()
                if not nama_baru:
                    print("Nama tugas dikosongkan. nama lama dipertahankan.")
                else:
                    tugas[index]["nama"] = nama_baru
                while True:
                    deadline_baru_input = input("Masukkan deadline tugas baru (YYYY-MM-DD): ").strip()
                    try:
                        deadline_baru = datetime.strptime(deadline_baru_input, "%Y-%m-%d").date().isoformat()
                        break
                    except ValueError:
                        print("Format tanggal tidak valid. Harap masukkan dalam format YYYY-MM-DD.")
                tugas[index]["deadline"] = deadline_baru
                while True:
                    print("\nPilihan prioritas tugas:")
                    print("1. Tinggi")
                    print("2. Sedang")
                    print("3. Rendah")
                    prioritas_input = input("Masukkan prioritas tugas baru (1/2/3): ").strip()
                    if prioritas_input in ["1", "2", "3"]:
                        break
                    print("Input tidak valid. Harap masukkan 1, 2, atau 3.")
                if prioritas_input == "1":  
                    tugas[index]["prioritas"] = "tinggi"
                elif prioritas_input == "2":
                    tugas[index]["prioritas"] = "sedang"
                elif prioritas_input == "3":
                    tugas[index]["prioritas"] = "rendah"
                else:
                    print("Input tidak valid. Prioritas tugas tidak diubah.")
                    simpan_tugas(tugas)
                print("Tugas berhasil diedit:", edit_nomor)
            else:
                print("Nomor tugas tidak valid")
        except (IndexError, ValueError):
            print("Tugas gagal diedit. Nomor tugas tidak valid.")
        tunggu_enter()
        continue
#Pengguna menandai tugas sebagai selesai
    elif pilihan == "5":
        try:
            if not tugas:
                print("Tidak ada tugas yang tersedia")
                continue
            else:
                print(f"\nDaftar Tugas (Total: {len(tugas)}):")
                print("\nDaftar Tugas:")
                nomor = 1
                for item in tugas:
                    print(nomor,item["nama"],"-",item["status"],"-",item["prioritas"],"-",item["deadline"])
                    nomor += 1
            selesai_nomor = int(input("\nMasukkan nomor tugas yang telah selesai: ").strip())
            if 1 <= selesai_nomor <= len(tugas):
                index = selesai_nomor - 1
                if tugas[index]["status"] == "selesai":
                    print("Tugas ini sudah ditandai sebagai selesai.")
                else:
                    tugas[index]["status"] = "selesai"
                    print("Tugas berhasil ditandai sebagai selesai:", selesai_nomor)
                    simpan_tugas(tugas)
            else:
                print("Nomor tugas tidak valid")
        except (IndexError, ValueError):
            print("Tugas gagal ditandai sebagai selesai. Nomor tugas tidak valid.")
        tunggu_enter()
        continue
#Pengguna mencari tugas
    elif pilihan == "6":
        keyword = input("\nMasukkan keyword tugas yang ingin dicari: ").strip()
        if not keyword:
            print("Keyword tidak boleh kosong")
            tunggu_enter()
            continue
        ditemukan = False
        for item in tugas:
            if keyword.lower() in item["nama"].lower():
                print(item["nama"], "-", item["status"], "-", item["deadline"])
                ditemukan = True
        if not ditemukan:
            print("Tugas tidak ditemukan")
        tunggu_enter()
        continue
#Pengguna memfilter tugas berdasarkan prioritas
    elif pilihan == "7":
        while True:
            print("\nPilihan prioritas tugas:")
            print("1. Tinggi")
            print("2. Sedang")
            print("3. Rendah")
            prioritas_filter = input("Masukkan prioritas tugas (1/2/3): ").strip()
            if prioritas_filter not in ["1","2","3"]:
                print("Input tidak boleh kosong. Harap masukkan 1, 2, atau 3.")
                tunggu_enter()
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
        tunggu_enter()
        continue
#Pengguna memfilter tugas berdasarkan status
    elif pilihan == "8":
        while True:
            print("\nPilihan status tugas:")
            print("1. Selesai")
            print("2. Belum Selesai")
            status_filter = input("Masukkan status tugas (1/2): ").strip()
            if status_filter not in ["1", "2"]:
                print("Input tidak valid. Harap masukkan 1 atau 2.")
                tunggu_enter
                continue
            break
        if status_filter == "1":
            status = "selesai"
        elif status_filter == "2":
            status = "belum"
        ditemukan = False
        for item in tugas:
            if item["status"] == status:
                print(item["nama"], "-", item["status"], "-", item["deadline"])
                ditemukan = True
        if not ditemukan:
            print("Tidak ada tugas dengan status", status)
        tunggu_enter()
        continue
#Pengguna ingin melihat statistik tugas
    elif pilihan == "9":
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
        tunggu_enter()
        continue
#Pengguna ingin membatalkan status selesai
    elif pilihan == "10":
        if not tugas:
            print("Tidak ada tugas yang tersedia")
            tunggu_enter()
            continue
        try:
            batal_nomor = int(input("\nMasukkan nomor tugas yang ingin dibatalkan status selesai: ").strip())
            if 1 <= batal_nomor <= len(tugas):
                index = batal_nomor - 1
                if tugas[index]["status"] == "selesai":
                    tugas[index]["status"] = "belum"
                    print("Status tugas berhasil dibatalkan menjadi belum selesai:", batal_nomor)
                    simpan_tugas(tugas)
                else:
                    print("Tugas ini belum ditandai sebagai selesai.")
        except (IndexError, ValueError):
                print("Nomor tugas tidak valid")
        tunggu_enter()
        continue

#Pengguna keluar dari program
    elif pilihan == "11":
        print("Terima kasih telah menggunakan aplikasi daftar tugas sederhana!")
        print("Silahkan datang lagi")
        break
    else:
        print("Pilihan tidak tersedia")
