import re
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from datetime import date

class SchoolTeacher(models.Model):
    _name = 'teacher.teacher'
    _order = 'name'

    nip = fields.Char(string='NIP', required=True, index=True)
    name = fields.Char(string='Nama Guru', required=True)
    gender = fields.Selection([
        ('L', 'Laki-Laki'),
        ('P', 'Perempuan')
    ], string='Jenis Kelamin', default='L')
    birth_date = fields.Date(string='Tanggal Lahir')
    age = fields.Integer(string='Usia', compute='_compute_age', store=True)
    phone = fields.Char(string='No. Telp')
    address = fields.Text(string='Alamat')
    last_education = fields.Char(string='Pendidikan Terakhir')
    major = fields.Char(string='Jurusan')
    graduation_year = fields.Char(string='Tahun Lulus', index=True)

    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.today()
        for record in self:
            if record.birth_date:
                delta = relativedelta(today, record.birth_date)
                record.age = delta.years
            else:
                record.age = 0

    @api.constrains('phone')
    def _check_phone(self):
        for rec in self:
            if rec.phone:
                if not re.match(r'^\+?\d+$', rec.phone):
                    raise ValidationError("Format Nomor Telepon salah! Hanya diperbolehkan angka, tanda plus (+) diawal.")

    @api.constrains('graduation_year')
    def _check_graduation_year(self):
        current_year = date.today().year
        for rec in self:
            if rec.graduation_year:
                if not rec.graduation_year.isdigit() or len(rec.graduation_year) != 4:
                    raise ValidationError("Tahun Lulus harus berupa 4 digit angka (Contoh: 2015).")
                
                year_int = int(rec.graduation_year)
                if year_int < 1950 or year_int > current_year + 1:
                    raise ValidationError(f"Tahun Lulus tidak logis. Harus berada di antara 1950 dan {current_year + 1}.")

    @api.constrains('birth_date')
    def _check_birth_date(self):
        for rec in self:
            if rec.birth_date and rec.birth_date >= date.today():
                raise ValidationError("Tanggal Lahir tidak valid. Tidak boleh lebih dari atau sama dengan hari ini.")