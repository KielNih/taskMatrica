Note: Configuration Steps for custom_attendance_api
To ensure the API is accessible, this module uses a dynamic Bearer Token security system integrated with Odoo's System Parameters. You must configure this token before testing:
- Navigate to Settings -> Technical -> System Parameters.
- Click New and create a new parameter with the following details:
- Key: custom_api.secret_token
- Value: (Enter your secret password/token here, e.g., SecretNih)
- Click Save.
