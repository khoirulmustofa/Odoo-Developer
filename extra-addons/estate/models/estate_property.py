# File: estate/models/estate_property.py
from dateutil.relativedelta import relativedelta

# 1. Mengimpor pustaka (library) bawaan Odoo
# tambahkan 'api' untuk menggunakan decorator
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

# 2. Mendefinisikan class Python yang mewarisi class models.Model milik Odoo
class EstateProperty(models.Model):
    # 3. Menentukan nama unik untuk model ini di dalam sistem Odoo
    _name = "estate.property"
    
    # 4. Memberikan deskripsi internal mengenai model ini (menghilangkan warning log)
    _description = "Real Estate Property"

    # 5. Membuat field / kolom 'name' (Tipe teks pendek/VARCHAR), wajib diisi
    name = fields.Char(required=True, string="Title")
    
    # 6. Membuat field 'description' (Tipe teks panjang/TEXT)
    description = fields.Text(string="Description")
    
    # 7. Membuat field 'postcode' (Tipe teks pendek/VARCHAR)
    postcode = fields.Char(string="Postcode")
    
    # 8. Membuat field 'date_availability' (Tipe tanggal/DATE)
    date_availability = fields.Date(string="Available From",copy=False, default=lambda self: fields.Datetime.now() + relativedelta(months=3))
    
    # 9. Membuat field 'expected_price' (Tipe desimal/FLOAT), wajib diisi
    expected_price = fields.Float(required=True, string="Expected Price")
    
    # 10. Membuat field 'selling_price' (Tipe desimal/FLOAT), diatur readonly agar tidak bisa diedit manual
    selling_price = fields.Float(string="Selling Price", readonly=True,copy=False)
    
    # 11. Membuat field 'bedrooms' (Tipe bilangan bulat/INTEGER) dengan nilai default awal 2
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    
    # 12. BARU: Membuat field 'living_area' (Tipe bilangan bulat/INTEGER) untuk menyimpan luas ruang utama/bisa dihuni
    living_area = fields.Integer(string="Living Area (sqm)")
    
    # 13. BARU: Membuat field 'facades' (Tipe bilangan bulat/INTEGER) untuk menyimpan jumlah sisi muka/depan bangunan
    facades = fields.Integer(string="Facades")
    
    # 14. Membuat field 'garage' (Tipe benar atau salah/BOOLEAN) untuk status kepemilikan garasi
    garage = fields.Boolean(string="Garage")
    
    # 15. BARU: Membuat field 'garden' (Tipe benar atau salah/BOOLEAN) untuk status apakah memiliki kebun atau tidak
    garden = fields.Boolean(string="Garden")
    
    # 16. BARU: Membuat field 'garden_area' (Tipe bilangan bulat/INTEGER) untuk menyimpan data luas area kebun
    garden_area = fields.Integer(string="Garden Area (sqm)")
    
    # 17. Membuat field 'garden_orientation' (Tipe Pilihan/SELECTION) dengan 4 nilai opsional dalam bentuk list of tuples
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', 'North'), # Elemen pertama ('north') disimpan di database, elemen kedua ('North') ditampilkan di UI
            ('south', 'South'), # Menambahkan opsi arah Selatan
            ('east', 'East'),   # Menambahkan opsi arah Timur
            ('west', 'West')    # Menambahkan opsi arah Barat
        ],
    )

    # Mendefinisikan field baru bernama total_area.
    # 18. Atribut 'compute' menunjuk ke nama fungsi (berupa string) yang akan melakukan kalkulasi.
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")

    # 19. BARU: Membuat field 'best_price' (Tipe desimal/FLOAT) untuk menyimpan nilai hasil kalkulasi
    best_price = fields.Float(compute="_compute_best_price", string="Best Price Offers", copy=False)

    # 20. BARU: Membuat field 'state' (Tipe Pilihan/SELECTION) untuk menyimpan status properti
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'), 
            ('canceled', 'Canceled')
        ],
        required=True, copy=False, default='new', string="Status"
    )

    # === PENAMBAHAN RELASI MANY2ONE ===
    
    # Menghubungkan properti ke 1 tipe (dropdown Tipe Rumah)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    
    # Menghubungkan properti ke 1 pembeli (tabel bawaan res.partner)
    # copy=False memastikan rumah yang diduplikasi tidak otomatis terjual ke pembeli yang sama
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    
    # Menghubungkan properti ke 1 agen penjual (tabel bawaan res.users / user yang login ke sistem)
    # default=lambda self: self.env.user secara otomatis mengisi field ini dengan user yang sedang aktif membuat data
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)

    # === PENAMBAHAN RELASI MANY2MANY ===
    
    # Menghubungkan ke tabel Tag. Odoo akan mengurus tabel perantara (pivot)-nya
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    # === PENAMBAHAN RELASI ONE2MANY ===
    
    # Menarik semua data Penawaran untuk rumah ini. 
    # Parameter 1: Nama model target ("estate.property.offer")
    # Parameter 2: Nama field Many2one yang ada di dalam model target tersebut ("property_id")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")


   # 1. Atribut ajaib _order menentukan pengurutan default tabel saat diload.
    # 'id desc' berarti diurutkan berdasarkan ID secara 'descending' (menurun).
    # Efeknya: Rumah yang baru saja diinput (ID terbesar) akan selalu muncul paling atas.
    _order = "id desc"


    # Menambahkan validasi harga tidak boleh minus langsung di PostgreSQL
    _sql_constraints = [
        (
            'check_expected_price',          # Identifier unik
            'CHECK(expected_price > 0)',     # Instruksi SQL: Harga harapan harus lebih dari 0
            'A property expected price must be strictly positive.' # Pesan error
        ),
        (
            'check_selling_price',
            'CHECK(selling_price >= 0)',     # Instruksi SQL: Harga jual boleh 0 (belum terjual), tapi tidak boleh minus
            'A property selling price must be positive.'
        )
    ]

    # Jika 'expected_price' atau 'selling_price' diisi/diubah, fungsi di bawahnya akan jalan.
    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        # 4. WAJIB melooping 'self' karena Odoo bekerja secara batch (Recordset)
        for record in self:
            # 5. Kita abaikan pengecekan jika harga jual masih 0 (artinya rumah belum laku/belum ada penawaran diterima)
            # presicion_digits=2 berarti kita membandingkan hingga 2 angka di belakang koma (0.00)
            if not float_is_zero(record.selling_price, precision_digits=2):
                
                # 6. Menghitung ambang batas bawah (90% dari harga harapan)
                lowest_price = record.expected_price * 0.9
                
                # 7. Menggunakan float_compare untuk membandingkan 2 angka desimal secara aman.
                # Format: float_compare(Angka_A, Angka_B, precision_digits)
                # Return -1 artinya Angka_A < Angka_B
                # Return  0 artinya Angka_A == Angka_B
                # Return  1 artinya Angka_A > Angka_B
                if float_compare(record.selling_price, lowest_price, precision_digits=2) == -1:
                    
                    # 8. Jika harga jual lebih kecil (-1) dari 90%, lemparkan error untuk mencegah data tersimpan!
                    raise ValidationError("The selling price cannot be lower than 90% of the expected price.")
    

    # Fungsi ini akan dijalankan ulang jika nilai living_area ATAU garden_area berubah.
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        # 'self' di Odoo adalah Recordset (seperti array of objects).
        # WAJIB melakukan perulangan (looping), meskipun kita sedang mengedit 1 baris data.
        for record in self:
            # 4. Menjumlahkan kedua field dan memasukkannya ke total_area
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        """Menghitung harga terbaik dari semua penawaran (offers)."""
        for property_record in self:
            offers = property_record.offer_ids
            
            if offers:
                highest_price = max(offers.mapped('price'))
                property_record.best_price = highest_price
            else:
                property_record.best_price = 0

    # Decorator @api.onchange memantau perubahan langsung di UI pada field 'garden'
    @api.onchange("garden")
    def _onchange_garden(self):
        # Tidak perlu looping 'for record in self' karena onchange HANYA bekerja pada 1 form yang sedang aktif di layar.
        if self.garden: # Jika checkbox dicentang (bernilai True)
            self.garden_area = 10
            self.garden_orientation = "north"
        else: # Jika checkbox tidak dicentang (bernilai False)
            self.garden_area = 0
            # Mengosongkan pilihan dropdown
            self.garden_orientation = False 
            
            # Menampilkan pop-up notifikasi peringatan ke user
            return {'warning': {
                'title': "Warning",
                'message': "Data kebun telah dihapus karena checkbox dimatikan."
            }}

    # Ini artinya fungsi ini boleh dipanggil dari UI/tombol oleh User.
    def action_sold(self):
        # Selalu lakukan looping karena Odoo bekerja memproses banyak record sekaligus (Recordset)
        for record in self:
            # Validasi bisnis: Rumah yang sudah dibatalkan tidak bisa dijual lagi
            if record.state == 'canceled':
                raise UserError("Canceled property cannot be sold.")
            # Ubah status rumah menjadi terjual
            record.state = 'sold'
        # Fungsi publik XML-RPC Odoo harus selalu mereturn sesuatu (biasanya True jika berhasil)
        return True

    def action_cancel(self):
        for record in self:
            # Validasi bisnis: Rumah yang sudah terjual tidak bisa dibatalkan
            if record.state == 'sold':
                raise UserError("Sold property cannot be canceled.")
            # Ubah status rumah menjadi batal
            record.state = 'canceled'
        return True