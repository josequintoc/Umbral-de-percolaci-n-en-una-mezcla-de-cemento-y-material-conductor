# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 17:09:07 2024

@author: user
"""

import numpy as np
import random
from scipy.ndimage import label
n=18
depth, rows, cols =n, n, n

np.random.seed(0)
matrix = np.random.choice([0, 1], size=(depth, rows, cols), p=[0.81, 0.19])

def move_cluster_3d(cluster, depth, rows, cols):
    dx, dy, dz = random.choice([-1, 0, 1]), random.choice([-1, 0, 1]), random.choice([-1, 0, 1])
    new_cluster = []
    for (z, x, y) in cluster:
        new_z, new_x, new_y = z + dz, x + dx, y + dy
        
        if 0 <= new_z < depth and 0 <= new_x < rows and 0 <= new_y < cols:
            new_cluster.append((new_z, new_x, new_y))
        else:
            new_cluster.append((z, x, y))
    return new_cluster

def update_matrix_3d(matrix, clusters):
    new_matrix = np.zeros(matrix.shape)
    for cluster in clusters:
        for point in cluster:
            new_matrix[point] = 1
    return new_matrix

def save_to_xyz(matrix, iteration):
    points = np.argwhere(matrix == 1)
    with open(f'output_{iteration}.xyz', 'w') as f:
        f.write(f"{len(points)}\n")
        f.write(f"Iteration {iteration}\n")
        for point in points:
            f.write(f"1 {point[0]} {point[1]} {point[2]}\n")


iterations = 10

for i in range(iterations):

    labeled_matrix, num_features = label(matrix)
    
    clusters = []
    for feature in range(1, num_features + 1):
        cluster = list(zip(*np.where(labeled_matrix == feature)))
        clusters.append(cluster)

    
    new_clusters = [move_cluster_3d(cluster, depth, rows, cols) for cluster in clusters]

    
    matrix = update_matrix_3d(matrix, new_clusters)
    
    
    save_to_xyz(matrix, i)

def is_connected_central(matrix):
    visited = np.zeros_like(matrix, dtype=bool)
    def dfs(i, j, k):
        if not (4 <= i < n-4 and 4 <= j < n-4 and 4 <= k < n-4):
            return False
        if visited[i, j, k] or matrix[i, j, k] != 1:
            return False
        visited[i, j, k] = True
        if i == n-5:  
            return True
        
        return (dfs(i-1, j, k) or dfs(i+1, j, k) or dfs(i, j-1, k) or
                dfs(i, j+1, k) or dfs(i, j, k-1) or dfs(i, j, k+1))

    
    for j in range(4, n-4):
        for k in range(4, n-4):
            if matrix[4, j, k] == 1 and dfs(4, j, k):
                return True
    return False

connected = is_connected_central(matrix)
print("¿El material es conductor?", connected)
