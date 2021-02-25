import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLAlchemyBase = declarative_base()
engine = sa.create_engine("sqlite:///sqlite.db", echo=False)
Session = sessionmaker(bind=engine)


class Text(SQLAlchemyBase):
    __tablename__ = 'Texts'
    text_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    text_hash = sa.Column(sa.String)
    file_name = sa.Column(sa.String)
    title = sa.Column(sa.String)
    url_path = sa.Column(sa.String)
    html = sa.Column(sa.Text)
    date_created = sa.Column(sa.Date)
    date_modified = sa.Column(sa.Date)
    reads = sa.Column(sa.Integer)

    def __repr__(self):
        return f"<URL(text_id='{self.text_id}', title='{self.title}', ...)>"


SQLAlchemyBase.metadata.create_all(engine)
