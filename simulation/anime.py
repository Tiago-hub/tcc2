import matplotlib.pyplot as plt 
from matplotlib import animation 
from mpl_toolkits.mplot3d import Axes3D 
from matplotlib.animation import PillowWriter

class Anime:
    def __init__(self,x1,x2,y1,y2):
        self.x1=x1
        self.x2=x2
        self.y1=y1
        self.y2=y2
    
    def animate(self,i):
        self.ln1.set_data([0, self.x1[i], self.x2[i]], [0,self.y1[i], self.y2[i]])

    def generateAnimation(self):
        fig, ax = plt.subplots(1,1, figsize=(8,8))
        ax.set_facecolor('k')
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        self.ln1, = plt.plot([], [], 'ro--', lw=3, markersize=8)
        ax.set_ylim(-4,4)
        ax.set_xlim(-4,4)
        ani = animation.FuncAnimation(fig,self.animate,frames=len(self.x1),interval=0.1)
        ani.save('pen.gif',writer='pillow',fps=120)