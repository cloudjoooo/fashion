import sqlite3

def insertDB( cnt, color, clothes):
    conn = sqlite3.connect('closetdb.sqlite')
    c = conn.cursor()
    # 데이터 베이스에 몇 개의 데이터가 있는지 변수로 받아와서 다음 줄에 +1 해서 실행
    list1 = c.fetchall()
    cnt = len(list1)
    c.execute("INSERT INTO closet VALUES (?, ?, ?)", [cnt + 1, color, clothes])
    conn.commit()
    conn.close()

insertDB(10, "pink", 'dress')