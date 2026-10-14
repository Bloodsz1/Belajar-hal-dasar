buku = []
while True:
    print("\n")
    print("=====Perpustakaan=====")
    print("1. Tambah buku")
    print("2. Lihat buku")
    print("3. Cari buku")
    print("4. Hapus buku")
    print("5. Keluar")

    pilihan = input("Masukkan pilihan (1/2/3/4/5): ").strip()
#Menambahkan buku
    if pilihan == "1":
        judul = input('Judul buku: ').lower().strip()
        penulis = input('Penulis buku: ').lower().strip()

        if judul == "" or penulis == "" :
            print ("data tidak boleh kosong")
            continue

        data_buku = [judul, penulis]
        buku.append(data_buku)
#Melihat daftar buku    
    elif pilihan == "2":
        print("\n","="*10,"Data buku: ","="*10,"\n")

        for index,data_buku in enumerate(buku):
            print(f"{index+1} | {data_buku[0]} | {data_buku[1]}")

        print ("="*34)
#Mencari daftar buku
    elif pilihan == "3":
        dicari = input("Masukkan judul buku yg ingin dicari: ").lower().strip()
        ditemukan = False
        for data_buku in buku:
            if dicari in data_buku[0]:
                print(f"judul   :{data_buku[0]}")
                print(f"penulis :{data_buku[1]}")
                ditemukan = True
        if not ditemukan:
            print("Buku tidak ditemukan")
#Menghapus buku
    elif pilihan == "4":
        print("\n","="*10,"Data buku: ","="*10,"\n")
    
        for index,data_buku in enumerate(buku):
            print(f"{index+1} | {data_buku[0]} | {data_buku[1]}")
            print ("="*34)
        hapus = input("masukkan judul buku")
#Keluar dari program
    elif pilihan == '5':
        print ("Terima kasih telah mengunakan program perpustakaan")
        break
    else :
        print ("pilihan tidak tersedia")

print ("Program selesai")