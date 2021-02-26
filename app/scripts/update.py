import os
import sys
import datetime
import urllib.parse
import hashlib
import pathlib
import markdown
from bs4 import BeautifulSoup
if os.getcwd().endswith("scripts"):
    print("Should be run from the root directory, changing dir now")
    os.chdir("../..")
print("Current working directory:", os.getcwd())
sys.path.append(os.getcwd())
import glob
import app.database as db

TEXTS_DIR = "app/texts"


def reset_db():
    print("Resetting database")
    db.SQLAlchemyBase.metadata.drop_all(db.engine)
    db.SQLAlchemyBase.metadata.create_all(db.engine)


def generate_hash(file_path) -> str:
    blocksize = 65536
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(blocksize)
    return hasher.hexdigest()


def ls_texts(dir_path) -> set:
    glob_path = f"{dir_path}/*.md"
    file_paths = glob.glob(glob_path, recursive=True)
    return {os.path.basename(f) for f in file_paths}


def paths_in_db() -> list:  # unused
    session = db.Session()
    entries = session.query(db.Text).all()
    session.close()
    return [e.file_path for e in entries]


def add_to_db(path: str):
    with open(path, 'r') as f:
        text = f.read()
    if not text:
        print(f"Skipping {path}")
        return
    text_hash: str = generate_hash(path)
    file_name: str = os.path.basename(path)
    html = markdown.markdown(text)
    title: str = BeautifulSoup(html, features='html.parser').get_text().split('\n')[0]  # wow...
    url_path: str = urllib.parse.quote(title.lower().replace(' ', '-')[:30])
    date_created = datetime.datetime.fromtimestamp(pathlib.Path(path).stat().st_ctime)
    date_modified = datetime.datetime.fromtimestamp(pathlib.Path(path).stat().st_mtime)
    reads: int = 0

    session = db.Session()
    entry = db.Text(text_hash=text_hash, file_name=file_name, title=title, url_path=url_path, html=html,
                    date_created=date_created, date_modified=date_modified, reads=reads)
    session.add(entry)
    session.commit()


def import_texts(dir_path):
    for file_path in ls_texts(dir_path):
        print("Adding", file_path)
        add_to_db(path=f"{dir_path}/{file_path}")
    print("indexing complete")


if __name__ == "__main__":
    reset_db()
    import_texts(TEXTS_DIR)
