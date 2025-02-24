# Appendix

This appendix contains additional details for the research project.

## Functions Folder:

The files in this folder contain the scripts for running the various functions detailed in Section 3 of the project report. We will describe each script in more detail, and explain its purpose in the context of the research project.

### Function.py

[function.py](Functions/function.py) contains the function described in Section 3.7. This purpose of this script is to simulate a Boolean Network based on the example network given in Figure 9, and to compute the values of $\Theta_f$ and $\Theta_s$ for a specified `gate_list`. Thus this script enables us to quantitatively compare the 'performance' of different Boolean Models compared to the given PSN. Note that while this script is written for the example model of Figure 9, it is easily generalisable to other simple protein interaction networks. The script consists of the following functions:

- `create_bnd` and `create_cfg` respectively create the .bnd and .cfg files necessary to construct the MaBoSS Boolean model. If experimenting with other model networks, the networks in these functions must be replaced.
- `run_maboss` then executes the MaBoSS command. The file path must be edited to match the location where you have stored the file.
- 
