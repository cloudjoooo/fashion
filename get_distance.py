import numpy as np
import numpy.linalg as LA


color_dict = {'red':[255, 0, 0], 'green':[0, 255, 0], 'blue':[0, 0, 255],
              'brown':[165, 42, 42], 'purple':[156, 39, 176], 'pink':[225, 128, 171], 'yellow':[255,255,0]}
grayscale = {'black':[0,0,0], 'white': [255,255,255], 'gray':[128,128,128] }

def cal_distance(a:list):
    point = np.array([255,255,255])
    a = np.array(a)
    result = np.linalg.norm(a-point)
    print(result)
    
# cal_distance([109, 85, 83])
# cal_distance([109, 86, 81])
# cal_distance([98,92,71])
# cal_distance([85, 95, 76])
# cal_distance([77,97,85])
# cal_distance([72, 96, 94])
# cal_distance([39,85,105])
# cal_distance([64, 79, 112])
# cal_distance([90, 72, 108])
# cal_distance([101, 65, 92])

def get_dist(a:list): # black, white, gray 중 어떤 점과 가까운지 거리를 구하는 함수
    dist_dict = {}
    for color, d in list(grayscale.items()):
        a = np.array(a)
        d = np.array(d)
        dist = np.linalg.norm(a-d)
        dist_dict[color] = dist
    sort_dist = sorted(dist_dict.items(), key=lambda x:x[1])
    print(sort_dist) # 현재 딕셔너리를 모두 보여주고 있으나, 상황에 따라 가장 짧은 거리를 가지는 색상값만 return 하도록 수정 가능


def check_grayscale(a:list): # rgb값에서 각 요소끼리의 차가 10이하이면 grayscale로 간주한다.
    cnt = 0
    for i in range(0, 2):  # 3
        for j in range(1, 3):
            if i != j:
                result = a[i] - a[j]
                print(i, j)
                print(result)
                if abs(result) > 10: # 수정 가능
                    cnt += 1
    return cnt # 10을 넘는 값이 몇 개인지 return

def get_angle(a:list):
    angle_dict = {} # 색상명과 그 색상 벡터와의 각도
    cnt = check_grayscale(a)
    if cnt == 0: # gray scale
        distance = get_dist(a)
        print(distance)
    else: # rgb channel
        for color, d in list(color_dict.items()):

            a = np.array(a)
            d = np.array(d)

            inner = np.inner(a, d)
            norms = LA.norm(a) * LA.norm(d)

            cos = inner / norms
            rad = np.arccos(np.clip(cos, -1.0, 1.0))
            deg = np.rad2deg(rad)
            angle_dict[color] = deg
        angle_dict = sorted(angle_dict.items(), key=lambda x:x[1])
        # print(angle_dict) # 현재 딕셔너리를 모두 보여주고 있으나, 상황에 따라 가장 짧은 거리를 가지는 색상값만 return 하도록 수정 가능
        return angle_dict
'''
get_angle([19, 21, 15])
# 값이 잘 나오는지 check
'''
get_angle([255, 235, 238])