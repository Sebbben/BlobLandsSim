def clamp(value, minV, maxV):
    return min(maxV, max(value, minV))

def avrg(l:list):
    if len(l) == 0:
        return 0
    else:
        return sum(l)//len(l)
