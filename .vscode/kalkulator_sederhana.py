print ('\nselamat datang dikalkulator epic')

angka_pertama = float(input('masukkan angka pertama: '))
operator = input('masukkan operator(+  - X /): ')
angka_kedua = float(input('masukkan angka ke dua: '))

if operator == '+':
    hasil = f'{angka_pertama + angka_kedua}'
    print(f"hasil: {hasil}")

elif operator == '-':
    hasil = f'{angka_pertama - angka_kedua}'
    print(f"hasil: {hasil}")

elif operator == 'x' or operator == 'X':
    hasil = f'{angka_pertama * angka_kedua}'
    print(f"hasil: {hasil}")

elif operator == '/':
    hasil = f'{angka_pertama / angka_kedua}'
    print(f"hasil: {hasil}")
print ('\nterimakasih telah menggunakan kalkulator epic')