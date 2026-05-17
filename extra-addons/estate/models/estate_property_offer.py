from odoo import models, fields,api
from datetime import timedelta # Import library standar Python untuk memanipulasi waktu
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    # Nama model ini akan menjadi tabel 'estate_property_offer'
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    # Kolom untuk menyimpan nilai harga penawaran
    price = fields.Float(string="Price")
    
    # Kolom status penawaran, menggunakan dropdown pilihan statis
    # copy=False memastikan saat properti diduplikasi, status penawaran lama tidak ikut tersalin
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
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
    property_id = fields.Many2one("estate.property", string="Property", required=True, ondelete='cascade')
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", string="Property Type", store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals.get('property_id'))
            if property_id and property_id.state == 'new':
                # Update status properti menjadi 'Offer Received' jika tawaran masuk
                property_id.state = 'offer_received'
        return super().create(vals_list)

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
    
    def action_accept(self):
        for offer in self:
            # Validasi: Cek apakah rumah ini sudah punya penawaran lain yang diterima?
            # Kita cari penawaran yang terhubung ke rumah ini (property_id) yang statusnya 'accepted'
            accepted_offers = offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted')
            if accepted_offers:
                raise UserError("You can only accept one offer for a property!")
            
            # Ubah status penawaran ini jadi diterima
            offer.status = 'accepted'
            
            # MAGIC HAPPENS HERE:
            # Kita bisa memanipulasi model induknya (Rumah) langsung dari model Penawaran ini!
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
        return True