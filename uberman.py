#!/usr/bin/env python

import matplotlib.pyplot as plt
from datetime import datetime, date, time, timedelta

TOTAL_AWAKE_TIME = time(22,0)
TOTAL_ASLEEP_TIME = time(2,0)

def check_times(num, nap, awake):
    total_awake_time = (datetime.combine(date.today(), time(0,0)) + awake*num).time()
    assert total_awake_time == TOTAL_AWAKE_TIME

    total_asleep_time = (datetime.combine(date.today(), time(0,0)) + nap*num).time()
    assert total_asleep_time == TOTAL_ASLEEP_TIME

    assert (datetime.combine(date.today(), total_awake_time) + timedelta(hours=total_asleep_time.hour, minutes=total_asleep_time.minute)).time() == time(0,0)

def compute_times(initial=(0,0), num=6, nap=(0,20), awake=(3,40)):
    nap, awake = timedelta(hours=nap[0], minutes=nap[1]), timedelta(hours=awake[0], minutes=awake[1])
    check_times(num, nap, awake)

    times = []
    s = e = datetime.combine(date.today(), time(*initial))
    for i in range(num):
        d = nap; s = e; e = s + d; times.append((s.time(), e.time(), d))
        s = e; e = s + awake; times.append((s.time(), e.time(), awake))

    return times

fig, axes = plt.subplots(nrows=1, ncols=1)

explode = (.1, 0, .1, 0, .1, 0, .1, 0, .1, 0, .1, 0,)
colors = ['gold', 'lightskyblue',]

for ax, initial in [(axes, (8,45)),
                    # (axes[0,1], (22,0)),
                    # (axes[1,0], (22,0)),
                ]:
    times = compute_times(initial=initial)
    sizes = [t[2].seconds for t in times]
    labels = ['%s\n%s' % (s.strftime('%H:%M'),e.strftime('%H:%M')) for s,e,d in times]

    ax.pie(list(reversed(sizes)), labels=list(reversed(labels)),
           explode=list(reversed(explode)), colors=list(reversed(colors)),
           shadow=True, startangle=(-(initial[0]*60+initial[1])/(24*60))*360+90,
           #autopct='%1.1f%%',
    )
    ax.axis('equal')

plt.show()
