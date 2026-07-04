# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'Data Kelas'

    name = fields.Char(string='Nama Kelas', required=True)
    teacher_id = fields.Many2one('teacher.teacher', string='Wali Kelas', ondelete='set null')

    @api.constrains('name')
    def _check_unique_class_name(self):
        for rec in self:
            if rec.name:
                domain = [('name', '=', rec.name), ('id', '!=', rec.id)]
                already_exists = self.search_count(domain)
                if already_exists:
                    raise ValidationError("Nama Kelas ini sudah ada di database. Silakan gunakan nama lain!")


class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Data Mata Pelajaran'

    name = fields.Char(string='Nama Mata Pelajaran', required=True)
    major = fields.Char(string='Jurusan / Peminatan')
    teacher_id = fields.Many2one('teacher.teacher', string='Guru Pengajar', ondelete='set null')

class SchoolSchedule(models.Model):
    _name = 'school.schedule'
    _description = 'Data Jadwal Pelajaran'
    schedule_datetime = fields.Datetime(string='Tanggal & Waktu', required=True)
    
    class_id = fields.Many2one('school.class', string='Kelas Pelajaran', required=True, ondelete='cascade')
    subject_id = fields.Many2one('school.subject', string='Mata Pelajaran', required=True, ondelete='cascade')

    @api.constrains('schedule_datetime')
    def _check_valid_date(self):
        for rec in self:
            if rec.schedule_datetime:
                if rec.schedule_datetime < fields.Datetime.now():
                    raise ValidationError("Validasi Gagal! Tanggal dan waktu jadwal tidak boleh diatur ke masa lalu.")

    