# pentathlon

### Description

**Author: k1nomi**

Selamat datang di HackToday 2024 Olympics! Di cabor ini, kamu akan diminta melalui 5 jenis challenge dalam bidang forensics, masing-masing memberikan part dari flagnya. Tim yang berhasil menyatukan flag akan mendapatkan 🥇!

## Attachments
- `chall1.png`

### Flag

`hacktoday{j3_cro1s_3n_m0i_for_1_b3li3ve_1n_mys3lf_7e6afd6912}`

### Proof of Concept
- chall 1: `binwalk -M -e chall1.png`
- chall 2: jpg dimension fix
- chall 3: zip password cracking menggunakan `fcrackzip` atau `john`
- chall 4: reverse scriptnya
- chall 5: fix CRC yang corrupt menggunakan scripting