from odoo import models, fields

class EstatePropertyTag(models.Model):
    # Nama model ini akan menjadi tabel 'estate_property_tag'
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(string="Name", required=True)

