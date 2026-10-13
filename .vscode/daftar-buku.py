buku = []

while True:
    print("=====Perpustakaan=====")
    print("1. Tambah buku")
    print("2. Lihat buku")
    print("3. Cari buku")
    print("4. Keluar")

    pilihan = input("Masukkan pilihan (1/2/3/4): ").strip()

    if pilihan == "1":
        judul = input('Judul buku: ').capitalize().strip()
        penulis = input('Penulis buku: ').capitalize().strip()

        if judul == "" or penulis == "" :
            print ("data tidak boleh kosong")
            continue

        data_buku = [judul, penulis]
        buku.append(data_buku)
    elif pilihan == "2":
        print("\n","="*10,"Data buku: ","="*10,"\n")

        for index,data_buku in enumerate(buku):
            print(f"{index+1} | {data_buku[0]} | {data_buku[1]}")

        print ("="*34)

    elif pilihan == '4':
        print ("Terima kasih telah mengunakan program perpustakaan")
        break
    else :
        print ("pilihan tidak tersedia")
    

    
print ("Program selesai")