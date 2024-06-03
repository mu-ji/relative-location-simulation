import numpy as np
import matplotlib.pyplot as plt
import Nodes_class
import random
import os
import shutil

def clear_figure_buffer():
    """
    清空 figure_buffer 文件夹下的所有文件和文件夹。
    """
    buffer_path = 'figure_buffer'
    
    if os.path.exists(buffer_path):
        shutil.rmtree(buffer_path)
        os.makedirs(buffer_path)
        #print(f"已成功清空 {buffer_path} 文件夹。")
    else:
        print(f"{buffer_path} 文件夹不存在。")


def compute_MSE(Nodes_list):
    x_error = (Nodes_list[0].true_position - Nodes_list[0].pseudo_position)[0]
    y_error = (Nodes_list[0].true_position - Nodes_list[0].pseudo_position)[1]
    total_error = 0
    for i in Nodes_list:
        error_vector = i.pseudo_error()
        total_error = total_error + np.sqrt((error_vector[0]-x_error)**2 + (error_vector[1]-y_error)**2)
    
    MeanSE = total_error/len(Nodes_list)
    return MeanSE

def simulator_with_weight_main(measure_noise_mean, measure_noise_var, nodes_number, communicable_rate):
    clear_figure_buffer()
    #the number of nodes
    number_of_node = nodes_number

    #This list used for store all the node
    Nodes_list = []

    #Two list used for store the error vector of each node and error covariance matirx in each step
    error_list = []
    error_cov_list = []

    #Used for store the mean square error in each step
    MSE_list = []

    #set up nodes
    for i in range(number_of_node):
        node_name = f"Node{i}"
        locals()[node_name] = Nodes_class.RobotNode(measure_noise_mean, measure_noise_var, i)
        Nodes_list.append(locals()[node_name])
        error_list.append(locals()[node_name].pseudo_error())

    #randomly allocate coomunicable nodes for each node
    for i in range(number_of_node):
        Nodes_list_copy = Nodes_list.copy()
        Nodes_list_copy.remove(Nodes_list[i])
        #print(Nodes_list_copy)
        communicable_node_list = random.sample(Nodes_list_copy, int(number_of_node*(communicable_rate)))
        Nodes_list[i].allocate_communicable_node(communicable_node_list)

    error_cov_list.append(np.cov(np.array(error_list).T))

    MSE_list.append(compute_MSE(Nodes_list))

    def update_pseudo_position_with_weight(node):
        possible_position_list = []
        possible_position_weight_list = []
        for i in node.communicable_node_list:
            direction_vector = node.measure_distance_and_direction(i)
            possible_position = i.pseudo_position - direction_vector
            possible_position_list.append(possible_position)
            pseudo_direction_vector = i.pseudo_position - node.pseudo_position

            weight = 1/np.linalg.norm(direction_vector - pseudo_direction_vector, ord = 2)
            possible_position_weight_list.append(weight)
        
        possible_position_weight_array = np.array(possible_position_weight_list)/np.array(possible_position_weight_list).sum()
        possible_position_array = np.array(possible_position_list)
        #print(possible_position_weight_array.shape)
        #print(possible_position_array.shape)
        estimate_position = np.dot(possible_position_array.T, possible_position_weight_array)
        node.set_pseudo_position(estimate_position)

    steps = 0
    while steps < 100: # if steps > 100, considering this situation as can't convergent
        steps = steps + 1
        error_list = []
        for i in Nodes_list:

            update_pseudo_position_with_weight(i)
            error_list.append(i.pseudo_error())

        error_cov_list.append(np.cov(np.array(error_list).T))

        MSE_list.append(compute_MSE(Nodes_list))

        if np.cov(np.array(error_list).T)[0][0] <= 1 and np.cov(np.array(error_list).T)[1][1] <= 1:
            break
    
    x_error = (Nodes_list[0].true_position - Nodes_list[0].pseudo_position)[0]
    y_error = (Nodes_list[0].true_position - Nodes_list[0].pseudo_position)[1]
    for i in Nodes_list:
        i.correct_pseudo_position(x_error,y_error)

    MSE_list.append(compute_MSE(Nodes_list))

    return MSE_list[-1], steps

