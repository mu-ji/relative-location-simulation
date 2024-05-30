import numpy as np
import matplotlib.pyplot as plt

class RobotNode:
    "This class is used to set up the nodes in the simulation"

    def __init__(self,node_number):
        self.number = node_number
        self.true_position = np.array([np.random.randint(0,100), np.random.randint(0,100)])
        self.pseudo_position = np.array([np.random.randint(0,100), np.random.randint(0,100)])
        self.measure_noise_mean = 0
        self.measure_noise_var = 5
        # 使用 'tab10' colormap 生成颜色
        num_nodes = 10
        cmap = plt.cm.get_cmap('tab10', num_nodes)
        self.color = cmap(np.linspace(0, 1, num_nodes))[node_number-1]

        
    def measure_distance_and_direction(self,target_node):
        direction = [(target_node.true_position[0] - self.true_position[0] + np.random.normal(self.measure_noise_mean, self.measure_noise_var)), (target_node.true_position[1] - self.true_position[1] + np.random.normal(self.measure_noise_mean,self.measure_noise_var))]
        return direction
    
    def update_pseudo_position(self,target_nodes):
        possibla_pseudo_position_list = []
        for node in target_nodes:
            if node == self:
                continue
            else:
                direction = self.measure_distance_and_direction(node)
                possibla_pseudo_position_list.append(node.pseudo_position - direction)
        
        self.pseudo_position = np.mean(np.stack(possibla_pseudo_position_list, axis=0), axis=0)


    def draw_pseudo_position(self):
        plt.scatter(self.pseudo_position[0], self.pseudo_position[1],c = self.color, marker = 'o', label = 'Node{} pseudo position'.format(self.number))

    def draw_true_position(self):
        plt.scatter(self.true_position[0], self.true_position[1],c = self.color, marker = '+', label = 'Node{} true position'.format(self.number))

    def pseudo_error(self):
        error_vector = self.true_position - self.pseudo_position
        return error_vector
    
    def correct_pseudo_position(self,x_error,y_error):
        self.pseudo_position[0] = self.pseudo_position[0] + x_error
        self.pseudo_position[1] = self.pseudo_position[1] + y_error
