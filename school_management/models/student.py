from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from datetime import date

class StudentStudent(models.Model):
    _name = 'student.student'
    _description = 'Master Data Siswa'
    _order = 'name'

    nis = fields.Char(string='NIS', required=True, index=True)
    name = fields.Char(string='Nama Siswa', required=True)
    image = fields.Image(string='Foto Siswa', max_width=512, max_height=512)
    gender = fields.Selection([
        ('L', 'Laki-Laki'),
        ('P', 'Perempuan')
    ], string='Jenis Kelamin', default='L')
    birth_date = fields.Date(string='Tanggal Lahir')
    age = fields.Integer(string='Usia', compute='_compute_age', store=True)
    religion = fields.Char(string='Agama')
    father_name = fields.Char(string='Nama Ayah')
    mother_name = fields.Char(string='Nama Ibu')
    address = fields.Text(string='Alamat')
    class_id = fields.Many2one('school.class', string='Kelas', ondelete='restrict')

    @api.constrains('nis')
    def _check_unique_nis(self):
        for rec in self:
            if rec.nis:
                domain = [('nis', '=', rec.nis), ('id', '!=', rec.id)]
                already_exists = self.search_count(domain)
                if already_exists:
                    raise ValidationError("NIS sudah terdaftar! NIS harus unik untuk setiap siswa.")
    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.today()
        for record in self:
            if record.birth_date:
                delta = relativedelta(today, record.birth_date)
                record.age = delta.years
            else:
                record.age = 0
    

    @api.constrains('nis')
    def _check_nis_format(self):
        for rec in self:
            if rec.nis and not rec.nis.isdigit():
                raise ValidationError("NIS (Nomor Induk Siswa) hanya boleh berisi angka tanpa spasi atau huruf.")

    @api.constrains('birth_date')
    def _check_birth_date(self):
        for rec in self:
            if rec.birth_date and rec.birth_date >= date.today():
                raise ValidationError("Tanggal Lahir tidak valid. Siswa tidak mungkin lahir di masa depan.")