def simulator_2d_main(measure_noise_mean, measure_noise_var, nodes_number, communicable_rate):
    clear_figure_buffer()
    #the number of nodes
    number_of_node = nodes_number

    #This list used for store all the node
    Nodes_list = []

    #Two list used for store the error vector of each node and error covariance matirx in each step
    error_list = []
    error_cov_list = []

    #Used for store the mean square error in each step
    MSE_list = []

    #set up nodes
    for i in range(number_of_node):
        node_name = f"Node{i}"
        locals()[node_name] = Nodes_class.RobotNode(measure_noise_mean, measure_noise_var, i)
        Nodes_list.append(locals()[node_name])
        error_list.append(locals()[node_name].pseudo_error())

    #randomly allocate coomunicable nodes for each node
    for i in range(number_of_node):
        Nodes_list_copy = Nodes_list.copy()
        Nodes_list_copy.remove(Nodes_list[i])
        communicable_node_list = random.sample(Nodes_list_copy, int(number_of_node*(communicable_rate)))
        Nodes_list[i].allocate_communicable_node(communicable_node_list)

    error_cov_list.append(np.cov(np.array(error_list).T))

    MSE_list.append(compute_MSE(Nodes_list))


    steps = 0
    while steps <100:  # if steps > 100, considering this situation as can't convergent
        steps = steps + 1
        error_list = []
        for i in Nodes_list:
            i.update_pseudo_position()
            error_list.append(i.pseudo_error())

        error_cov_list.append(np.cov(np.array(error_list).T))

        MSE_list.append(compute_MSE(Nodes_list))
        
        if np.cov(np.array(error_list).T)[0][0] <= 1 and np.cov(np.array(error_list).T)[1][1] <= 1:
            break
    
    x_error = (Nodes_list[0].true_position - Nodes_list[0].pseudo_position)[0]
    y_error = (Nodes_list[0].true_position - Nodes_list[0].pseudo_position)[1]
    for i in Nodes_list:
        i.correct_pseudo_position(x_error,y_error)

    MSE_list.append(compute_MSE(Nodes_list))

    return MSE_list[-1], steps


#main() begin
'''
measure_noise_list = [0.5, 1, 2, 3, 5, 8, 10]
nodes_number_list = [2, 5, 10, 15, 20]
communicable_rate_list = [0.1, 0.3, 0.5, 0.7, 0.9]

Mse_list = []
steps_list = []

for measure_noise in measure_noise_list:
    for nodes_number in nodes_number_list:
        for communicable_rate in communicable_rate_list:
            Mse_list = []
            steps_list = []
            for i in range(10):
                mse, steps = simulator_with_weight_main(0, measure_noise, nodes_number, communicable_rate)
'''


nodes_number = 20
communicable_rate_list = [0.1, 0.3, 0.5, 0.7, 0.9]
measure_noise_list = [1, 3, 5]
times = 20

MSE_array_with_weight = np.zeros((times,len(communicable_rate_list)))
steps_array_with_weight = np.zeros((times,len(communicable_rate_list)))

MSE_array_2d = np.zeros((times,len(communicable_rate_list)))
steps_array_2d = np.zeros((times,len(communicable_rate_list)))

fig = plt.figure()
for k in range(len(measure_noise_list)):
    for i in range(len(communicable_rate_list)):
        for j in range(times):
            measure_noise = measure_noise_list[k]
            communicable_rate = communicable_rate_list[i]
            mse, steps = simulator_with_weight_main(0, measure_noise, nodes_number, communicable_rate)
            MSE_array_with_weight[j][i] = mse
            steps_array_with_weight[j][i] = steps

            mse, steps = simulator_2d_main(0, measure_noise, nodes_number, communicable_rate)
            MSE_array_2d[j][i] = mse
            steps_array_2d[j][i] = steps

    fig.add_subplot(3,2,2*k+1)
    positions = np.arange(len(communicable_rate_list)) - 0.2
    bp1 = plt.boxplot(MSE_array_with_weight, positions=positions, patch_artist=True, boxprops=dict(facecolor='lightblue', color='black'), widths=0.2)
    positions = np.arange(len(communicable_rate_list)) + 0.2
    bp2 = plt.boxplot(MSE_array_2d, positions=positions, patch_artist=True, boxprops=dict(facecolor='lightgreen', color='black'), widths=0.2)
    plt.title(f'MSE, Noise level: {measure_noise_list[k]}')
    plt.xlabel('communicable rate')
    plt.xticks(np.arange(len(communicable_rate_list)), ['0.1', '0.3', '0.5', '0.7', '0.9'])
    plt.ylabel('MSE error')
    plt.legend([bp1["boxes"][0], bp2["boxes"][0]], ['Weighted', 'Mean'], loc='upper right')
    
    fig.add_subplot(3,2,2*k+2)
    positions = np.arange(len(communicable_rate_list)) - 0.2
    bp1 = plt.boxplot(steps_array_with_weight, positions=positions, patch_artist=True, boxprops=dict(facecolor='lightblue', color='black'), widths=0.2)
    positions = np.arange(len(communicable_rate_list)) + 0.2
    bp2 = plt.boxplot(steps_array_2d, positions=positions, patch_artist=True, boxprops=dict(facecolor='lightgreen', color='black'), widths=0.2)
    plt.title(f'Steps, Noise level: {measure_noise_list[k]}')
    plt.xlabel('communicable rate')
    plt.xticks(np.arange(len(communicable_rate_list)), ['0.1', '0.3', '0.5', '0.7', '0.9'])
    plt.ylabel('total steps to convergent')
    plt.legend([bp1["boxes"][0], bp2["boxes"][0]], ['Weighted', 'Mean'], loc='upper right')

plt.tight_layout()
plt.savefig('simulator_evaluation_result.png')

plt.show()
