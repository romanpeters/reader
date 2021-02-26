from flask import render_template, request
from sqlalchemy import or_
import base64
import markdown
from app import database as db
from app import app


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


def encode_url(text):
    url_path = base64.urlsafe_b64encode(bytes(text, 'utf-8')).decode('utf-8')
    return url_path.replace('=', '')

def decode_url(url_path):
    text = base64.urlsafe_b64decode(f'{url_path}===').decode('utf-8')
    sanitized_text = text.replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;')
    return markdown.markdown(sanitized_text)


@app.route("/<string:url_path>", methods=['GET'])
def read_text(url_path):
    session = db.Session()
    text_entry = session.query(db.Text).filter(or_(db.Text.url_path == url_path, db.Text.text_hash == url_path)).first()
    if text_entry:
        text_entry.reads += 1
        session.add(text_entry)
        session.commit()
        title = text_entry.title
        html = text_entry.html
    else:
        session.close()
        try:
            title = "Reader"
            html = decode_url(url_path)
        except Exception as e:
            print(e)
            return render_template("404.html")
    return render_template('reader.html', title=title, html=html)

@app.route("/writer", methods=['GET'])
def writer():
    text = request.args.get('text')
    if not text:
        return render_template('writer.html')
    url_path = encode_url(text)
    return render_template('writer.html', url=f"https://reader.romanpeters.nl/{url_path}")



