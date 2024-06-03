import numpy as np
import matplotlib.pyplot as plt
import simulator_parameters
import KF4single_node

class RobotNode:
    "This class is used to set up the nodes in the simulation"

    def __init__(self,measure_noise_mean, measure_noise_var, node_number):
        self.number = node_number
        self.true_position = np.array([np.random.randint(-50,50), np.random.randint(-50,50)])
        self.pseudo_position = np.array([np.random.randint(-50,50), np.random.randint(-50,50)])
        self.measure_noise_mean = measure_noise_mean
        self.measure_noise_var = measure_noise_var
        # 使用 'tab10' colormap 生成颜色
        num_nodes = simulator_parameters.nodes_number
        if num_nodes <= 10:
            num_nodes = 10
        cmap = plt.cm.get_cmap('tab{}'.format(num_nodes), num_nodes)
        self.color = cmap(np.linspace(0, 1, num_nodes))[node_number-1]
        self.communicable_node_list = []


        self.filter = KF4single_node.KalmanFilter(Q= 0, R= simulator_parameters.measure_noise_var, x0= self.pseudo_position)

    def set_pseudo_position(self, position):
        self.pseudo_position = position

    def measure_distance_and_direction(self,target_node):
        direction = [(target_node.true_position[0] - self.true_position[0] + np.random.normal(self.measure_noise_mean, self.measure_noise_var)), (target_node.true_position[1] - self.true_position[1] + np.random.normal(self.measure_noise_mean,self.measure_noise_var))]
        return direction
    
    def update_pseudo_position(self):
        possibla_pseudo_position_list = []
        for node in self.communicable_node_list:
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

    def allocate_communicable_node(self, communicable_node_list):
        self.communicable_node_list = communicable_node_list

    
