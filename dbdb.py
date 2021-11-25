from flask_sqlalchemy import SQLAlchemy
import sqlite3

#소스들을 함수로 만들어서 필요한 함수를 불러서 사용
db = SQLAlchemy()

class Closet(db.Model):
    __tablename__ = 'closet'   #테이블 이름
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)   #id를 프라이머리키로 설정, 자동증
    color = db.Column(db.String(64))
    clothes = db.Column(db.String(64))
    red = db.Column(db.Integer)
    green = db.Column(db.Integer)
    blue = db.Column(db.Integer)
    path = db.Column(db.String(128))

def __init__(self, color, clothes, red, green, blue, path):
    self.color = color
    self.clothes = clothes
    self.red = red
    self.green = green
    self.blue = blue
    self.path = path

# conn = sqlite3.connect('lookbookdb.sqlite') #db에 연결하는 부분
# c = conn.cursor() #cursor 객체 생성해야 execute('쿼리') 함수를 사용할 수 있다.
# for row in c.execute("SELECT * FROM closet ORDER BY ROWID DESC LIMIT 1;"):
#     print(row)
# c.execute("DELETE FROM closet WHERE ID = '마지막 키값';")
# conn.commit()  #데이터 수정, 삽입을 한 경우 commit을 해주어야 execute가 db 에 적용
# conn.close() #접속한 db 닫기
     # UPDATE color, clothes FROM closet

# query = '''
# UPDATE closet
# SET color = (SELECT closet.color
#              FROM ( SELECT rid, ROWNUM rn
#                     FROM ( SELECT ROWID rid
#                            FROM closet
#                            ORDER BY ROWID)
#                   )
#              WHERE rid = a.ROWID )
# '''
#
#          closet = Closet()
#          query='''
# UPDATE closet SET closet.color = color, closet.clothes = clothes
# SELECR id FROM
# WHERE ROWID id FROM closet ORDER BY ROWID DESC LIMIT 1;
#
# closet ORDER BY ROWID DESC LIMIT 1;
#           (SELECT * FROM closet ORDER BY ROWID DESC LIMIT 1;)
# '''
# query= "UPDATE closet SET color='pink', clothes='pants' WHERE id = (SELECT max(id) FROM closet)"
# c.execute(query)

# "UPDATE closet SET color='blue' ORDER BY ROWID DESC LIMIT 1;"

# UPDATE closet SET color='blue' ORDER BY ROWID DESC LIMIT 1;

    # UPDATE closet SET color='blue', clothes='pants' WHERE id = (SELECT max(id) FROM closet)

#데이터 삽
# c.execute("INSERT INTO closet VALUES ('1', 'yellow', 'pants', '0', '0' ,'0')")
# c.execute("INSERT INTO closet VALUES ('2', 'gray', 'pants', '0', '0' ,'0')")
# c.execute("INSERT INTO closet VALUES ('3', 'green', 'dress', '0', '0' ,'0')")
# c.execute("INSERT INTO closet VALUES ('4', 'pink', 'pants', '0', '0' ,'0')")
# c.execute("INSERT INTO closet VALUES ('5', 'black', 'pants', '0', '0' ,'0')")
# c.execute("INSERT INTO closet VALUES ('6', 'red', 'dress', '0', '0' ,'0')")

# def __repr__(self):
#         return f"Closet('{self.color}', '{self.clothes}')"

# #데이터 불러 와서 출력
# for row in c.execute('SELECT * FROM closet'):
#     print(row)

#학번을 검색해서 정보 출력

# color = ('blue',)
# c.execute('SELECT * FROM closet WHERE color = ?', color) #execute()함수 쿼리를 실행시켜준다.
# print(c.fetchone())  #fetchone, fetchall사용가능
#
# conn.commit()  #데이터 수정, 삽입을 한 경우 commit을 해주어야 execute가 db 에 적용
# conn.close() #접속한 db 닫기


# def sqlitecon():  #db파일 접속 함
#     return sqlite3.connect('closetdb.sqlite')

# def create_table():  #테이블 생성 함
#     try:
#         db = ()
#         c = db.cursor()
#         c.execute("CREATE TABLE closet (clothes varchar(50), color varchar(50))")
#         db.commit()
#     except Exception as e:
#         print('db error:', e)
#     finally:
#         db.close()

# def insert_data(clothes, color):  #데이터 넣는 함
#     try:
#         db = conn()
#         c = db.cursor()setdata = (clothes, color)
#         c.execute("INSERT INTO closet VALUES (shirts, red)", setdata)
#         conn.commit()
#     except Exception as e:
#         print('db error:', e)
#     finally:
#         conn.close()

# def select_all(): #옷종류로 모든 해당 데이터를 가져
#     ret = list()
#     try:
#         # db = conn()
#         # c = db.cursor()
#         c.execute('SELECT * FROM clothes')
#         ret = c.fetchall()
#     except Exception as e:
#         print('db error:', e)
#     finally:
#         db.close()
#     return ret
#
#
# def select_num(num): #색상으로 하나의 데이터만 가져
#     ret = ()
#     try:
#         # db = conn()
#         # c = db.cursor()
#         setdata = (num,)
#         c.execute('SELECT * FROM closet WHERE color = ?', setdata)
#         ret = c.fetchone()
#     except Exception as e:
#         print('db error:', e)
#     finally:
#         db.close()
#         return ret

# #함수로 안만드는 경우
#
# conn = sqlite3.connect('closetdb.sqlite') #db에 연결하는 부분
# c = conn.cursor() #cursor 객체 생성해야 execute('쿼리') 함수를 사용할 수 있다.
# query = "SQL 쿼리" #쿼리작성
# result = conn.execute(query) #쿼리실행
#
# #테이블 생성
# c.execute("CREATE TABLE student (num varchar(50), name varchar(50))")
# #데이터 불러 와서 출력
# for row in c.execute('SELECT * FROM student'):
#     print(row)
#
#컬 검색해서 정보 출력
# color = ('red',)
# c.execute('SELECT * FROM closet WHERE color = ?', color) #execute()함수 쿼리를 실행시켜준다.
# print(c.fetchone())  #fetchone, fetchall사용가능

# query = "CREATE TABLE closet (id INTEGER PRIMARY KEY, clothes String(64), color String(64))"
# result = conn.execute(query) #쿼리실행
# conn.commit()  #데이터 수정, 삽입을 한 경우 commit을 해주어야 execute가 db 에 적용
# conn.close() #접속한 db 닫기