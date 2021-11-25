from flask import Flask, render_template, request, redirect #render_template으로 html파일 렌더링
from models import db
from flask_sqlalchemy import SQLAlchemy
import os
import uuid
import tensorflow as tf
# import sqlite3
# from PIL import Image
from tensorflow.keras.models import load_model
from flask import Flask, render_template, request, redirect, jsonify
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from models_login import Fcuser
from models import Closet

# 색상 추천 알고리즘 추가
from third_GC import grapcut #  알고리즘 grapcut -> 파라미터로 이미지 경로 전달
from get_distance import get_angle
from recoColor import tonInTon, tonOnTon 

app = Flask(__name__)
# conn = sqlite3.connect("closetdb.db")
# print("Opened database successfully")
# # conn.execute(
    
# conn.commit()   # 지금껏 작성한 SQL, DB에 반영 commit
# conn.close()

basedir = os.path.abspath(os.path.dirname(__file__))

model_col = load_model(os.path.join(basedir, 'best_colors.hdf5'))
model_cat = load_model(os.path.join(basedir, 'best_category.hdf5'), custom_objects={'tf':tf})


ALLOWED_EXT = set(['jpg', 'jpeg', 'png', 'jfif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT
    

cat_classes = ['dress', 'pants', 'shirt', 'shoes', 'shorts']
col_classes = ['black', 'blue', 'brown', 'green', 'red', 'white']

def predict(filename, model_cat, model_col):
    img = load_img(filename, target_size=(110, 110))
    img = img_to_array(img)
    img = img.reshape(1, 110, 110, 3)

    img = img.astype('float32')
    img = img/255.0

    result_col = model_col.predict(img)  # 색상 예측 결과 저장
    result_cat = model_cat.predict(img)  # 카테고리 예측 결과 저장


    dict_result_col = {}  # 색상 결과 딕셔너리
    dict_result_cat = {}  # 카테고리 결과 딕셔너리

    for i in range(6):
        dict_result_col[result_col[0][i]] = col_classes[i]
        # dict_result_col 에 result_col[0][i]가 '키'이고, col_classes[i]가 '값'이 되도록 추가
    for i in range(5):
        dict_result_cat[result_cat[0][i]] = cat_classes[i]
        # dict_result_cat 에 result_cat[0][i]가 '키'이고, cat_classes[i]가 '값'이 되도록 추가

    res_col = result_col[0]  # 색상 결과 1차원 리스트로 res_col 에 저장
    res_cat = result_cat[0]  # 카테고리 결과 1차원 리스트로 res_cat 에 저장

    res_col.sort()  # 각 카테고리가 될 확률을 순서대로 정렬
    res_cat.sort()  # 각 색상이 될 확률을 순서대로 정렬

    res_col = res_col[::-1]  # 정렬한 것 반대로 
    res_cat = res_cat[::-1]  # 정렬한 것 반대로

    prob_col = res_col[:3]  # 상위 3개 따로 리스트(prob_col) 만들어서 저장
    prob_cat = res_cat[:3]  # 상위 3개 따로 리스트(prob_cat) 만들어서 저장


    class_col_result = []
    class_cat_result = []

    for i in range(3):
        class_col_result.append(dict_result_col[prob_col[i]])
        class_cat_result.append(dict_result_cat[prob_cat[i]])


    return class_cat_result, class_col_result


@app.route('/', methods=['GET','POST'])
def main():
    if request.method == 'GET':
        return render_template("main.html")

    
@app.route('/mycloset', methods=['GET','POST'])
def mycloset():
    if request.method == 'GET':
        return render_template("mycloset.html")

@app.route('/recommendation', methods=['GET','POST'])
def recommendation():
    if request.method == 'GET':
        return render_template("recommendation.html")

@app.route('/closetshare', methods=['GET','POST'])
def closetshare():
    if request.method == 'GET':
        return render_template("closetshare.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
@app.route('/login2', methods=['GET','POST'])
def login2():
    if request.method == 'GET':
        return render_template("room.html")

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template("register.html")
    
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register2.html")    
    else:
        #회원정보 생성
        userid = request.form.get('userid') 
        email = request.form.get('email')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        print(password) # 들어오나 확인해볼 수 있다. 


        if not (userid and email and password and re_password) :
            return "모두 입력해주세요"
        elif password != re_password:
            return "비밀번호를 확인해주세요"
        else: #모두 입력이 정상적으로 되었다면 밑에명령실행(DB에 입력됨)
            fcuser = Fcuser()         
            fcuser.password = password           #models의 FCuser 클래스를 이용해 db에 입력한다.
            fcuser.userid = userid
            fcuser.email = email     
            db.session.add(fcuser)
            db.session.commit()
            # render_template("accept.html")   //이거 실행 안 되는데 나중에 수정해보기

        return redirect('/')
    
@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")

    
@app.route('/compare_success', methods = ['GET', 'POST'])
def compare_success():
    error = ''
    target_img = os.path.join(os.getcwd(), 'static/images')
    if request.method == 'POST':
        if(request.form):
            link = request.form.get('link')
            try:
                resource = urllib.request.urlopen(link)
                unique_filename = str(uuid.uuid4())
                filename = unique_filename+".jpg"
                img_path = os.path.join(target_img, filename)
                output = open(img_path, "wb")
                output.write(resource.read())
                output.close()
                img = filename
                
                col = grapcut(img_path)
                angle_result = get_angle(col)
                print(angle_result)
                
                # color_result = angle_result.keys()[:3]

                
                cat_result, col_result = predict(img_path, model_cat, model_col)

                predictions = {
                        "class1": cat_result[0],
                        "class2": cat_result[1],
                        "class3": cat_result[2],
                        "prob1": col_result[0],
                        "prob2": col_result[1],
                        "prob3": col_result[2]
                }

            except Exception as e:
                print(str(e))
                error = 'This image from this site is not accesible or inappropriate input'

            if(len(error) == 0):
                return render_template('compare_success.html', img=img, predictions=predictions)
            else:
                return render_template('load_img.html', error=error)


        elif (request.files):
            file = request.files['file']
            if file and allowed_file(file.filename):
                file.save(os.path.join(target_img, file.filename))
                img_path = os.path.join(target_img, file.filename)
                img = file.filename
                cat_result, col_result = predict(img_path, model_cat, model_col)

                predictions = {
                      "class1": cat_result[0],
                        "class2": cat_result[1],
                        "class3": cat_result[2],
                        "prob1": col_result[0],
                        "prob2": col_result[1],
                        "prob3": col_result[2]
                }

            else:
                error = "Please upload images of jpg , jpeg and png extension only"

            if(len(error) == 0):
                return render_template('compare_success.html', img=img, predictions=predictions)
            else:
                return render_template('index.html', error=error)

    else:
        return render_template('index.html')
    
# @app.route('/success', methods = ['GET', 'POST'])
# def success():
#     if request.method == 'POST':
#         col = grapcut(img_path)
#         angle_result = get_angle(col) # angle_result 는 딕셔너리임
#         print(angle_result)
#         tonOnTon(col)
#         tonInTon(col)
#         return render_template("success.html")

# @app.route('/comparedb')
# def board():
#     con = sqlite3.connect("closetdb.db")
#     cur = con.cursor()
#     cur.execute("SELECT * FROM closet")
#     rows = cur.fetchall()
 
#     print("DB: ")
    
#     for i in range(len(rows)):
#         print(rows[i][0] + ':' + rows[i][1])
#     return render_template("comparedb.html", rows = rows)
    

    
if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))  # database 경로를 절대경로로 설정함
    dbfile = os.path.join(basedir, 'closetdb.sqlite') # 데이터베이스 이름과 경로
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True     # 사용자에게 원하는 정보를 전달완료했을때가 TEARDOWN, 그 순간마다 COMMIT을 하도록 한다.라는 설정
    #여러가지 쌓아져있던 동작들을 Commit을 해주어야 데이터베이스에 반영됨. 이러한 단위들은 트렌젝션이라고함.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # True하면 warrnig메시지 유발, 

    db.init_app(app) #초기화 후 db.app에 app으로 명시적으로 넣어줌
    db.app = app
    db.create_all()   # 이 명령이 있어야 생성됨. DB가
    
    app.run(host='0.0.0.0',debug=True)


