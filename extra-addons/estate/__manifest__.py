# -*- coding: utf-8 -*-
{
    # Nama modul yang akan ditampilkan di antarmuka web Odoo
    'name': 'Real Estate Advertisement',
    
    # Versi modul Anda
    'version': '1.0',
    
    # Kategori untuk mengelompokkan modul di menu Odoo Apps
    'category': 'Real Estate',
    
    # Ringkasan singkat mengenai fungsi modul
    'summary': 'Modul untuk mengelola iklan lowongan properti dan real estate.',
    
    # Deskripsi lengkap modul (opsional namun baik untuk dokumentasi)
    'description': """
        Modul Real Estate untuk pembelajaran tutorial Odoo 19.
        Mengelola properti, penawaran dari pembeli, dan tipe properti.
    """,
    
    # Menentukan modul apa saja yang wajib terinstall sebelum modul ini diinstall.
    # Modul 'base' adalah modul inti dari seluruh server Odoo framework.
    'depends': [
        'base',
    ],
    
    # File data (XML, CSV) yang akan dimuat (akan diisi pada chapter selanjutnya)
    'data': [
        # Kita mendaftarkan file security agar dieksekusi oleh Odoo
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ],
    
    # PENTING (Sesuai latihan tutorial):
    # 'application': True membuat modul ini dianggap sebagai Aplikasi utama.
    # Jika bernilai True, modul akan muncul saat filter 'Apps' aktif di Odoo.
    'application': True,
    
    # Menentukan apakah modul ini bisa diinstall secara otomatis atau tidak
    'auto_install': False,
    
    # Lisensi modul
    'license': 'LGPL-3',
}