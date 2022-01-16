import numpy as np
from sympy import Matrix

g = 9.8
class double_pendulum:

    def __init__(self, m1, m2, l1, l2, w1, w2, q1=0, q2=0, b1=0, b2=0, a1=0, a2=0):
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
        self.Gen2Cart(self.q1, self.q2, self.w1, self.w2)

    def Gen2Cart(self, q1, q2, w1, w2):
        self.x1 = self.w1 * np.sin(self.q1)
        self.x2 = self.x1 + self.w2 * np.sin(self.q2)
        self.y1 = -self.w1 * np.cos(self.q1)
        self.y2 = self.y1 + -1*self.w2*np.cos(self.q2)
        return (self.x1, self.y1, self.x2, self.y2)

    def linear_system(self):
        a = self.m1*self.l1**2 + self.m2*self.w1**2
        b = self.m2*self.w1*self.l2
        c = self.m1*g*self.l1 + self.m2*g*self.w1
        d = self.m2*self.w1*self.l2
        e = self.m2*self.l2**2
        f = self.m2*g*self.l2
        A = Matrix([[a,b,self.b1**2,self.b1*self.b2,c,0],[d,e,self.b2**2,self.b1*self.b2,0,f],[0,0,0,0,0,0],[0,0,0,0,0,0]])
        B = Matrix([[self.a1],[self.a2],[0],[0]])
        sol, params = A.gauss_jordan_solve(B)
        return [sol,params]

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

    def dxdt(self,t,y0=None):
        if y0 is not None:
            [self.q1_, self.q1, self.q2_, self.q2, self.a1, self.a2] = y0
        """
        returns: a list containing every variable derivate
            q1__ -> acceleration of q1
            q1_ -> velocity of q1
            q2__ -> acceleration of q2
            q2_ -> velocity of q2
            a1 -> angular acceleration imposed to q1 by actuator
            a2 -> angular acceleration imposed to q2 by actuator
        """
        sol, params = self.linear_system()
        initial_taus = [self.q1_,self.q2_,self.q1,self.q2]
        taus_zeroes = {}
        for i,tau in enumerate(params):
            taus_zeroes[tau] = initial_taus[i]
        sol_unique = sol.xreplace(taus_zeroes)
        self.q1__ = sol_unique[0]
        self.q2__ = sol_unique[1]
        self.q1_ = sol_unique[2]
        self.q2_ = sol_unique[3]
        self.q1 = sol_unique[4]
        self.q2 = sol_unique[5]
        return([self.q1__,self.q1_,self.q2__,self.q2_,self.a1,self.a2])

    def dpend_dt(self,t, x):
        a, b, g, d, e, z, n, th = [self.m1*self.l1**2+self.m2*self.w1**2, self.w1*self.l2,
                                   self.w1*self.l2, self.m1*self.l1*self.g+self.m2*self.w1*self.g, self.m2*self.l2**2, self.w1*self.l2, self.w1*self.l2, self.m2*self.l2*self.g]
        x1, x2, x3, x4, tal1, tal2 = x
        dxdt = np.array([   x2,
                            (-1/(a-((b*z)/e)*np.cos(x1-x3)**2))*((b/e)*x2**2*np.sin(x1-x3)*np.cos(x1-x3)-((b*th)/e)*np.cos(x1-x3)*np.sin(x3)+g*x4**2*np.sin(x1-x3)+d*np.sin(x1)) + tal1 - 0.15*0.5*x2*x2,
                            x4,
                            (1/(e-((b*z/a)*np.cos(x1-x3)**2)))*(((g*z)/a)*x4**2*np.cos(x1-x3)*np.sin(x1-x3)+(((d*z)/a)*np.sin(x1)*np.cos(x1-x3)+n*x2**2*np.sin(x1-x3)-th*np.sin(x3))) + tal2 - 0.15*0.5*x4*x4,
                            tal1,
                            tal2])
        return dxdt
