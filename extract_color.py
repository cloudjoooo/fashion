# Load packages

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Load and show sample img
def show_img_compar(img_1, img_2):
    f, ax = plt.subplots(1, 2, figsize=(10,10))
    ax[0].imshow(img_1)
    ax[1].imshow(img_2)
    ax[0].axis('off')
    ax[1].axis('off')
    f.tight_layout()
    plt.show()

def palette_perc(k_cluster):
    width = 300
    palette = np.zeros((50, width, 3), np.uint8)

    n_pixels = len(k_cluster.labels_)
    counter = Counter(k_cluster.labels_)
    perc={}

    for i in counter:
        perc[i] = np.round(counter[i]/n_pixels,2)

    perc=dict(sorted(perc.items(), key=lambda x: x[1], reverse=True))

    # for logging purpose

    print(perc)
    print(k_cluster.cluster_centers_)

    step=0

    for idx, centers in enumerate(k_cluster.cluster_centers_):
        palette[:, step:int(step+perc[idx]*width+1), :] = centers
        step += int(perc[idx]*width+1)

    return perc, k_cluster.cluster_centers_

'''
clt1 = clt.fit(img.reshape(-1,3))
show_img_compar(img, palette_perc(clt1))'''
