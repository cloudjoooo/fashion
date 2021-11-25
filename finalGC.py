import cv2
import numpy as np
from sklearn.cluster import KMeans
from extract_color import palette_perc
# from recoColor import tonOnTon


def gc(name):
    src = cv2.imread(name)
    # # print("src.shape[:2]", src.shape[:2]) # (1500, 1000) 세로 가로
    # # print("src.shape[:2][0], src.shape[:2][1]", src.shape[:2][0], src.shape[:2][1])
    # mask = np.zeros(src.shape[:2], np.uint8)
    # bgdModel = np.zeros((1,65), np.float64)
    # fgdModel = np.zeros((1, 65), np.float64)

    # # rc = cv2.selectROI(src)
    # rc = (1,1,src.shape[:2][0],src.shape[:2][1])
    # # print("rc",rc)
    # cv2.grabCut(src, mask, rc, bgdModel, fgdModel, 1, cv2.GC_INIT_WITH_RECT)

    # mask2 = np.where((mask==0)|(mask==2),0,1).astype('uint8')
    # dst = src * mask2[:,:,np.newaxis]

    # # cv2.imshow('dst', dst)
    # # cv2.waitKey()
    # # cv2.destroyAllWindows()

    # cv2.imwrite('./out_' + name, dst)  # output img save
    output = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    dim = (500, 300)
    output = cv2.resize(output, dim, interpolation=cv2.INTER_AREA)
    clt = KMeans(n_clusters=5)
    clt1 = clt.fit(output.reshape(-1, 3))
    perc, rgb_pal = palette_perc(clt1)
    top_perc = list(perc.keys())[0]
    col = rgb_pal[top_perc]  # rgb 중 최빈값
    col.astype(int)

    return col