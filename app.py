from flask import Flask
from bargaindigest_email import send_email, generate_digest_html
from le_scraper import scrape_ozbargain
from json_scanner_function import read_json_files_in_range

app = Flask(__name__)

@app.route('/api/send_email', methods=['GET'])
def hello():
    file_name = scrape_ozbargain()
    # Remove.json from file name
    file_name = file_name[:-5]
    deals = read_json_files_in_range(file_name, file_name, ['Other'])
    deals_html = generate_digest_html(deals)
    send_email("edensteven@protonmail.com", "BargainDigest", deals_html)
    return {'message': 'Sent Message'}