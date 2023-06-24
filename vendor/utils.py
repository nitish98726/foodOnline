from datetime import time
def list_of_time():
    l = []
    for h in range(0,24):
        for m in (0,30):
            t = (time(h,m).strftime('%I:%M %p'))
            l.append((t,t))
    return l 