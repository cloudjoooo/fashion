import sqlite3
import numpy as np

def calDist(a:list,b:list): # 값 두 개를 받아서 두 점 사이 계산
    a = np.array(a)
    b = np.array(b)
    result = np.linalg.norm(a-b)
    return result

def hex_to_int(a:str):
    a = str(a)
    print(a)
    col = []
    col.append(int(a[:4],16))
    col.append(int('0x'+a[4:6],16))
    col.append(int('0x'+a[6:],16))
    return col

def cal_dist_ver2(new_list, col): # new_list 를 어떻게 받아올 건지 생각. 왜? [(1, 'shirt', 36, 60, 37)] 데이터가 이런 형태임.
    result_dict = {}
    col = [int('0x'+col[:2],16), int('0x'+col[2:4],16), int('0x'+col[4:],16)]
    for i in new_list:
        result = calDist((i[2], i[3], i[4]), col) # new_list 요소의 i 와 color 리스트의 거리를 계산함.
        result_dict[i[0]] = result
    key = list(result_dict.keys())[0]
    # print("key——>", key)
    # print(result_dict) -> 나중에 지우기
    return str(key)

def setArange(category): ## 추가한 함수 : 공유할 때 같이 보내기
    if category == 'dress':
        choosable = ['shoes']
        return choosable
    elif category == 'pants':
        choosable = ['shirt', 'shoes']
        return choosable
    elif category == 'shirt':
        choosable = [ 'pants', 'shorts', 'shoes']
        return choosable
    elif category == 'shorts':
        choosable = ['shirt', 'shoes']
        return choosable
    else: # shoes
        choosable = ['dress', 'pants', 'shirt', 'shorts']
        return choosable

def findClothes(col, category): # findClothes 뉴버전
    conn = sqlite3.connect('./db.sqlite')
    c = conn.cursor()
    c.execute("select id, clothes, red, green, blue from closet")
    rgb_list = c.fetchall()
    choosable = setArange(category) #  카테고리를 인자로 넘기면 코디가 가능한 옷들이 리스트로 반환됨.
    new_list = []
    for i in rgb_list: # 만약 내 옷장에 있는 옷 중
        if i[1] in choosable: # 코디가 가능한 옷들이 리스트 내에 있으면 (원래 not in 사용하려고 했으나, 결과가 제대로 나오지 않아서 새로 리스트를 만들었음)
            new_list.append(i) # 그 row를 new_list 에 저장 -> 이제 여기서는 원하는 옷들만 저장되었으므로 카테고리 요소를 계속 가져갈 필요 없음.
    print(new_list) # [(1, 'shirt', 36, 60, 37)]
    a = cal_dist_ver2(new_list, col) # -> 바뀐 버전 # 10이하의 거리로 임계치를 두고싶으면 이 함수를 수정해야 함.
    #a = sorted(a.items(), key=lambda x: x[1])
    c.execute("select path from closet where id=(?)", a) # 첫번째 값(a[0])만 사용 Q. 그럼 cal_dist_ver2 함수에서 딕셔너리를 모두 넘길 필요가 있을까?,,
    # ——> 그래서 수정함. 가장 짧은 거리를 가지는 옷의 id 값만 return 해서 받아오기
    path_clothes = c.fetchall()
    # print(path_clothes[0][0])  # return 하던지 출력하던지
    path = path_clothes[0][0] # db 와 연결을 끊어 주어야 하므로, 변수에 할당 한 번 해주어야 함.
    conn.close()

    return path # 이미지 경로(이미지 파일 이름 return)



