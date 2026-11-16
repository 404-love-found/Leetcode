#Artificial Neural Networks - Forward Propagation

import numpy as np

def initialize_network(num_inputs, num_hidden_layers, num_nodes_hidden, num_nodes_output):
    num_nodes_previous = num_inputs
    network = {}

    for layer in range(num_hidden_layers + 1):
        if layer == num_hidden_layers:
            num_nodes = num_nodes_output
            layer_name = f'output_layer'
        else:
            layer_name = 'layer_{}'.format(layer + 1)
            num_nodes = num_nodes_hidden[layer]

        network[layer_name] = {}
        for node in range(num_nodes):
            node_name = 'node_{}'.format(node+1)
            network[layer_name][node_name] = {
                'weights': np.around(np.random.uniform(size=num_nodes_previous),decimals=2),    
                'bias': np.around(np.random.uniform(size=1),decimals=2)
            }
        num_nodes_previous = num_nodes
    return network

#calculate the weighted sum of inputs and weights, and add the bias
def compute_weighted_sum(inputs, weights, bias):
    return np.sum(inputs * weights) + bias

#use the sigmoid activation function to calculate the output of a node
def node_activation(weighted_sum):
    return 1.0 / (1.0 + np.exp(-weighted_sum))

#perform forward propagation through the network
def forward_propagation(network, inputs):
    layer_inputs = list(inputs)
    for layer in network:
        layer_output = []
        for node_data in network[layer].values():
            

