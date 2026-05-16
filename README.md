# Odoo-Developer

**.gitignore**
```
/var/lib/odoo
```

**git command**
```
git status
git add .
git commit -m "first commit"
git push -u origin main


```

## cara belajar dengan odoo
```
Halo AI, saya sedang mempelajari dokumentasi Odoo Developer. Saya ingin kamu bertindak sebagai mentor Odoo yang berpengalaman. 

Tolong bedah dan jelaskan isi dari dokumentasi berikut ini:
[MASUKKAN LINK DOKUMENTASI DI SINI, CONTOH: https://www.odoo.com/documentation/18.0/developer/tutorials/server_framework_101/03_basicmodel.html]

Ketentuan penjelasan:
1. Jelaskan konsep dasar dari bab ini dengan analogi sederhana yang mudah dipahami pemula.
2. Berikan contoh kode/skrip yang dibahas di halaman tersebut.
3. Berikan komentar bahasa Indonesia yang SANGAT DETAIL pada setiap baris kodenya agar saya tahu fungsi spesifik dari baris tersebut.
4. Apa saja kesalahan umum (common mistakes) yang sering dilakukan developer pemula saat menerapkan bab ini?

```

## jenis relasi 

1. **Many2one (`belongsTo`):** Banyak data bisa merujuk ke satu data referensi.
* *Analogi:* Banyak rumah bisa dikategorikan ke dalam 1 tipe yang sama (misal: "Apartemen"). Di form web, ini biasanya tampil sebagai *dropdown list*.


2. **Many2many (`belongsToMany`):** Hubungan dua arah yang jamak.
* *Analogi:* 1 Rumah bisa punya banyak Tag/Label ("Renovasi", "Nyaman"), dan 1 Tag "Renovasi" bisa dipakai oleh banyak Rumah. Odoo otomatis membuat tabel *pivot* rahasia untuk ini.


3. **One2many (`hasMany`):** Kebalikan dari Many2one. Satu data memiliki banyak data anak.
* *Analogi:* 1 Rumah bisa menerima banyak data Penawaran (*Offers*) dari pembeli. Ini adalah relasi virtual; Odoo akan menarik semua penawaran yang memiliki `property_id` dari rumah tersebut.


