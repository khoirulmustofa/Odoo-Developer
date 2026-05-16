from odoo import models, fields,api
from datetime import timedelta # Import library standar Python untuk memanipulasi waktu

class EstatePropertyOffer(models.Model):
    # Nama model ini akan menjadi tabel 'estate_property_offer'
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    # Kolom untuk menyimpan nilai harga penawaran
    price = fields.Float(string="Price")
    
    # Kolom status penawaran, menggunakan dropdown pilihan statis
    # copy=False memastikan saat properti diduplikasi, status penawaran lama tidak ikut tersalin
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        copy=False
    )

    # Masa berlaku penawaran (contoh: 7 hari)
    validity = fields.Integer(string="Validity (days)", default=7)
    
    # Field date_deadline dihitung otomatis, TAPI juga diberi izin untuk diubah manual via 'inverse'
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline" 
    )

    
    # RELASI: Menghubungkan penawaran ini dengan pihak pembeli (mengambil data dari tabel bawaan res.partner)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    
    # RELASI: PENTING! Agar One2many di tabel utama berfungsi, tabel anak ini wajib memiliki Many2one ke tabel utama.
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    # Fungsi Hitung Maju (Menghitung Tanggal Deadline dari Jumlah Hari)
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            # Mengambil tanggal saat ini jika data baru (create_date belum ada di database)
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            # Deadline = Tanggal Pembuatan + Masa Berlaku (hari)
            offer.date_deadline = date + timedelta(days=offer.validity)

    # Fungsi Hitung Mundur (Menghitung Jumlah Hari jika user mengubah Tanggal Deadline)
    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            # Memperbarui nilai validity: (Tanggal Deadline Baru - Tanggal Dasar) dikonversi ke hari
            offer.validity = (offer.date_deadline - date).days