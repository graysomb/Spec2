'''
Created on Oct 13, 2015

@author: graysomb
'''
import numpy as np
import multiprocessing as mp
import time
import matplotlib.pyplot as plt

def f(conn):
    conn.send([42, None, 'hello'])
    conn.send([42, None])
    conn.close()
    
if __name__ == '__main__':
    parent_conn, child_conn = mp.Pipe()
    p = mp.Process(target=f, args=(child_conn,))
    p.start()
    p.join()
    print parent_conn.recv()   # prints "[42, None, 'hello']"
    print parent_conn.recv()


'''
x = np.linspace(0, 6*np.pi, 100)
y = np.sin(x)

# You probably won't need this if you're embedding things in a tkinter plot...
plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x, y, 'r-') # Returns a tuple of line objects, thus the comma

for phase in np.linspace(0, 10*np.pi, 500):
    line1.set_ydata(np.sin(x + phase))
    fig.canvas.draw()
'''
    
    
    