buku = []
while True:
    print("\nMasukkan data buku!\n")
    judul = input('Judul buku: ').capitalize()
    penulis = input('Penulis buku: ').capitalize()

    data_buku = [judul, penulis]
    buku.append(data_buku)

    print("\n","="*10,"Data buku: ","="*10,"\n")
    for index,data_buku in enumerate(buku):
        print(f"{index+1} | {data_buku[0]} | {data_buku[1]}")

    print ("="*34)
    pilihan = input("\nApakah ingin menambahkan buku lagi? (y/n): ").lower()
    if pilihan == 'n':
        break   
print ("Program selesai")