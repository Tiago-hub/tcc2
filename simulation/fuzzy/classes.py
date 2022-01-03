class triangular:
    def __init__(self, _min, modal, _max):
        self.min = _min
        self.max = _max
        self.modal = modal

    def __call__(self, x):
        #try:
        if self.min is None:
            if x > self.modal and x < self.max:
                y = (self.max-x)/(self.max-self.modal)
            else:
                y = 0
        elif self.max is None:
            if x > self.min and x < self.modal:
                y = (x-self.min)/(self.modal-self.min)
            else:
                y = 0
        elif x < self.min or x > self.max:
            y = 0
        else:
            if x < self.modal:
                if self.min is not None:
                    y = (x-self.min)/(self.modal-self.min)
                else:
                    y = 0
            elif x > self.modal:
                if self.max is not None:
                    y = (self.max-x)/(self.max-self.modal)
                else:
                    y = 0
            else:
                y = self.modal
        #except:
        #    y = 0
        return y


class membership:
    """"Membership class is a class that handles the creation and calculation of multiple 
        triangular functions between a range of values on x axis
        - Initial parameters:
            xmin -> minimum value the memberships functions receive
            xmax -> maximum value the memberships functions receive
            m -> number of memberships functions to generate between xmin and xmax
        - Important atributes:
            A -> list of membership functions
            q -> list of respective weight to multiply each membership output"""

    def __init__(self, xmin, xmax, m,q=None):
        self.xmin = xmin
        self.xmam = xmax
        self.m = m
        self.delta_i = (xmax-xmin)/(m-1)
        self.A = []
        self.modals = []
        if q is None:
            self.q = [1]*m
        elif q:
            self.q = q
        for i in range(m):
            b = self.xmin + (i)*self.delta_i #the formula is (i-1), but assumes i begins at 1
            self.modals.append(b)
        for i, modal in enumerate(self.modals):
            if i == 0:
                a = None
                b = self.modals[i]
                c = self.modals[i+1]
            elif i == (m-1):
                a = self.modals[i-1]
                b = self.modals[i]
                c = None
            else:
                a = self.modals[i-1]
                b = self.modals[i]
                c = self.modals[i+1]
            self.A.append(triangular(a, b, c))

    def get_active_membership(self,x):
        r = {}
        for i,A in enumerate(self.A):
            mbsh_result =  A(x)
            if mbsh_result > 0:
                r[i] = mbsh_result
        return r
    
    def calc_memberships(self, x):
        r = []
        for i, A in enumerate(self.A):
            r.append(A(x)*self.q[i])
        return r

    def sum_of_memberships(self, x):
        r = sum(self.calc_memberships(x))
        return r


class neuron:
    def __init__(self, mbs_number=3, mbs_limits=[-10, 10],q=None):
        try:
            if len(q)!=mbs_number and q!=None:
                raise TypeError
        except TypeError:
            print("Membership number must be equal to q list length. Each membership has it own costant to multiply")
            exit(1)
        self.membership_number = mbs_number
        if q is None:
            self.q = [1]*mbs_number
        elif q:
            self.q = q
        self.memberships = membership(
            xmin=mbs_limits[0], xmax=mbs_limits[1], m=mbs_number, q=q)

    def calc(self,x):
        mbsh_results = self.memberships.get_active_membership(x)
        r = 0
        for mbsh in mbsh_results:
            r   += mbsh_results[mbsh] * self.q[mbsh]
        return r

    def update_q(self,indexes,values):
        for i,index in enumerate(indexes):
            self.q[index] = values[i]

class NFN:
    """"receives a list of neurons"""
    def __init__(self, neurons):
        self.neurons = neurons
    def calc(self):
        r = 0
        for neuron in self.neurons:
            r += neuron.calc()
        return r

neuron = neuron(q=[1,1,1])
print(neuron.calc(5))