import matplotlib.pyplot as plt
import numpy as np


#color = ['#F6DCE0','#EDBAC1','#E498A2','#DB7683','#A45862','#6D3B41','#361D20']
# color = x
def draw_bar(hexColor:list):
    y_val = [100]
    y_val *= len(hexColor)
    barlist = plt.bar(hexColor, y_val)
    for i in range(len(y_val)):
        barlist[i].set_color(hexColor[i])
    plt.show()

