import datetime as dt

while True:
    try:
        print ('Silahkan masukkan tanggal,bulan, dan tahun lahir anda.')
        tahun = int(input('Tahun lahir  : '))
        bulan = int(input('Bulan lahir  : '))
        tanggal = int(input('Tanggal lahir: '))

        lahir = dt.date(tahun, bulan, tanggal)
        print (f'Tanggal lahir anda adalah: {lahir}')

        hari_ini = dt.date.today()
        print (f'Hari ini adalah: {hari_ini}')

        umur_hari = hari_ini - lahir
        umur_tahun = umur_hari.days // 365
        umur_bulan_sisa = (umur_hari.days % 365) // 30

        print (f'Hari lahir anda adalah: {lahir:%A}')
        print (f'Anda berumur: {umur_tahun} tahun dan {umur_bulan_sisa} bulan')
        break
    except ValueError:
        print("Input tidak valid. Silakan masukkan tanggal, bulan, dan tahun yang benar.")
