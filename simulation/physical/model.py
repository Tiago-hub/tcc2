import numpy as np
from numpy import sin, cos
from sympy import Matrix

g = 9.8
class double_pendulum:

    def __init__(self, m1, m2, l1, l2, w1, w2, q1=0, q2=0, b1=0, b2=0, a1=0, a2=0, tal1 = [], tal2 = []):
        """"set initial values of the mathematical model of the double pendulum:
            m(x) -> mass of beam x
            l(x) -> center of mass position along beam x axis
            w(x) -> beam x length
            q(x) -> angle betwen beam x and the vertical axis
            b(x) -> friction coefficient on the x rotational axis
            a(x) -> angular acceleration on the x rotational axis"""
        self.m1 = m1
        self.l1 = l1
        self.w1 = w1
        self.m2 = m2
        self.l2 = l2
        self.w2 = w2
        self.q1 = q1
        self.q1_ = 0
        self.q1__ = 0
        self.q2 = q2
        self.q2_ = 0
        self.q2__ = 0
        self.b1 = b1
        self.b2 = b2
        self.a1 = a1
        self.a2 = a2
        self.g = 9.8
        self.tal1 = tal1
        self.tal2 = tal2
        self.time_keys = list(tal1.keys())
        self.current_index = 0
        self.Gen2Cart(self.q1, self.q2, self.w1, self.w2)

    def Gen2Cart(self, q1, q2, w1, w2):
        self.x1 = self.w1 * np.sin(self.q1)
        self.x2 = self.x1 + self.w2 * np.sin(self.q2)
        self.y1 = -self.w1 * np.cos(self.q1)
        self.y2 = self.y1 + -1*self.w2*np.cos(self.q2)
        return (self.x1, self.y1, self.x2, self.y2)

    def set_initial_conditions(self,initial_state):
        """
            x1 -> velocity of q1
            x2 -> velocity of q2
            x3 -> position of q1
            x4 -> position of q2
            a1 -> angular acceleration imposed to q1 by actuator
            a2 -> angular acceleration imposed to q2 by actuator
        """
        self.q1_, self.q2_, self.q1, self.q2, self.a1, self.a2 = initial_state

    def dpend_dt(self,x, t):
        
        m1 = self.m1
        m2 = self.m2
        l1 = self.l1
        l2 = self.l2
        w1 = self.w1
        w2 = self.w2
        g = self.g
        b1 = self.b1
        b2 = self.b2

        x1, x2, x3, x4 = x

        tal1 = self.tal1[self.time_keys[self.current_index]]
        tal2 = self.tal2[self.time_keys[self.current_index]]
        if t > self.time_keys[self.current_index]:
            if self.current_index + 1 < len(self.time_keys):
                self.current_index += 1

        dxdt = np.array([   x2,
                            -(b1*l1*l2*x2 - 2*l2*tal2*w1 - 2*l1*l2*tal1 + 2*l1*tal2*w1*cos(x1 - x3) - b2*l1*w1*x4*cos(x1 - x3) + g*l1**2*l2*m1*sin(x1) + g*l1*l2*m2*w1*sin(x1) + l1*l2**2*m2*w1*x4**2*sin(x1 - x3) - g*l1*l2*m2*w1*cos(x1 - x3)*sin(x3) + l1*l2*m2*w1**2*x2**2*cos(x1 - x3)*sin(x1 - x3))/(l1*l2*(l1**2*m1 + m2*w1**2 - m2*w1**2*cos(x1 - x3)**2)),
                            x4,
                            (2*l1**3*m1*tal2 - b2*l1**3*m1*x4 + 2*l1*m2*tal2*w1**2 - 2*l2*m2*tal2*w1**2*cos(x1 - x3) - b2*l1*m2*w1**2*x4 - g*l1*l2*m2**2*w1**2*sin(x3) - 2*l1*l2*m2*tal1*w1*cos(x1 - x3) - g*l1**3*l2*m1*m2*sin(x3) + l1*l2*m2**2*w1**3*x2**2*sin(x1 - x3) + b1*l1*l2*m2*w1*x2*cos(x1 - x3) + g*l1*l2*m2**2*w1**2*cos(x1 - x3)*sin(x1) + l1*l2**2*m2**2*w1**2*x4**2*cos(x1 - x3)*sin(x1 - x3) + l1**3*l2*m1*m2*w1*x2**2*sin(x1 - x3) + g*l1**2*l2*m1*m2*w1*cos(x1 - x3)*sin(x1))/(l1*l2**2*m2*(l1**2*m1 + m2*w1**2 - m2*w1**2*cos(x1 - x3)**2)) ,
                    ])
        
        return dxdt