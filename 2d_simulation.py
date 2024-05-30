import numpy as np
import Nodes_class 
import matplotlib.pyplot as plt

#Node1 = Nodes_class.RobotNode(1)
#Node2 = Nodes_class.RobotNode(2)
#Node3 = Nodes_class.RobotNode(3)

number_of_node = 10
Nodes_list = []

error_list = []
error_cov_list = []

for i in range(number_of_node):
    node_name = f"Node{i}"
    locals()[node_name] = Nodes_class.RobotNode(i)
    Nodes_list.append(locals()[node_name])
    error_list.append(locals()[node_name].pseudo_error())

error_cov_list.append(np.cov(np.array(error_list).T))

plt.figure()
for i in Nodes_list:
    i.draw_pseudo_position()
    i.draw_true_position()

plt.legend()
plt.grid()
plt.xlim(-200,200)
plt.ylim(-200,200)
plt.show()

while True:
    error_list = []
    for i in Nodes_list:
        i.update_pseudo_position(Nodes_list)
        error_list.append(i.pseudo_error())

    error_cov_list.append(np.cov(np.array(error_list).T))
    print(np.cov(np.array(error_list).T))

    plt.figure()
    for i in Nodes_list:
        i.draw_pseudo_position()
        i.draw_true_position()
    #plt.legend()
    plt.grid()
    #plt.xlim(-200,200)
    #plt.ylim(-200,200)
    plt.savefig('relative localization.png')
    #plt.show()
    

    if np.cov(np.array(error_list).T)[0][0] <= 1 and np.cov(np.array(error_list).T)[1][1] <= 1:
        x_error = (Nodes_list[0].true_position - Nodes_list[0].pseudo_position)[0]
        y_error = (Nodes_list[0].true_position - Nodes_list[0].pseudo_position)[1]
        break

for i in Nodes_list:
    i.correct_pseudo_position(x_error,y_error)

plt.figure()
for i in Nodes_list:
    i.draw_pseudo_position()
    i.draw_true_position()
plt.grid()
plt.savefig('relative localization corrected.png')
plt.show()
