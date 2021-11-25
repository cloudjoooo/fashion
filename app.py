from flask import Flask, render_template, request, redirect, jsonify, url_for, abort
from flask_sqlalchemy import SQLAlchemy
import os
import uuid
import urllib
import tensorflow as tf
import sqlite3
import io


import json
# from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

from dbdb import Closet
from dbdb import db
from dblookbook import Lookbook
from dblookbook import db_lookbook
from models_login import db_login
from models_login import Fcuser


# from flask_wtf.csrf import CSRFProtect
# from forms import RegisterForm
# from forms import RegisterForm, LoginForm


# 색상 추천 알고리즘 추가
from finalGC import gc
from recoColor import tonOnTon, tonInTon
from closetFin import findClothes

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

model_col = load_model(os.path.join(basedir, 'keras_model.h5'))
# model_col = load_model(os.path.join(basedir, 'best_colors.hdf5'))
model_cat = load_model(os.path.join(basedir, 'best_category.hdf5'), custom_objects={'tf': tf})

ALLOWED_EXT = set(['jpg', 'jpeg', 'png', 'jfif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

cat_classes = ['dress', 'pants', 'shirt', 'shoes', 'shorts']
# col_classes = ['black', 'blue', 'brown', 'green', 'red', 'white']
col_classes = ['black', 'brown', 'gray', 'green', 'pink', 'white', 'red', 'yellow', 'blue']
# col_classes = ['빨간색', '검정색', '회색', '남색', '노란색', '흰색', '핑크색', '초록색']


# def predict(filename, model_col):
#     img = load_img(filename, target_size=(224, 224))
#     img = img_to_array(img)
#     img = img.reshape(1, 224, 224, 3)
#
#     img = img.astype('float32')
#     img = img/255.0
#
#     result_col = model_col.predict(img)  # 색상 예측 결과 저장
#
#
#     dict_result_col = {}  # 색상 결과 딕셔너리
#
#     for i in range(6):
#         dict_result_col[result_col[0][i]] = col_classes[i]
#         # dict_result_col 에 result_col[0][i]가 '키'이고, col_classes[i]가 '값'이 되도록 추가
#
#     res_col = result_col[0]  # 색상 결과 1차원 리스트로 res_col 에 저장
#
#     res_col.sort()  # 각 카테고리가 될 확률을 순서대로 정렬
#
#     res_col = res_col[::-1]  # 정렬한 것 반대로
#
#     prob_col = res_col[:3]  # 상위 3개 따로 리스트(prob_col) 만들어서 저장
#
#     class_col_result = []
#
#     for i in range(3):
#         class_col_result.append(dict_result_col[prob_col[i]])
#
#
#     return class_col_result

def predict(filename, model_cat, model_col):
    img_cat = load_img(filename, target_size=(110, 110))
    img_cat = img_to_array(img_cat)
    img_cat = img_cat.reshape(1, 110, 110, 3)

    img_cat = img_cat.astype('float32')
    img_cat = img_cat/255.0

    img_col = load_img(filename, target_size=(224, 224))
    img_col = img_to_array(img_col)
    img_col = img_col.reshape(1, 224, 224, 3)

    img_col = img_col.astype('float32')
    img_col = img_col / 255.0

    result_col = model_col.predict(img_col)  # 색상 예측 결과 저장
    result_cat = model_cat.predict(img_cat)  # 카테고리 예측 결과 저장


    dict_result_col = {}  # 색상 결과 딕셔너리
    dict_result_cat = {}  # 카테고리 결과 딕셔너리

    for i in range(9):
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

# rgb추가하기
# def insertDB(color, col, path):
#     conn = sqlite3.connect('db.sqlite')
#     c = conn.cursor()
#     c.execute("select * from closet")
#     a = c.fetchall()
#     cnt = len(a)+1
#     c.execute("INSERT INTO closet VALUES (?, ?, ?, ?, ?, ?, ?)", [cnt, color, color, col[0], col[1], col[2], path])
#     conn.commit()
#     conn.close()

def insertDB(color, clothes, col, path):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute("select * from closet")
    a = c.fetchall()
    cnt = len(a)+1
    c.execute("INSERT INTO closet VALUES (?, ?, ?, ?, ?, ?, ?)", [cnt, color, clothes, col[0], col[1], col[2], path])
    conn.commit()
    conn.close()

def compareDB(color, clothes):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute("select color, clothes from closet")
    col_clo =c.fetchall()
    print(col_clo)
    result = ''
    cnt = 0
    for i,j in col_clo:
        if ((i==color) and (j==clothes)):
            cnt += 1

    result = "옷장에 비슷한 옷이 %d 개 있습니다." %cnt

    return result

def insertDB_lb(input_path, match_input):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute("select * from lookbook")
    a = c.fetchall()
    cnt = len(a) + 1
    c.execute("INSERT INTO lookbook VALUES (?, ?, ?)", [cnt, input_path, match_input])
    conn.commit()
    conn.close()


def showChart():
    conn = sqlite3.connect("./db.sqlite")
    c = conn.cursor()
    data = []
    clothes = ['dress', 'pants', 'shirt', 'shoes', 'shorts']
    col = ['black', 'blue', 'brown', 'green', 'red', 'white']
    list1 = []
    for j in clothes:
        clo_cat = {}
        clo_cat["name"] = j
        clo_cat["children"] = list1
        for i in col:
            clo = {}
            c.execute("select count(?) from closet where clothes = ? and color = ?", (i, j, i,))
            a = c.fetchall()
            clo["name"] = i
            clo['value'] = a[0][0]
            list1.append(clo)
        list1 = []
        data.append(clo_cat)
    c.close()
    return data


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template("main.html")

@app.route('/mycloset', methods=['GET', 'POST'])
def mycloset():
    if request.method == 'GET':
        return render_template("mycloset.html")

@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    if request.method == 'GET':
        return render_template("recommendation.html")

@app.route('/closetshare', methods=['GET', 'POST'])
def closetshare():
    name = 'world'
    return render_template('hello2.html', data=name)

@app.route('/hello2')
def hello2():
    return render_template("hello2.html")

@app.route('/getinfo')
def getinfo():
    # info = db.select_all()
    closet = Closet.query.all()
    # lookbook = Lookbook.query.all()
    # closet = Closet.query.all()
    return render_template("getinfo.html", closet=closet)

@app.route('/db_search', methods=['POST','GET'])
def db_search():
	if request.method=='POST':
		#temp = request.args.get('nm's)
		temp = request.form['color']
		closet = Closet.query.filter_by(color=temp)
		count = closet.counㅇt()
		return render_template("getinfo.html", closet=closet, cnt=count)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()  # 로그인폼
#     if form.validate_on_submit():  # 유효성 검사
#         print('{}가 로그인 했습니다'.format(form.data.get('userid')))
#         session['userid'] = form.data.get('userid')  # form에서 가져온 userid를 세션에 저장
#         return redirect('/')  # 성공하면 main.html로
#     return render_template('login.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     else:
#         userid = request.form['userid']
#         password = request.form['password']
#         # id와 pw가 임의로 정한 값이랑 비교 해서 맞으면 맞다 틀리면 틀리다
#     if userid == 'abc' and password == '1234':
#         session['userid'] = userid
#         return '''
#         <script> alert("안녕하세요~ {}님");
#         location.href="/form"
#         </script>
#     '''.format(userid)
#         # return redirect(url_for('form'))
#     else:
#         return "아이디 또는 패스워드를 확인 하세요."
#
# 로그인 사용자만 접근 가능으로 만들면
# @app.route('/form')
# def form():
#     if 'user' in session:
#         return render_template('test.html')
#     return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("register.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        userid = request.form.get('userid')
        email = request.form.get('email')
        password = request.form.get('password')
        password_2 = request.form.get('password')
        # print(password)  # 들어오나 확인해볼 수 있다.

        if not (userid and email and password and password_2):
            return "정보를 모두 입력해주세요."
        elif password != password_2:
            return "비밀번호가 일치하지 않습니다."
        else:  # 모두 입력이 정상적으로 되었다면 밑에명령실행(DB에 입력됨)
            fcuser = Fcuser()
            fcuser.userid = userid
            fcuser.email = email
            fcuser.password = password

            db.session.add(fcuser)
            db.session.commit()

            return "회원가입 성공"
        return redirect('/')


@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'GET':
        return render_template("compare.html")

@app.route('/upload_crop', methods=['GET', 'POST'])
def upload_cro():
    if request.method == 'GET':
        return render_template("upload_crop.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template("upload.html")

@app.route('/chart', methods=['GET','POST'])
def chart():
    if request.method == 'GET':
        result2 = showChart()
        return render_template("chart.html", result=result2)

@app.route('/tononin', methods=['GET', 'POST'])
def tononin():
    error = ''
    target_img = os.path.join(os.getcwd(), 'static/images')
    if request.method == 'GET':
        return render_template("tononin.html")


@app.route('/tononingrid', methods=['GET', 'POST'])
def tononingrid():
    # if request.method == 'GET':
    #     return render_template("tononingrid2.html")

    error = ''
    target_img = os.path.join(os.getcwd(), 'static/crop_images')  # 이미지 경로 내에 저장하는 코드 ,, ?
    if request.method == 'POST':
        if (request.files):
            file = request.files['file']
            if file and allowed_file(file.filename):
                img = file.filename
                # insertDB_lb(img, img)
                # cv2.imwrite(target_img+'cropped.png', file)
                file.filename = 'cropped.png'
                file.save(os.path.join(target_img, file.filename))
                img_path = os.path.join(target_img, file.filename)
                # img = file.filename

                cat_result, col_result = predict(img_path, model_cat, model_col)

                predictions = {
                    "class1": cat_result[0],
                    # "class2": cat_result[1],
                    # "class3": cat_result[2],
                    "prob1": col_result[0],
                    # "prob2": col_result[1],
                    # "prob3": col_result[2]
                }

                col = gc(img_path)
                print(col)
                # angle_result = get_angle(col)  # angle_result 는 딕셔너리임.
                # print(angle_result)
                tonon_list = tonOnTon(col)
                tonon_num = []
                for i in tonon_list:
                    i = int('0x'+i[1:],16)
                    tonon_num.append(i)
                tonin_list = tonInTon(col)
                tonin_num = []
                for i in tonin_list:
                    i = int('0x' + i[1:], 16)
                    tonin_num.append(i)
                # print(tonin_num)
                # print(tonon_num)


            else:
                error = "Please upload images of jpg , jpeg and png extension only"

            if (len(error) == 0):
                # return render_template('tononingrid2.html', tonon_list = tonon_list)
                return render_template('tononingrid.html', tonon_list=tonon_list, tonin_list=tonin_list, tonon_num = tonon_num,tonin_num = tonin_num, img=img, predictions=predictions)
            else:
                return render_template('tononingrid.html', error=error)
    else:
        return render_template('tononingrid.html')


@app.route('/tonon_rec', methods=['GET', 'POST'])
def tonon_rec():
    if request.method == 'GET':
        return render_template("tonon_rec.html")


@app.route('/tonin_rec', methods=['GET', 'POST'])
def tonin_rec():
    if request.method == 'GET':
        return render_template("tonin_rec.html")

@app.route('/checkmycloset', methods=['GET','POST'])
def checkmycloset():
     if request.method == 'GET':
        file_list = os.listdir("static/images")
        # print(file_list)
        return render_template("checkmycloset.html", file_list=file_list)

# @app.route('/lookbook2', methods=['GET','POST'])
# def lookbook2():
#     if request.method == 'GET':
#          # file_list = os.listdir('static/images')
#         # return render_template("lookbook.html", file_list = file_list)
#         return render_template("lookbook2.html")

@app.route('/lookbook', methods=['GET', 'POST'])
def lookbook():
    if request.method == 'GET':
        conn=sqlite3.connect('db.sqlite')
        c= conn.cursor()
        c.execute("select input_path, match_path from lookbook")
        file_list=c.fetchall()
        conn.close()
        print(file_list)
        return render_template("lookbook.html", file_list=file_list)

@app.route('/compare_success', methods=['GET', 'POST'])
def compare_success():
    error = ''
    target_img = os.path.join(os.getcwd(), 'static/images')
    if request.method == 'POST':
        if (request.form):
            link = request.form.get('link')
            try:
                resource = urllib.request.urlopen(link)
                unique_filename = str(uuid.uuid4())
                filename = unique_filename + ".jpg"
                img_path = os.path.join(target_img, filename)
                output = open(img_path, "wb")
                output.write(resource.read())
                output.close()
                img = filename

                cat_result, col_result = predict(img_path, model_cat, model_col)

                predictions = {
                    "class1": cat_result[0],
                    # "class2": cat_result[1],
                    # "class3": cat_result[2],
                    "prob1": col_result[0],
                    # "prob2": col_result[1],
                    # "prob3": col_result[2]
                }

                col = gc(img_path)
                result = compareDB(predictions["prob1"], predictions["class1"])

            except Exception as e:
                print(str(e))
                error = 'This image from this site is not accesible or inappropriate input'
            if (len(error) == 0):
                return render_template('compare_success.html', img=img, predictions=predictions, result=result)
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
                    # "class2": cat_result[1],
                    # "class3": cat_result[2],
                    "prob1": col_result[0],
                    # "prob2": col_result[1],
                    # "prob3": col_result[2]
                }

                col = gc(img_path)
                result = compareDB(predictions["prob1"], predictions["class1"])

            else:
                error = "Please upload images of jpg , jpeg and png extension only"

            if (len(error) == 0):
                return render_template('compare_success.html', img=img, predictions=predictions, result=result)
            else:
                return render_template('index.html', error=error)

    else:
        return render_template('compare.html')

@app.route('/upload_success', methods=['GET', 'POST'])
def upload_success():
    error = ''
    target_img = os.path.join(os.getcwd(), 'static/images')
    if request.method == 'POST':
        if (request.files):
            file = request.files['file']
            if file and allowed_file(file.filename):
                file.save(os.path.join(target_img, file.filename))
                img_path = os.path.join(target_img, file.filename)
                img = file.filename

                cat_result, col_result = predict(img_path, model_cat, model_col)

                predictions = {
                    "class1": cat_result[0],
                    # "class2": cat_result[1],
                    # "class3": cat_result[2],
                    "prob1": col_result[0],
                    # "prob2": col_result[1],
                    # "prob3": col_result[2]
                }

                col = gc(img_path)
                insertDB(predictions["prob1"],predictions["class1"], col, img) #rgb, path 값도 같이 넘겨주는 db코드

            else:
                error = "Please upload images of jpg , jpeg and png extension only"

            if (len(error) == 0):
                return render_template('upload_success.html', img=img, predictions=predictions)
            else:
                return render_template('upload_success.html', error=error)

    else:
        return render_template('upload_success.html')

# @app.route('/newupload_success', methods=['GET', 'POST'])
# def newupload_success():
#     error = ''
#     target_img = os.path.join(os.getcwd(), 'static/images')
#     if request.method == 'POST':
#         if (request.files):
#             file = request.files['file']
#             if file and allowed_file(file.filename):
#                 file.save(os.path.join(target_img, file.filename))
#                 img_path = os.path.join(target_img, file.filename)
#                 img = file.filename
#
#                 col_result = predict(img_path, model_col)
#
#                 predictions = {
#                     # "class1": cat_result[0],
#                     # "class2": cat_result[1],
#                     # "class3": cat_result[2],
#                     "prob1": col_result[0]
#                     # "prob2": col_result[1],
#                     # "prob3": col_result[2]
#                 }
#
#                 col = gc(img_path)
#                 # insertDB(predictions["prob1"],predictions["class1"], col, img) #rgb, path 값도 같이 넘겨주는 db코드
#                 insertDB(predictions["prob1"], col, img)
#             else:
#                 error = "Please upload images of jpg , jpeg and png extension only"
#
#             if (len(error) == 0):
#                 return render_template('newupload_success.html', img=img, predictions=predictions)
#             else:
#                 return render_template('index.html', error=error)
#
#     else:
#         return render_template('index.html')

@app.route('/success_rec', methods=['GET', 'POST'])
def success_rec():
    error = ''
    target_img = os.path.join(os.getcwd(), 'static/images')
    if request.method == 'POST':
        if (request.form):
            link = request.form.get('link')
            try:
                resource = urllib.request.urlopen(link)
                unique_filename = str(uuid.uuid4())
                filename = unique_filename + ".jpg"
                img_path = os.path.join(target_img, filename)
                output = open(img_path, "wb")
                output.write(resource.read())
                output.close()
                img = filename

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

            if (len(error) == 0):
                return render_template('recommendation_success.html', img=img, predictions=predictions)
            else:
                return render_template('recommendation.html', error=error)

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

            if (len(error) == 0):
                return render_template('recommendation_success.html', img=img, predictions=predictions)
            else:
                return render_template('recommendation.html', error=error)

    else:
        return render_template('recommendation.html')



@app.route('/upload_edit_proc', methods=['GET', 'POST'])
def upload_edit_proc():
    if request.method == 'GET':
        return render_template("upload_success.html")
    else:
        upload_color = request.form.get('color')
        upload_clothes = request.form.get('clothes')
        if not (upload_color and upload_clothes):
            return "모두 입력해주세요"
        else:
            closet = Closet()
            closet.color = upload_color
            closet.clothes = upload_clothes

            conn = sqlite3.connect('db.sqlite')
            c = conn.cursor()
            c.execute("UPDATE closet SET color=?, clothes=? WHERE id = (SELECT max(id) FROM closet)",(upload_color, upload_clothes))
            # query = "UPDATE closet SET color='upload_color', clothes='clothes' WHERE id = (SELECT max(id) FROM closet)"
            # result = c.execute(query)

            # db.session.add(closet)
            conn.commit()
            conn.close()

            return redirect('/upload_crop')

@app.route('/ton_on', methods = ["POST"])
def ton_on():
    print("/tonon request.method : ", request.method)
    if request.method == 'POST':
        path = './static/images/'
        name = request.get_json()
        print('data', name)
        new_data = []
        for i in name["tonon"]:
            new_data.append(hex(i)[2:])
        closet_list = []
        print("new_data", new_data)
        for i in new_data:
            closet_list.append(path + findClothes(i,name["category"])) # i는 list type
        len_tonon = len(closet_list)
        closet_list = list(set(closet_list))
        if len(closet_list) != len_tonon:
            while(len(closet_list) == len_tonon):
                closet_list.append('.')
        print("closet_list", closet_list)
        # print(closet_list)
        return jsonify({'path': closet_list})

@app.route('/ton_in', methods = ["POST"])
def ton_in():
    print("/tonon request.method : ", request.method)
    if request.method == 'POST':
        path = './static/images/'
        name = request.get_json()
        print('data', name)
        new_data = []
        for i in name["tonin"]:
            new_data.append(hex(i)[2:])
        closet_list = []
        for i in new_data:
            closet_list.append(path + findClothes(i,name["category"])) # i는 list type
        len_tonin = len(closet_list)
        closet_list = list(set(closet_list))
        if len(closet_list) != len_tonin:
            while (len(closet_list) == len_tonin):
                closet_list.append('.')
        return jsonify({'path': closet_list})

@app.route('/save_clothes', methods=['POST'])
def save_clothes():
    if request.method == "POST":
        clothes_path = request.get_json()
        data = clothes_path["selected"]
        input_data = clothes_path["input"]

        lookbook = Lookbook()
        lookbook.match_path = data

        conn = sqlite3.connect('db.sqlite')
        c = conn.cursor()
        c.execute("select * from lookbook")
        a = c.fetchall()
        cnt = len(a) + 1

        c.execute("INSERT into lookbook VALUES (?,?, ?)", [cnt, input_data, data])
        conn.commit()
        conn.close()

        print(data)

        return jsonify(clothes_path)

        return redirect('/tononingrid')


if __name__ == "__main__":

    basedir = os.path.abspath(os.path.dirname(__file__))  # database 경로를 절대경로로 설정함
    dbfile = os.path.join(basedir, 'db.sqlite')  # 데이터베이스 이름과 경로
    dbfile2 = os.path.join(basedir, 'lookbookdb.sqlite')  # 데이터베이스 이름과 경로
    dbfile3 = os.path.join(basedir, 'fcuserdb.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile2
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile3

    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 사용자에게 원하는 정보를 전달완료했을때가 TEARDOWN, 그 순간마다 COMMIT을 하도록 한다.라는 설정
    # 여러가지 쌓아져있던 동작들을 Commit을 해주어야 데이터베이스에 반영됨. 이러한 단위들은 트렌젝션이라고함.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # True하면 warrnig메시지 유발,

    db.init_app(app)  # 초기화 후 db.app에 app으로 명시적으로 넣어줌
    db.app = app
    db.create_all()  # 이 명령이 있어야 생성됨. DB가

    db_lookbook.init_app(app)  # 초기화 후 db.app에 app으로 명시적으로 넣어줌
    db_lookbook.app = app
    db_lookbook.create_all()  # 이 명령이 있어야 생성됨. DB가

    db_login.init_app(app)  # 초기화 후 db.app에 app으로 명시적으로 넣어줌
    db_login.app = app
    db_login.create_all()  # 이 명령이 있어야 생성됨. DB가

    app.run(host='0.0.0.0', debug=True)

