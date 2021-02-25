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
    return url_path

def decode_url(url_path):
    text = base64.urlsafe_b64decode(f'{url_path}===').decode('utf-8')
    return markdown.markdown(text)


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
            title = None
            html = decode_url(url_path)
        except Exception as e:
            print(e)
            return render_template("404.html")
    return render_template('reader.html', title=title, html=html)

@app.route("/writer", methods=['GET', 'POST'])
def writer():
    if request.method == 'POST':
        text = request.form['text']
        if text:
            url_path = encode_url(text)
            print(url_path)
            return render_template('writer.html', url=f"{request.host_url}{url_path}")
    return render_template("writer.html")



