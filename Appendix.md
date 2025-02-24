# Appendix

This appendix contains additional details for the research project.

## Functions Folder:

The files in this folder contain the scripts for running the various functions detailed in Sections 3 and 4 of the project report. We will describe each script in more detail, and explain its purpose in the context of the research project. The files described in this appendix are the following:

- [function.py](#functionpy)
- [rand_function.py](#rand_functionpy)
- [exhaustive_fun.py](#systematic_funpy)

### function.py

[function.py](Functions/function.py) contains the function described in Section 3.7. This purpose of this script is to simulate a Boolean Network based on the example network given in Figure 9, and to compute the values of $\Theta_f$ and $\Theta_s$ for a specified `gate_list`. Thus this script enables us to quantitatively compare the 'performance' of different Boolean Models compared to the given PSN. Note that while this script is written for the example model of Figure 9, it is easily generalisable to other simple protein interaction networks. The script consists of the following functions:

- `create_bnd` and `create_cfg` respectively create the .bnd and .cfg files necessary to construct the MaBoSS Boolean model. If experimenting with other model networks, the networks in these functions must be replaced. Note that `create_bnd` takes as input the list `gate_list` which contains the logic gates which are to be tested, for example ['A|B','C&D']. `create_bnd` takes as input the list of initial conditions for each node, for example [0,0,1,1].
- `run_maboss` then executes the MaBoSS command. The file path must be edited to match the location where you have stored the file.
- `read_fixed_point_table` and `delete_files` respectively read the information generated from the MaBoSS simulation in the fixed point table, and then delete the files created for the Boolean simulation.
- `bn_vals_calculator` takes as inputs the lists of gates and initial conditions and executes the functions previously described. It returns the steady states generated from the MaBoSS simulation as a list of 0s and 1s corresponding to the steady state of each node in the system. Then the function `bn_matrix_calculator` calls the function `bn_vals_calculator` for every set of initial conditions and creates a matrix where each entry is the eventual state of each node, for every initial condition. 
- The functions `psn_vals_calculator` and `psn_matrix_calculator` compute the same matrix for the PSN, so that we obtain two matrices of identical dimensions.
- Finally, `calculate_theta_f`, `calculate_theta_s` and `calculate_theta` use the two matrices described above to compare the steady states of the BN, with those from the PSN, for all initial conditions. Thus $\Theta_f$ penalises large differences between the steady states generated, while $\Theta_s$ simply penalises the size of the model to avoid overfitting.

### rand_function.py

[rand_function.py](Functions/rand_function.py) is described in section 4.1 of the project report and utilises the functions described in `function.py` to test randomly generated combinations of logic gates. The script contains the following function:

- `generate_logic_gates` inputs a set of nodes and randomly combines AND and OR operators to create a logic gate of maximum length 3. The function also contains a clause to include the NOT operator with a given probability, however for this example we have set this probability to 0. The script then uses `calculate_theta_f` to combute the $\Theta_f$ value for the randomly generated logic gate.

### exhaustive_fun.py

[exhaustive_fun.py](Functions/exhaustive_fun.py) is detailed in section 4.2 of the project report and works similarly to `random_function.py`, but instead it checks through all logically distinct logic gates exhaustively. It contains the following functions:

- `exhaustive_logic_gates` inputs a set of nodes and outputs a list of all logically distinct combinations of logic gates of maximum length 3.
- `evaluate_logic_gates` simply evaluates the $\Theta_f$ value of each of these logic gates and outputs the logic gate with the optimal score, along with this optimal score and the list of all the logic gates and their respective scores.
