import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import EMAIL_ADDRESS, PASSWORD_SECRET_KEY
from datetime import datetime




def send_peminjaman_status_email(receiver_email: str, status: str, alasan: str = None):
    sender = EMAIL_ADDRESS
    password = PASSWORD_SECRET_KEY 

    msg = MIMEMultipart()
    msg["Subject"] = f"Update Status Peminjaman Anda: {status.title()}"
    msg["From"] = sender
    msg["To"] = receiver_email

    status_color = {
        "disetujui": "#059669",  # Green
        "ditolak": "#DC2626",    # Red
        "pending": "#F59E0B",   # Amber
        "dikembalikan": "#4B5563" # Gray
    }.get(status, "#1f2937")

    alasan_html = ""
    if status == "ditolak" and alasan:
        alasan_html = f"""
        <tr>
            <td width="30%" style="padding-bottom: 5px;"><span style="color: #4b5563; font-size: 15px; font-weight: bold;">Alasan:</span></td>
            <td style="padding-bottom: 5px;"><span style="color: #1f2937; font-size: 15px;">{alasan}</span></td>
        </tr>
        """

    html = f""" 
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Notifikasi Status Peminjaman</title>
    <style>
    </style>
</head>
<body style="margin: 0; padding: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f5f5f5;">

    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;">
        <tr>
            <td align="center" style="padding: 40px 0;">
                <table class="content" align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; background: #ffffff; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.08);">
                    
                    <tr>
                        <td align="center" style="padding: 30px 40px 20px 40px; border-bottom: 1px solid #e0e0e0;">
                            <h2 style="color: #1f2937; margin: 0; font-size: 24px; font-weight: 600;">Update Status Peminjaman</h2>
                        </td>
                    </tr>
                    
                    <tr>
                        <td style="padding: 30px 40px;">
                            <p style="color: #4b5563; font-size: 16px; line-height: 1.7;">
                                Halo, status permintaan peminjaman buku Anda telah diperbarui.
                            </p>
                            
                            <div style="background: #f8f9fb; padding: 20px; border-radius: 8px; margin: 25px 0; border-left: 4px solid {status_color};">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                        <td width="30%" style="padding-bottom: 5px;">
                                            <span style="color: #4b5563; font-size: 15px; font-weight: bold;">Status:</span>
                                        </td>
                                        <td style="padding-bottom: 5px;">
                                            <span style="color: {status_color}; font-size: 15px; font-weight: bold;">{status.title()}</span>
                                        </td>
                                    </tr>
                                    {alasan_html}
                                    <tr>
                                        <td width="30%">
                                            <span style="color: #4b5563; font-size: 15px; font-weight: bold;">Waktu:</span>
                                        </td>
                                        <td>
                                            <span style="color: #1f2937; font-size: 15px;">{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC</span>
                                        </td>
                                    </tr>
                                </table>
                            </div>

                            <p style="color: #4b5563; font-size: 16px; line-height: 1.7;">
                                Anda dapat melihat detail lengkap peminjaman Anda dengan masuk ke akun di platform kami.
                            </p>
                        </td>
                    </tr>
                    
                    <tr>
                        <td align="center" style="padding: 20px 40px; border-top: 1px solid #e0e0e0; background-color: #f9f9f9;">
                            <p style="color: #9ca3af; font-size: 12px; margin: 0; line-height: 1.5;">
                                Ini adalah email notifikasi otomatis. Mohon untuk tidak membalas email ini.
                            </p>
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>

</body>
</html>
"""


    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
