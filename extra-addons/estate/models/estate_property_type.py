# Mengimpor modul dasar Odoo
from odoo import models, fields

# Membuat tabel baru untuk Tipe Properti
class EstatePropertyType(models.Model):
    # Nama model ini akan menjadi tabel 'estate_property_type'
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    # Kolom nama tipe properti, wajib diisi
    name = fields.Char(string="Name", required=True)


    _sql_constraints = [
        # 2. Tuple berisi 3 elemen: ('nama_constraint_unik', 'SINTAKS_SQL', 'Pesan Error untuk User')
        (
            'type_name_unique',             # Nama constraint unik untuk database PostgreSQL
            'UNIQUE(name)',                  # Instruksi SQL: Kolom 'name' tidak boleh ada yang duplikat
            'The property type name must be unique!' # Pesan pop-up merah yang muncul di layar user
        )
    ]
    
    # RELASI: Menghubungkan tipe properti dengan properti yang dimilikinya.
    # one2many memastikan satu tipe properti bisa dimiliki oleh banyak properti.
    # 'property_type_id' adalah nama field yang nanti akan dibuat di model estate.property (tabel anak).
    # property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")