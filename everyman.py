#!/usr/bin/env python

import matplotlib.pyplot as plt
from datetime import datetime, date, time, timedelta

TOTAL_AWAKE_TIME = time(19,30)
TOTAL_ASLEEP_TIME = time(4,30)

def check_times(core, nap, awakes):
    total_awake_time = datetime.combine(date.today(), time(0,0))
    for i in range(4): total_awake_time += awakes[i]
    total_awake_time = total_awake_time.time()
    assert total_awake_time == TOTAL_AWAKE_TIME

    total_asleep_time = (datetime.combine(date.today(), time(0,0)) + nap*3 + core).time()
    assert total_asleep_time == TOTAL_ASLEEP_TIME

    assert (datetime.combine(date.today(), total_awake_time) + timedelta(hours=total_asleep_time.hour, minutes=total_asleep_time.minute)).time() == time(0,0)

def compute_times(initial=(0,0), core_rank=0, core=(3,30), nap=(0,20),
                  awakes=[(5,30), (4,30), (4,30), (5,0)]):
    core = timedelta(hours=core[0], minutes=core[1])
    nap = timedelta(hours=nap[0], minutes=nap[1])
    for i in range(4): awakes[i] = timedelta(hours=awakes[i][0], minutes=awakes[i][1])

    check_times(core, nap, awakes)

    times = []
    s = e = datetime.combine(date.today(), time(*initial))

    for i in range(4):
        d = (core if core_rank == i else nap)
        s = e; e = s + d; times.append((s.time(), e.time(), d))
        s = e; e = s + awakes[i]; times.append((s.time(), e.time(), awakes[i]))

    return times

fig, axes = plt.subplots(nrows=2, ncols=2)

explode = (.1, 0, .1, 0, .1, 0, .1, 0,)
colors = ['gold', 'lightskyblue',]

for ax, initial, rank, aa in [(axes[0,0], (22,0), 0, [(5,30), (4,30), (4,30), (5,0)]),
                              (axes[0,1], (22,0), 0, [(4,30), (5,30), (4,30), (5,0)]),
                              (axes[1,0], (22,0), 0, [(5,30), (4,30), (4,30), (5,0)]),
                          ]:
    times = compute_times(initial=initial, core_rank=rank, awakes=aa)
    sizes = [t[2].seconds for t in times]
    labels = ['%s\n%s' % (s.strftime('%H:%M'),e.strftime('%H:%M')) for s,e,d in times]

    ax.pie(list(reversed(sizes)), labels=list(reversed(labels)),
           explode=list(reversed(explode)), colors=list(reversed(colors)),
           shadow=True, startangle=(-(initial[0]*60+initial[1])/(24*60))*360+90,
           #autopct='%1.1f%%'
    )
    ax.axis('equal')

plt.show()
