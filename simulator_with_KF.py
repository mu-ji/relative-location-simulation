'''
Author Manjiang Cao
E-mail mcao999@connect.hkust-gz.edu.cn

This file is relative localization simulator
'''

import numpy as np
import Nodes_class 
import matplotlib.pyplot as plt
import shutil
import os
import random
import simulator_parameters

#Node1 = Nodes_class.RobotNode(1)
#Node2 = Nodes_class.RobotNode(2)
#Node3 = Nodes_class.RobotNode(3)


def clear_figure_buffer():
    """
    清空 figure_buffer 文件夹下的所有文件和文件夹。
    """
    buffer_path = 'figure_buffer'
    
    if os.path.exists(buffer_path):
        shutil.rmtree(buffer_path)
        os.makedirs(buffer_path)
        print(f"已成功清空 {buffer_path} 文件夹。")
    else:
        print(f"{buffer_path} 文件夹不存在。")

clear_figure_buffer()

def compute_MSE(Nodes_list):
    x_error = (Nodes_list[0].true_position - Nodes_list[0].pseudo_position)[0]
    y_error = (Nodes_list[0].true_position - Nodes_list[0].pseudo_position)[1]
    total_error = 0
    for i in Nodes_list:
        error_vector = i.pseudo_error()
        total_error = total_error + np.sqrt((error_vector[0]-x_error)**2 + (error_vector[1]-y_error)**2)
    
    MeanSE = total_error/len(Nodes_list)
    return MeanSE

#the number of nodes
number_of_node = simulator_parameters.nodes_number

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
    locals()[node_name] = Nodes_class.RobotNode(i)
    Nodes_list.append(locals()[node_name])
    error_list.append(locals()[node_name].pseudo_error())

#randomly allocate coomunicable nodes for each node
for i in range(number_of_node):
    Nodes_list_copy = Nodes_list.copy()
    Nodes_list_copy.remove(Nodes_list[i])
    print(Nodes_list_copy)
    communicable_node_list = random.sample(Nodes_list_copy, int(number_of_node*(simulator_parameters.communicable_rate)))
    Nodes_list[i].allocate_communicable_node(communicable_node_list)

error_cov_list.append(np.cov(np.array(error_list).T))

MSE_list.append(compute_MSE(Nodes_list))

plt.figure()
for i in Nodes_list:
    i.draw_pseudo_position()
    i.draw_true_position()

plt.title('start_states')
plt.legend()
plt.grid()
plt.xlim(-200,200)
plt.ylim(-200,200)
plt.savefig('figure_buffer/start_states.png')
plt.show()

steps = 0
while True:
    steps = steps + 1
    error_list = []
    for i in Nodes_list:
        #i.update_pseudo_position()
        i.filter.predict()
        z = i.filter.generate_z_with_communicable_node_list(i.true_position, i.communicable_node_list)
        i.filter.update(z, i.pseudo_position, i.communicable_node_list)

        i.set_pseudo_position([i.filter.x[0][0],i.filter.x[1][0]])

        error_list.append(i.pseudo_error())

    error_cov_list.append(np.cov(np.array(error_list).T))
    #print(np.cov(np.array(error_list).T))

    MSE_list.append(compute_MSE(Nodes_list))
    print(compute_MSE(Nodes_list))
    plt.figure()
    for i in Nodes_list:
        i.draw_pseudo_position()
        i.draw_true_position()
    #plt.legend()
    plt.grid()
    plt.title('step {}'.format(steps))
    plt.xlim(-200,200)
    plt.ylim(-200,200)
    plt.savefig('figure_buffer/step{}.png'.format(steps))
    plt.close()
    
    #plt.show()
    

    if np.cov(np.array(error_list).T)[0][0] <= 1 and np.cov(np.array(error_list).T)[1][1] <= 1:
        x_error = (Nodes_list[0].true_position - Nodes_list[0].pseudo_position)[0]
        y_error = (Nodes_list[0].true_position - Nodes_list[0].pseudo_position)[1]
        break

for i in Nodes_list:
    i.correct_pseudo_position(x_error,y_error)

MSE_list.append(compute_MSE(Nodes_list))

plt.figure()
for i in Nodes_list:
    i.draw_pseudo_position()
    i.draw_true_position()
plt.grid()
plt.xlim(-200,200)
plt.ylim(-200,200)
plt.title('corrected_state')

plt.savefig('figure_buffer/corrected_state.png')
#plt.show()

plt.figure()
plt.plot([i for i in range(steps+2)],MSE_list,label = 'MSE = {}'.format(MSE_list[-1]))
plt.grid()
plt.legend()
plt.xlabel('steps')
plt.ylabel('Mean square error')
plt.savefig('localization_error.png')