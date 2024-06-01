import numpy as np
import simulator_parameters

class KalmanFilter:
    def __init__(self, Q, R, x0):
        """
        初始化Kalman滤波器
        
        参数:
        F (ndarray): 状态转移矩阵
        H (ndarray): 观测矩阵
        Q (ndarray): 过程噪声协方差矩阵
        R (ndarray): 观测噪声协方差矩阵
        x0 (ndarray): 初始状态
        P0 (ndarray): 初始状态协方差矩阵
        """

        self.F = np.array([[1, 0], 
                           [0, 1]])

        self.Q = np.array([[Q, 0],
                            [0, Q]])
        
        self.R = R*np.eye(2*int(simulator_parameters.nodes_number*simulator_parameters.communicable_rate))
        
        self.x = np.array([[x0[0]],
                           [x0[1]]])  # 状态估计
        
        self.P = np.eye(2) # 状态协方差
    
    def generate_H_with_communicable_node_list(self, self_pseudo_position, communicable_node_list):
        n = len(communicable_node_list)
        new_H = np.zeros((2*n,2))
        for i in range(n):
            new_H[2*i][0] = 1
            new_H[2*i][1] = -communicable_node_list[i].pseudo_position[0]/self_pseudo_position[1]
            new_H[2*i+1][0] = -communicable_node_list[i].pseudo_position[1]/self_pseudo_position[0]
            new_H[2*i+1][1] = 1
        self.H = new_H

    def generate_z_with_communicable_node_list(self, self_true_position, communicable_node_list):
        n = len(communicable_node_list)
        new_z = np.zeros((2*n,1))
        for i in range(n):
            new_z[2*i] = self_true_position[0] - communicable_node_list[i].true_position[0]
            new_z[2*i+1] = self_true_position[1] - communicable_node_list[i].true_position[1]
        return new_z
    
    def predict(self):
        """
        状态预测步骤
        """
        self.x = np.dot(self.F, self.x)
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q
        
    def update(self, z, self_pseudo_postion, communicable_node_list):
        """
        状态更新步骤
        
        参数:
        z (ndarray): 观测值
        """
        self.generate_H_with_communicable_node_list(self_pseudo_postion, communicable_node_list)

        y = z - np.dot(self.H, self.x)  # 创新

        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))  # 卡尔曼增益

        self.x = self.x + np.dot(K, y)
        self.P = self.P - np.dot(np.dot(K, self.H), self.P)