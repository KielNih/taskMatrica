import json
from datetime import datetime
from odoo import http
from odoo.http import request



class AttendanceAPI(http.Controller):

    def _check_authentication(self):
        auth_header = request.httprequest.headers.get('Authorization')
        expected_token = request.env['ir.config_parameter'].sudo().get_param('custom_api.secret_token')
        if not expected_token or not auth_header or auth_header != f"Bearer {expected_token}":
            return False
        return True

    def _format_response(self, code, message, data=None):
        response_body = {
            "Code": code,
            "Message": message
        }
        if data is not None:
            response_body["Data"] = data
            
        return request.make_response(
            json.dumps(response_body),
            headers=[('Content-Type', 'application/json')]
        )

  
    @http.route('/api/attendance', type='http', auth='public', methods=['GET', 'POST'], csrf=False)
    def handle_attendance_api(self, **kwargs):
        if not self._check_authentication():
            return self._format_response(401, "Unauthorized: Invalid or missing token")
        if request.httprequest.method == 'GET':
            return self._process_get_request(**kwargs)
        elif request.httprequest.method == 'POST':
            return self._process_post_request()

    def _process_get_request(self, **kwargs):
        start_date_str = kwargs.get('start_date')
        end_date_str = kwargs.get('end_date')
        domain = []

        if start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                domain = [('date', '>=', start_date), ('date', '<=', end_date)]
            except ValueError:
                return self._format_response(400, "Bad Request: Invalid date format. Use YYYY-MM-DD")

        records = request.env['custom.attendance'].sudo().search(domain)
        
        data_result = []
        for rec in records:
            data_result.append({
                "nama": rec.name,
                "tanggal": rec.date.strftime('%Y-%m-%d %H:%M:%S') if rec.date else "",
                "tipe": rec.type,
                "longitude": str(rec.longitude), 
                "latitude": str(rec.latitude)
            })
            
        return self._format_response(200, "Success", data_result)

    def _process_post_request(self):
        try:
            raw_body = request.httprequest.data
            payload = json.loads(raw_body)
            required_fields = ['nama', 'tanggal', 'tipe', 'longitude', 'latitude']

            if not all(field in payload for field in required_fields):
                return self._format_response(400, "Bad Request: Missing required fields")
            try:
                date_obj = datetime.strptime(payload['tanggal'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                 return self._format_response(400, "Bad Request: Date format must be YYYY-MM-DD HH:MM:SS")

            request.env['custom.attendance'].sudo().create({
                'name': payload['nama'],
                'date': date_obj,
                'type': payload['tipe'],
                'longitude': float(payload['longitude']),
                'latitude': float(payload['latitude']),
            })
            return self._format_response(200, "Success")
            
        except json.JSONDecodeError:
            return self._format_response(400, "Bad Request: Invalid JSON body")
        except Exception as e:
            return self._format_response(500, f"Internal Server Error: {str(e)}")