import numpy as np

def rgb_to_hex(a:list):
    r, g, b = int(a[0]), int(a[1]), int(a[2])
    return '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)

def tonOnTon(a:list):
    a = np.array(a)
    tot_list =[]
    bl = a/4
    wh = (255-a)/4
    from_0 = []
    from_f = []
    for i in range(1,4):
        from_0.append(list((i*bl).round()))
    for i in range(1,4):
        from_f.append(list(((i*wh)+a).round()))
    for i in from_0:
        hex_col = rgb_to_hex(i)
        tot_list.append(hex_col)
    # hex_col = rgb_to_hex(list(a))
    # tot_list.append(hex_col)
    for i in from_f:
        hex_col = rgb_to_hex(i)
        tot_list.append(hex_col)
    print(tot_list)
    #draw_tot.draw_bar(tot_list)
    return tot_list

def tonInTon(a):
    r, g, b = int(a[0]), int(a[1]), int(a[2])
    color_pal = []

    rMax = max(g,b)
    rMin = min(g,b)
    gMax = max(r,b)
    gMin = min(r,b)
    bMax = max(r,g)
    bMin = min(r,g)


    for i in range(rMin, rMax, (rMax-rMin)//2): # red change
        if i == rMin:
            continue
        else:
            color_pal.append([i, g, b])
            color_pal.append([i, b, g])
    for i in range(gMin, gMax, (gMax-gMin)//2): # green change
        if i == rMin:
            continue
        else:
            color_pal.append([r, i, b])
            color_pal.append([b, i, r])
    for i in range(bMin, bMax, (bMax-bMin)//2): # blue change
        if i == rMin:
            continue
        else:
            color_pal.append([r, g, i])
            color_pal.append([g, r, i])
    color_pal.append(a) # 기준 색상 +
    for i in range(len(color_pal)):
        color_pal[i] = rgb_to_hex(color_pal[i])
    # draw_tot.draw_bar(color_pal)
    print(color_pal)
    return color_pal


def tonInTon(a):
    r, g, b = int(a[0]), int(a[1]), int(a[2])

    rMax = max(g, b)
    rMin = min(g, b)
    gMax = max(r, b)
    gMin = min(r, b)
    bMax = max(r, g)
    bMin = min(r, g)
    rMid = (rMax - rMin) / 2 + rMin
    gMid = (gMax - gMin) / 2 + gMin
    bMid = (bMax - bMin) / 2 + bMin
    color_pal = [[rMin, g, b], [rMax, g, b], [rMid, g, b],
    [rMin, b, g], [rMax, b, g], [rMid, b, g],
    [b, gMin, r], [b, gMax, r], [b, gMid, r],
    [r, gMin, b], [r, gMax, b], [r, gMid, b],
    [r, g, bMid], [r, g, bMax], [r, g, bMid],
    [g, r, bMid], [g, r, bMax], [g, r, bMid]]

    color_pal = [[rMin, g, b], [rMax, g, b],
                 [rMin, b, g], [rMax, b, g],
                 [b, gMin, r], [b, gMax, r],
                 [r, gMin, b], [r, gMax, b],
                 [r, g, bMid], [r, g, bMax],
                 [g, r, bMid], [g, r, bMax]]

    for i in range(len(color_pal)):
        color_pal[i] = rgb_to_hex(color_pal[i])

    return color_pal