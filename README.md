# Quantum genome sequence reconstruction
Genome sequence reconstruction is a process of reconstructing a complete genome on a collection of smaller DNA or RNA fragments. The overlap-layout-consensus(OLC) is a popular method for genome sequence reconstruction and can be seen as TSP, where the goal is to find the shortest path that visits each node exactly once. 


## Graph of genome sequence
* Nodes
  Each node presents a DNA or RNA fragment(a read). It can be obtained from sequencing technologies, such as Illumina.  
* Edges
  An edge presents the overlap between two nodes. The weight of the edge is the negative of the length of the overlap between two fragments. It is calculated by suffixes and prefixes of two sequences to identify common regions. The larger the overlap, the stronger the connection.

## Method
* OLC: construct a graph of overlapping fragments, determine the optimal layout, and reconstruct the consensus sequence.
* Hamiltonian path: the graph is visualized as a problem of finding a Hamiltonian path, where the goal is to find a path through all nodes with the maximum overlap between consecutive nodes.
* TSP: genome sequence reconstruction can be seen as TSP.

## VQE
A Hamiltonian was constructed for the genome sequence reconstruction. Then VQE on Qiskit was utilized for genome sequence reconstruction. 
