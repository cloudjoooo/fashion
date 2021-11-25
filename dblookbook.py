from flask_sqlalchemy import SQLAlchemy
import sqlite3


#소스들을 함수로 만들어서 필요한 함수를 불러서 사용
db_lookbook = SQLAlchemy()

class Lookbook(db_lookbook.Model):
    __tablename__ = 'lookbook'   #테이블 이름
    id = db_lookbook.Column(db_lookbook.Integer, primary_key=True, nullable=False, autoincrement=True)   #id를 프라이머리키로 설정, 자동증
    input_path = db_lookbook.Column(db_lookbook.String(128))
    match_path = db_lookbook.Column(db_lookbook.String(128))

def __init__(self, input_path, match_path):
    self.input_path = input_path
    self.input_path = match_path


# conn = sqlite3.connect('db.sqlite') #db에 연결하는 부분
# c = conn.cursor()
# conn.close() #접속한 db 닫기