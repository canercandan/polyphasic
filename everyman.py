#!/usr/bin/env python

import matplotlib.pyplot as plt
from datetime import datetime, date, time, timedelta

def compute_times(initial=(0,0), core_rank=0, core=(3,30), nap=(0,20),
                  awake1=(5,30), awake2=(4,30), awake3=(4,30), awake4=(5,0)):
    core = timedelta(hours=core[0], minutes=core[1])
    nap = timedelta(hours=nap[0], minutes=nap[1])
    awake1 = timedelta(hours=awake1[0], minutes=awake1[1])
    awake2 = timedelta(hours=awake2[0], minutes=awake2[1])
    awake3 = timedelta(hours=awake3[0], minutes=awake3[1])
    awake4 = timedelta(hours=awake4[0], minutes=awake4[1])

    total_awake_time = (datetime.combine(date.today(), time(0,0)) + awake1 + awake2 + awake3 + awake4).time()
    assert total_awake_time == time(19,30)

    total_asleep_time = (datetime.combine(date.today(), time(0,0)) + nap*3 + core).time()
    assert total_asleep_time == time(4,30)

    assert (datetime.combine(date.today(), total_awake_time) + timedelta(hours=total_asleep_time.hour, minutes=total_asleep_time.minute)).time() == time(0,0)

    times = []
    s = e = datetime.combine(date.today(), time(*initial))
    d = (core if core_rank == 0 else nap); s = e; e = s + d; times.append((s.time(), e.time(), d))
    s = e; e = s + awake1; times.append((s.time(), e.time(), awake1))
    d = (core if core_rank == 1 else nap); s = e; e = s + d; times.append((s.time(), e.time(), d))
    s = e; e = s + awake2; times.append((s.time(), e.time(), awake2))
    d = (core if core_rank == 2 else nap); s = e; e = s + d; times.append((s.time(), e.time(), d))
    s = e; e = s + awake3; times.append((s.time(), e.time(), awake3))
    d = (core if core_rank == 3 else nap); s = e; e = s + d; times.append((s.time(), e.time(), d))
    s = e; e = s + awake4; times.append((s.time(), e.time(), awake4))
    return times

fig, axes = plt.subplots(nrows=2, ncols=2)

explode = (.1, 0, .1, 0, .1, 0, .1, 0,)
colors = ['gold', 'lightskyblue', 'gold', 'lightskyblue',
          'gold', 'lightskyblue', 'gold', 'lightskyblue',]

for ax, initial, rank, a1, a2, a3, a4 in [(axes[0,0], (22,0), 0, (5,30), (4,30), (4,30), (5,0)),
                                          (axes[0,1], (22,0), 0, (4,30), (5,30), (4,30), (5,0)),
                                          (axes[1,0], (22,0), 0, (5,30), (4,30), (4,30), (5,0)),
                                      ]:
    times = compute_times(initial=initial, core_rank=rank, awake1=a1, awake2=a2, awake3=a3, awake4=a4)
    sizes = [t[2].seconds for t in times]
    labels = ['%s\n%s' % (s.strftime('%H:%M'),e.strftime('%H:%M')) for s,e,d in times]

    ax.pie(list(reversed(sizes)), labels=list(reversed(labels)),
           explode=list(reversed(explode)), colors=list(reversed(colors)),
           shadow=True, startangle=(-(initial[0]*60+initial[1])/(24*60))*360+90,
           #autopct='%1.1f%%'
    )
    ax.axis('equal')

plt.show()
