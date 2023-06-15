from flask import Flask, render_template, request
import urllib.parse
import re
import qrcode
import pyshorteners

app = Flask(__name__)

def normalize_phone_number(phone_number):
    normalized_number = re.sub(r'\D', '', phone_number)
    return normalized_number

def generate_whatsapp_link(phone_number, message):
    normalized_phone_number = normalize_phone_number(phone_number)

    base_url = "https://api.whatsapp.com/send"
    encoded_message = urllib.parse.quote(message)
    url = f"{base_url}?phone={normalized_phone_number}&text={encoded_message}"

    return url

def generate_shortened_url(original_url):
    s = pyshorteners.Shortener()
    shortened_url = s.tinyurl.short(original_url)
    return shortened_url

def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill='black', back_color='white')
    return qr_img

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_message = request.form['message']
        user_phone_number = request.form['phone_number']
        whatsapp_link = generate_whatsapp_link(user_phone_number, user_message)
        shortened_url = generate_shortened_url(whatsapp_link)
        qr_code = generate_qr_code(whatsapp_link)
        qr_code.save('static/qrcode.png')  # Save the QR code image
        return render_template('index.html', whatsapp_link=whatsapp_link, shortened_url=shortened_url)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
