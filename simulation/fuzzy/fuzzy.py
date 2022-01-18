"""inputs:  matrix x of inputs
            matrix y for training
output: the most parecido com y possible
"""
import numpy as np
import matplotlib.pyplot as plt

def fuzzy(x,y,epocas=1,max_membership=25,return_network=False):
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
    for i, _ in enumerate(x):
        j = 0
        for index in shuffle_list:
            train_input[i][j] = x[i][index]
            train_output[j] = y[index]
            j+=1
    yt = [0]*len(y)
    active_memberships = [[0]*len(train_input[0]) for i in range(inputs)]

    for n in range(epocas):
        #calc alpha and new weights
        for t in range(len(train_input[0])):
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