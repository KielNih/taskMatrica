
import base64
import io
import xlsxwriter
from datetime import datetime, time 
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ProductReportWizard(models.TransientModel):
    _name = 'product.report.wizard'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    
    excel_file = fields.Binary(string='Download Report', readonly=True)
    file_name = fields.Char(string='File Name', readonly=True)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date > record.end_date:
                raise ValidationError(_("Tanggal mulai (Start Date) tidak boleh lebih besar dari tanggal selesai (End Date)!"))

    def action_generate_excel_report(self):
        self.ensure_one()

        start_datetime = datetime.combine(self.start_date, time.min)
        end_datetime = datetime.combine(self.end_date, time.max)

        product_data = {}
        
        purchase_lines = self.env['purchase.order.line'].search([
            ('order_id.date_approve', '>=', start_datetime),
            ('order_id.date_approve', '<=', end_datetime),
            ('order_id.state', 'in', ['purchase', 'done'])
        ])

        for p_line in purchase_lines:
            prod_id = p_line.product_id.id
            if prod_id not in product_data:
                product_data[prod_id] = {
                    'name': p_line.product_id.display_name,
                    'purchase_qty': 0.0,
                    'purchase_amount': 0.0,
                    'sale_qty': 0.0,
                    'sale_amount': 0.0,
                }
            product_data[prod_id]['purchase_qty'] += p_line.product_qty
            product_data[prod_id]['purchase_amount'] += p_line.price_subtotal


        sale_lines = self.env['sale.order.line'].search([
            ('order_id.date_order', '>=', start_datetime),
            ('order_id.date_order', '<=', end_datetime),
            ('order_id.state', 'in', ['sale', 'done'])
        ])

        for s_line in sale_lines:
            prod_id = s_line.product_id.id
            if prod_id not in product_data:
                product_data[prod_id] = {
                    'name': s_line.product_id.display_name,
                    'purchase_qty': 0.0,
                    'purchase_amount': 0.0,
                    'sale_qty': 0.0,
                    'sale_amount': 0.0,
                }
            product_data[prod_id]['sale_qty'] += s_line.product_uom_qty
            product_data[prod_id]['sale_amount'] += s_line.price_subtotal

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Product Report')

        title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
        text_format = workbook.add_format({'border': 1, 'align': 'left'})
        number_format = workbook.add_format({'border': 1, 'align': 'right', 'num_format': '#,##0.00'})
        center_format = workbook.add_format({'border': 1, 'align': 'center'})

        worksheet.merge_range('A1:F1', 'Laporan Penjualan & Pembelian Produk', title_format)
        worksheet.write('A2', f"Periode: {self.start_date} s/d {self.end_date}")

        headers = [
            'No.', 
            'Nama produk', 
            'Total quantity pembelian', 
            'Total quantity penjualan', 
            'Rata – Rata Harga pembelian', 
            'Rata – Rata Harga penjualan'
        ]

        header_format.set_text_wrap()
        worksheet.set_row(3, 30) 
        
        for col_num, header_title in enumerate(headers):
            worksheet.write(3, col_num, header_title, header_format)

        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:B', 30)
        worksheet.set_column('C:F', 25)
        
        row_idx = 4
        no_seq = 1
        
        for prod_id, data in product_data.items():
            avg_purchase_price = data['purchase_amount'] / data['purchase_qty'] if data['purchase_qty'] > 0 else 0.0
            avg_sale_price = data['sale_amount'] / data['sale_qty'] if data['sale_qty'] > 0 else 0.0

            worksheet.write(row_idx, 0, no_seq, center_format)
            worksheet.write(row_idx, 1, data['name'], text_format)
            worksheet.write(row_idx, 2, data['purchase_qty'], number_format)
            worksheet.write(row_idx, 3, data['sale_qty'], number_format)
            worksheet.write(row_idx, 4, avg_purchase_price, number_format)
            worksheet.write(row_idx, 5, avg_sale_price, number_format)

            row_idx += 1
            no_seq += 1

        workbook.close()
        output.seek(0)

        file_base64 = base64.b64encode(output.read())
        filename = f"Product_Report_{self.start_date}_to_{self.end_date}.xlsx"

        self.write({
            'excel_file': file_base64,
            'file_name': filename
        })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.report.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }