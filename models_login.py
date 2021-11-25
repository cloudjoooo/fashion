from flask_sqlalchemy import SQLAlchemy
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash

db_login = SQLAlchemy()           #SQLAlchemy를 사용해 데이터베이스 저장

class Fcuser(db_login.Model):
    __tablename__ = 'fcuser'   #테이블 이름 : fcuser
    id = db_login.Column(db_login.Integer, primary_key = True)
    userid = db_login.Column(db_login.String(32), unique=True, nullable=False) #id를 프라이머리키로 설정
    email = db_login.Column(db_login.String(16), unique=True, nullable=False)  # 이하 위와 동일
    password = db_login.Column(db_login.String(64), nullable=False)     #패스워드를 받아올 문자열길이


    # def __init__(self, userid, email, password):
    #     self.userid = userid
    #     self.email = email
    #     self.password = password
    #
    # def set_password(self, password):
    #     self.password = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password, password)
