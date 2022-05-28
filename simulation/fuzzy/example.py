import time
from classes import NFN, membership,neuron
import numpy as np
import matplotlib.pyplot as plt

start_time = time.time()
def matrix_size(matrix):
    rows = len(matrix)
    columns = len(matrix[0])
    return rows,columns
pn = 1000 #numero de pontos
max_neurons = 4
number_train_inputs = 4
max_membership = 25
xmin = -1
xmax = 8
inputs = 1

#generate the database to follow
x = [[]] * inputs
y = [[]] * inputs
yn = [[]] * inputs
ntw = [[]] * inputs
active_memberships = [[]] * max_neurons
x[0]=(np.linspace(0, 2*np.pi, pn))
y[0]=(np.sin(x[0]))


# for i in range(len(x[0])):
#     y[0].append(x[0][i]**2)

neurons = []

for i in range(max_neurons):
    neurons.append(neuron(max_membership,[xmin,xmax]))
neural_ntw = NFN(neurons)

#train the network
train_input = [[],[],[],[]]
train_output = [[],[],[],[]]

for i in range(pn):
    if i > 20:
        train_input[0].append(x[0][i])
        train_input[1].append(x[0][i-1])
        train_input[2].append(x[0][i-2])
        train_input[3].append(x[0][i-3])
        train_output[0].append(y[0][i])
        train_output[1].append(y[0][i-1])
        train_output[2].append(y[0][i-2])
        train_output[3].append(y[0][i-3])
    else:
        train_input[0].append(x[0][i])
        train_input[1].append(0)
        train_input[2].append(0)
        train_input[3].append(0)
        train_output[0].append(y[0][i])
        train_output[1].append(0)
        train_output[2].append(0)
        train_output[3].append(0)

#shuffle train_inputs and outputs
shuffle_list = np.random.permutation(len(train_input[0]))
train_input_temp = [[],[],[],[]]
train_output_temp = [[],[],[],[]]
for index in shuffle_list:
    train_input_temp[0].append(train_input[0][index])
    train_input_temp[1].append(train_input[1][index])
    train_input_temp[2].append(train_input[2][index])
    train_input_temp[3].append(train_input[3][index])
    train_output_temp[0].append(train_output[0][index])
    train_output_temp[1].append(train_output[1][index])
    train_output_temp[2].append(train_output[2][index])
    train_output_temp[3].append(train_output[3][index])
for i in range(len(train_output)):
    for j in range(len(train_output[0])):
        train_input[i][j] = train_input_temp[i][j]
        train_output[i][j] = train_output_temp[i][j]

yt = [[0]*len(train_input[0]) for i in range(number_train_inputs)]
active_memberships = [[0]*len(train_input[0]) for i in range(number_train_inputs)]
epocas = 1

print("BEFORE TRAIN")
for neuron in neural_ntw.neurons:
    print(neuron.q)

for n in range(epocas):
    #calc alpha and new weights
    #for neuron in neural_ntw.neurons:
        #print(neuron.q)
    for t in range(len(train_input[0])):
        for i in range(len(train_input)):
            neuron = neural_ntw.neurons[i]
            yt[i][t] = neuron.calc(train_input[i][t])
            diff = yt[i][t] - train_output[i][t]
            active_memberships[i][t] = neuron.calc(train_input[i][t],returnSum=False)
            #calc alpha
            den = 0
            for j in range(len(train_input)):
                mbsh_active = (neural_ntw.neurons[j].calc(train_input[j][t],returnSum=False))
                den += sum(list(map(lambda a:a**2, mbsh_active.values())))
            alpha = 1/den
            for membership_index in active_memberships[i][t].keys():
                memberhip_value = active_memberships[i][t].get(membership_index)
                old_membership = neural_ntw.neurons[i].get_q(membership_index)
                new_membership = old_membership - alpha*diff*memberhip_value
                neural_ntw.neurons[i].update_q([membership_index],[new_membership])

print("AFTER TRAIN")

for neuron in neural_ntw.neurons:
    print(neuron.q)

output = [[0]*len(x[0]) for i in range(inputs)]

for i in range(len(x)):
    for t in range(len(x[0])):
        x_input = [x[i][t],0,0,0]
        if t > 4:
            x_input[1] = x[i][t-5]
        if t > 9:
            x_input[2] = x[i][t-10]
        if t > 14:
            x_input[3] = x[i][t-15]
        output[i][t]=(neural_ntw.calc(x_input))/4

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(x[0],y[0])
ax.plot(x[0],output[0])
ax.grid()
print("--- Trainning took %s seconds ---" % (time.time() - start_time))
plt.show()