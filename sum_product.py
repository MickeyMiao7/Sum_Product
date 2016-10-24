#!/usr/bin/env python

import numpy

__author__ = "MIAO QI"
__matricNo__ = "A0159327X"
__email__ = "E0046706@u.nus.edu"
__github__ = "git@Mickey.Miao7/"


"""
Python  Version : Python 2.7
Package Included: numpy


=======================================================================

The program realizes the sum-product algorithm in the tree.
The algorithm uses the equations in the slide of Page 33, lecture 6.  

Actually, this algorithm can be realized by belief propagation in factor
graph as well, but it is not illustrated here.

=======================================================================

In this case, Node 1,2,3 share the same potential as potential1
Node 2,4,6 share the same potential as potential2
All the edge share the same potental as edgePotential

But these can all be replaced by arbitary potential array for more 
generalize situation.


"""
potential1 = numpy.array([0.7, 0.3])
potential2 = numpy.array([0.1, 0.9])
edgePotential = numpy.array([[1, 0.5], [0.5,1]])

# The iteration times is not fixed.
# You need to enlarge this value as the tree becomes more complex until
# the value of each message not changed any more
iterationTimes = 10

class Node():
    """
    For each node, the initialization needs three parameters:
    index    :  id
    neighbors:  ids of all adjacent nodes
    potential:  array of potential

    """
    def __init__(self, index, neighbors, potential):
        self.index = index
        self.neighbors = [i for i in neighbors]
        self.potential = potential
        self.dimension = numpy.shape(self.potential)[0]
       
        # The dict reserving the info of the message propogated from neighbor nodes.
        # The key is the id of neibornode. The value is the value(array) of message.
        self.msgIn = {}                                                      
        
        # The dict reserving the info of the message propogated towards neighbor nodes.
        # The key is the id of neibornode. The value is the value(array) of message.
        self.msgOut = {}


    def calculateMarginal(self):
        # After all messages not changed, calculate marginalization
        # The equation is: 
        # Marginal(Xi) = (1 / Z) The sum Xi of (Product of all incoming messages)  
        # Z means normalization factor, represented by total
        total = 0
        dimensions = []
        for i in range(self.dimension):
            product = 1
            for array in self.msgIn.values():
                product = array[i] * product
            dimensions.append(product * self.potential[i])
        for i in dimensions:
            total = total + i
        return numpy.array([x / total for x in dimensions])


class Tree():
    """
    The initialization of the tree needs the list containing all nodes

    """
    def __init__(self, nodes):
        # For each node, initilize all the messages value to array of [1,1] (For node of two dimensions)
        self.nodes = dict([(node.index, node) for node in nodes])
        for node in self.nodes.values():
            node.msgIn = dict([(j, numpy.array([1] * node.dimension)) for j in node.neighbors])
            node.msgOut = dict([(j, numpy.array([1] * node.dimension)) for j in node.neighbors])
    

    # Each propagation contains two steps:
    # Compute messages out and messages in
    # It will repeat for (iterationTimes) times
    def propagation(self, iterationTimes):
        for i in xrange(iterationTimes):
            self.sendMsg()
            self.recvMsg()


    # Compute the messeges propogated towards neighbors for each node in tree
    # The equation here is:
    # Message(from Xj to Xi) = The sum Xi of [ Potential of edge * Product(all the message from Xk to Xj)]  
    # Xk is Xj's neighbor node except Xi

    # Actually, the message out is computed using message in iterated from previous turn
    def sendMsg(self):
        for node in self.nodes.values():
            for j in node.neighbors:
                # Initilization array([0, 0]) (For node of two dimensions)
                value = numpy.array([0] * node.dimension) 
                for i in range(0, node.dimension):
                    tmp = [node.msgIn[k][i] for k in node.neighbors if k != j]
                    # If tmp is empty list, the numpy.prod(tmp) will be 1,
                    # else, it will be the product of all the message from Xk to Xj(Xk is Xj's neighbor except Xi)
                    value = node.potential[i] * edgePotential[i] * numpy.prod(tmp) + value
                node.msgOut[j] = value 


    # The message in of Xi received from Xj = message sent out from Xj to Xi
    def recvMsg(self):
        for index, node in self.nodes.items():
            for i in node.neighbors:
                node.msgIn[i] = self.nodes[i].msgOut[index]


def main():
    # Construct the nodes, and then they form the tree
    x1 = Node(1, [2, 3], potential1)
    x2 = Node(2, [1, 4, 5], potential2)
    x3 = Node(3, [1, 6], potential1)
    x4 = Node(4, [2], potential2)
    x5 = Node(5, [2], potential1)
    x6 = Node(6, [3], potential2)
    tree = Tree([x1, x2, x3, x4, x5, x6])

    # The messages propagete for (iterationTimes) times
    tree.propagation(iterationTimes)

    for index, node in tree.nodes.items():
        print "The potential of Node %d is: " % index
        print node.calculateMarginal()
        print " "


if __name__ == "__main__":
    main()
