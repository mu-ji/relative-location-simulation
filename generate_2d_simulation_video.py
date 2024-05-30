import numpy as np
import Nodes_class 
import matplotlib.pyplot as plt
import matplotlib.animation as animation

Node1 = Nodes_class.RobotNode(1)
Node2 = Nodes_class.RobotNode(2)
Node3 = Nodes_class.RobotNode(3)

number_of_node = 10
Nodes_list = []

for i in range(number_of_node):
    node_name = f"Node{i}"
    locals()[node_name] = Nodes_class.RobotNode(i)
    Nodes_list.append(locals()[node_name])


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
    for i in Nodes_list:
        i.update_pseudo_position(Nodes_list)

    plt.figure()
    for i in Nodes_list:
        i.draw_pseudo_position()
        i.draw_true_position()
    plt.legend()
    plt.grid()
    plt.xlim(-200,200)
    plt.ylim(-200,200)
    plt.show()