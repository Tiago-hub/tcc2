"""inputs:  matrix x of inputs
            matrix y for training
output: the most parecido com y possible
"""
import numpy as np
import matplotlib.pyplot as plt
import concurrent.futures
from multiprocessing import Process, Manager, Value
from multiprocessing.managers import BaseManager

neural_ntw = None
active_memberships = None
alpha = None
train_input = None
train_output = None
yt = None

def split_list(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def update_membership(neural_ntw, i, t, train):
    neuron = neural_ntw.neurons[i]
    y_sum += neuron.calc(train_input[i][t])
    active_membership = neuron.calc(train_input[i][t],returnSum=False)
    return active_membership

def calc_alpha(neural_ntw, active_memberships, alpha, y_partials, train_input, i, t):

    # global neural_ntw
    # global active_memberships
    # global alpha



    neuron = neural_ntw[0].neurons[i]
    y_partial = neuron.calc(train_input[i][t])
    active_memberships[i][t] = neuron.calc(train_input[i][t],returnSum=False)
    #calc alpha
    den = 0
    for j in range(len(train_input)):
        mbsh_active = (neural_ntw[0].neurons[j].calc(train_input[j][t],returnSum=False))
        den += sum(list(map(lambda a:a**2, mbsh_active.values())))
    alpha_temp = 1/den
    alpha[i] = alpha_temp
    y_partials[i] = y_partial
    #return y_partial

def big_wrapper(time_chunk, index_inputs, neural_ntw, active_memberships, alpha, y_partials, train_input, i):
    for t in time_chunk:
        index_time_alpha = [t] * len(index_inputs)
        procs = [Process(target=calc_alpha, args=(neural_ntw,active_memberships,alpha,y_partials, train_input, i,t)) for i in index_inputs]
        for p in procs: p.start()
        for p in procs: p.join()
        print(t)
        print(y_partials)
def fuzzy(x,y,epocas=1,max_membership=25,return_network=False):
    global neural_ntw
    global active_memberships
    global alpha
    global train_input
    global train_output
    global yt

    from classes import NFN, membership,neuron
    max_neurons = len(x)
    inputs = len(x)
    active_memberships = [[]] * max_neurons
    #define xmax and xmin
    firstFlag = True
    for sample in x:
        if firstFlag:
            xmax = max(sample)
            xmin = min(sample)
            firstFlag = False
        else:
            xmax_temp = max(sample)
            xmin_temp = min(sample)
            if xmax_temp > xmax:
                xmax = xmax_temp
            if xmin_temp < xmin_temp:
                xmin = xmin_temp
        xmax = xmax + 1 #add some space from borders
        xmin = xmin - 1 #add some space from borders

    neurons = []

    for i in range(max_neurons):
        neurons.append(neuron(max_membership,[xmin,xmax]))
    neural_ntw = NFN(neurons)
    #shuffle train_inputs and outputs
    shuffle_list = np.random.permutation(len(x[0]))
    train_input = [[0]*len(x[0]) for i in range(inputs)]
    train_output= [0]*len(y)
    alpha = [0]*len(x)
    for i, _ in enumerate(x):
        j = 0
        for index in shuffle_list:
            train_input[i][j] = x[i][index]
            train_output[j] = y[index]
            j+=1
    yt = [0]*len(y)
    active_memberships = [[0]*len(train_input[0]) for i in range(inputs)]

    # def calc_alpha(i, t):

    #     global neural_ntw
    #     global active_memberships
    #     global alpha



    #     neuron = neural_ntw.neurons[i]
    #     y_partial = neuron.calc(train_input[i][t])
    #     active_memberships[i][t] = neuron.calc(train_input[i][t],returnSum=False)
    #     #calc alpha
    #     den = 0
    #     for j in range(len(train_input)):
    #         mbsh_active = (neural_ntw.neurons[j].calc(train_input[j][t],returnSum=False))
    #         den += sum(list(map(lambda a:a**2, mbsh_active.values())))
    #     alpha_temp = 1/den
    #     alpha[i] = alpha_temp
    #     return y_partial
    
    def update_neuron(i, t):

        global neural_ntw
        global active_memberships
        global alpha
        global train_output
        global yt

        
        diff = yt[t] - train_output[t]
        for membership_index in active_memberships[i][t].keys():
            memberhip_value = active_memberships[i][t].get(membership_index)
            old_membership = neural_ntw.neurons[i].get_q(membership_index)
            new_membership = old_membership - alpha[i]*diff*memberhip_value
            neural_ntw.neurons[i].update_q([membership_index],[new_membership])
    
    def time_calc(t):

            global neural_ntw
            global active_memberships
            global alpha
            global train_output
            global yt
            global train_input
            y_sum = 0
            for i in range(len(train_input)):
                neuron = neural_ntw.neurons[i]
                y_sum += neuron.calc(train_input[i][t])
                active_memberships[i][t] = neuron.calc(train_input[i][t],returnSum=False)
                #calc alpha
                den = 0
                for j in range(len(train_input)):
                    mbsh_active = (neural_ntw.neurons[j].calc(train_input[j][t],returnSum=False))
                    den += sum(list(map(lambda a:a**2, mbsh_active.values())))
                alpha = 1/den
            yt[t] = y_sum
            for i in range(len(train_input)):
                diff = yt[t] - train_output[t]
                for membership_index in active_memberships[i][t].keys():
                    memberhip_value = active_memberships[i][t].get(membership_index)
                    old_membership = neural_ntw.neurons[i].get_q(membership_index)
                    new_membership = old_membership - alpha*diff*memberhip_value
                    neural_ntw.neurons[i].update_q([membership_index],[new_membership])
            # print(neural_ntw.calc([0]))

    for n in range(epocas):

        
        #calc alpha and new weights
        # index_time = range(len(train_input[0]))
        # time_indexes = range(len(train_input[0]))
        # with concurrent.futures.ThreadPoolExecutor(max_workers=512) as executor:
        #     results = executor.map(time_calc,time_indexes)
        #     for result in results:
        #         pass
        #         # print(result)
        # #print(neural_ntw.calc([0]))
        with Manager() as manager:
            original_neural_ntw = neural_ntw
            original_active_memberships = active_memberships
            original_alpha = alpha


            neural_ntw = manager.list([neural_ntw])
            active_memberships = manager.list(active_memberships)
            alpha = manager.list(alpha)
            y_partials = manager.list([0]*(len(train_input)))
            train_input = manager.list(train_input)
            index_inputs = range(len(train_input))
            # index_time_alpha = manager.list([0] * len(index_inputs))
            time_list = list(split_list(range(len(train_input[0])), 100))
            procs = [Process(target=big_wrapper, args=(time_chunk, index_inputs, neural_ntw,active_memberships,alpha,y_partials, train_input, i)) for time_chunk in time_list]
            for p in procs: p.start()
            for p in procs: p.join()
            # for t in range(len(train_input[0])):
            #     y_sum = 0
            #     #alpha = list(range(len(train_input)))
            #     index_time_alpha = [t] * len(index_inputs)
            #     print(t)


            #     # BaseManager.register('NFN', NFN)
            #     # # neural_ntw = manager.NFN(neurons)
            #     # print(neural_ntw)
            #     # exit()
            #     procs = [Process(target=calc_alpha, args=(neural_ntw,active_memberships,alpha,y_partials, train_input, i,t)) for i in index_inputs]

            #     for p in procs: p.start()
            #     for p in procs: p.join()
            #     print(y_partials)
            #     #print(t)
            #     # exit()

            # with concurrent.futures.ThreadPoolExecutor() as executor:
            #     results = executor.map(calc_alpha,index_inputs, index_time_alpha)
            #     for result in results:
            #         y_sum += result

            # yt[t] = y_sum

            # with concurrent.futures.ThreadPoolExecutor() as executor:
            #     results = executor.map(update_neuron,index_inputs,index_time_alpha)
                # for result in results:
                #     pass


    if return_network:
        return neural_ntw
    output = [[0]*len(x[0]) for i in range(1)]

    for t in range(len(x[0])):
        x_input = []
        for i in range(len(x)):
            x_input += [x[i][t]]
        output[0][t]=(neural_ntw.calc(x_input))

    return output[0]


if __name__ == "__main__":
    x = [[0]*(1000) for i in range(4)]
    y = [] * 1000
    x[0]=(np.linspace(0, 2*np.pi, 1000))

    for i in range(len(x[0])):
        if i>5:
            x[1][i] = x[0][i-1]
            x[2][i] = x[0][i-2]
            x[3][i] = x[0][i-3]
        else:
            x[1][i] = 0
            x[2][i] = 0
            x[3][i] = 0

    # for i in range(len(x)):
    #     y[i]=np.sin(x[i])
    y=np.sin(x[0])

    output = fuzzy(x,y,max_membership=30,epocas=5)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x[0],y)
    ax.plot(x[0],output)
    ax.grid()
    plt.show()