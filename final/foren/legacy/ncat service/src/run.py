#!/usr/bin/env python3

if __name__ == "__main__":
    score = 0
    print('''
    ------------------------------------------------------------
    WELCOME !!! - WELCOME !!! - WELCOME !!! - WELCOME !!! - WELC
    ------------------------------------------------------------''')
    print('''.__                                    
|  |   ____   _________    ____ ___.__.
|  | _/ __ \ / ___\__  \ _/ ___<   |  |
|  |_\  ___// /_/  > __ \\  \___\___  |
|____/\___  >___  (____  /\___  > ____|
          \/_____/     \/     \/\/     ''')
    print('''
    ------------------------------------------------------------
    sudah mendapatkan flag part 1? lalu sudah tau step selanjut-
    nya tapi isi filenya tidak sesuai yang diharapkan? coba
    jawab pertanyaan berikut (maaf untuk ketidaknyamanannya, hal
    tersebut terjadi dikarenakan anomali pada aplikasi dumpernya
    dan cara tercepat untuk mengatasinya adalah menggunakan nc 
    ini)
    ------------------------------------------------------------''')
    while(1):
        print('\n    > Apa file yang menurutmu seharusnya kunci untuk step selanjutnya? (hurup kecil semua menggunakan extension. ex: bleco.dat)')
        inp = input('    > ').encode()
        if inp != b"usrclass.dat":
            print('    ------------------------------------------------------------')
            print('    salah! perhatikan kembali ke file evidencenya ya')
            print('    ------------------------------------------------------------')
            break
        print('    ------------------------------------------------------------')
        print('    Betul!!! emang gajelas FTK imager, dia buat bagian folder Local\Microsoft\Windows nya gasesuai, ')
        print('    seharusnya ada tricknya tapi karena dikejar2 waktu mari gini sajalah ya. berikut link usrclass.dat yang bener dan sudah')
        print('    gampang dibaca https://mega.nz/file/Ehwk3bgT#B361jS1JWpiCXaidq1GQHC-vCaCtcn7hLOE7eJ4jcj4')
        print('    ------------------------------------------------------------')
        break

    exit()
