# Code for "Correlated percolation and Ising model on the face-centered cubic lattice: Application to magnetism in doped double perovskites"

This repository contains code written for the paper titled "Correlated percolation and Ising model on the face-centered cubic lattice: Application to magnetism in doped double perovskites". The `percolationmagnet.pdf` file contains the paper. The code performs Monte Carlo simulations on the fcc lattice to find data for percolation, specific heat, and critical temperature, making use of Numpy for vector operations, and the Numba compiler to accelerate computations. The `dfscorrelatedpercolationfcc.py` program finds probability of percolation on the lattice based on doping probability. The `fccmetropolis.py` program calculates values for spin susceptibility, specific heat, and cumulants for the spanning cluster.

### 3D visualization of fcc lattice percolation:
![fccvisualization](https://github.com/Tanmay337442/percolationmagnet/blob/main/fccvisualization.png?raw=true)

Legend:
- Red circles in the graph show the percolating path of osmium (VI) ions
- Blue dots are osmium (VI) ions that are not part of the path
- Green squares represent the remaining calcium ions
- Sodium and osmium (VII) ions are not shown
