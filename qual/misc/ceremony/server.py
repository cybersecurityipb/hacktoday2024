#!/usr/bin/env python3

score = 0

# KJ
cek_answer1 = "20-05-2008" 
cek_answer2 = "29105141"
cek_answer3 = "Dhomber"
cek_answer4 = "PQV2+63"
cek_answer5 = "Polygon Cascade"

print("===================")
print("CEK JAWABAN DI SINI")
print("===================")
print()

# nomor 1
print("1. Apa tanggal lahir dari perwakilan putra Provinsi Gorontalo?")
print("   Format: DD-MM-YYYY")
print("   Contoh: 31-12-1999")
answer1 = input(">>> ")
if answer1 == cek_answer1:
	score += 1
	print("Mantap, jawabanmu benar :D! Lanjut...\n")
else:
	print("Jawaban masih salah :(! Lanjut...\n")

# nomor 2
print("2. Perancang taman di mana patung tersebut berada memiliki 2 putri, yang salah satunya kini bekerja sebagai dosen paruh waktu. Apa NIM-nya semasa kuliah?")
print("   Format: Angka")
print("   Contoh: 12345678")
answer2 = input(">>> ")
if answer2 == cek_answer2:
	score += 1
	print("Mantap, jawabanmu benar :D! Lanjut...\n")
else:
	print("Jawaban masih salah :(! Lanjut...\n")

# nomor 3
print("3. Di pangkalan udara (lanud) mana pesawat-pesawat tersebut menetap selama persiapan Upacara 17 Agustus di IKN?")
print("   Format: Nama")
print("   Contoh: Halim")
answer3 = input(">>> ")
if answer3 == cek_answer3:
	score += 1
	print("Mantap, jawabanmu benar :D! Lanjut...\n")
else:
	print("Jawaban masih salah :(! Lanjut...\n")

# nomor 4
print("4. Pencipta lagu tersebut bersekolah di suatu SMA negeri. Di manakah lokasi SMA tersebut?")
print("   Format: Pluscode")
print("   Contoh: CPRJ+QG")
answer4 = input(">>> ")
if answer4 == cek_answer4:
	score += 1
	print("Mantap, jawabanmu benar :D! Lanjut...\n")
else:
	print("Jawaban masih salah :(! Lanjut...\n")

# nomor 5
print("5. Apa nama model dari sepeda tersebut?")
print("   Format: Merk Model")
print("   Contoh: Trek Marlin")
answer5 = input(">>> ")
if answer5 == cek_answer5:
	score += 1
	print("Mantap, jawabanmu benar :D!\n")
else:
	print("Jawaban masih salah :(!\n")

# cek skor
if (score >= 0) & (score < 5) :
	print(f"{score} dari 5 jawaban benar. Coba lagi!")
elif score == 5:
	print(f"Selamat! {score} dari 5 jawaban benar. Gas submit gan :D!")
	print("Flag: hacktoday{" + f"{answer1}_{answer2}_{answer3}_{answer4}_{answer5}" + "}")
else:
	print("ada error...")
