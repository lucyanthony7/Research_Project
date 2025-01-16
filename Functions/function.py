import tellurium as te
import itertools
import numpy as np
import subprocess
import os
import shutil

def create_bnd(gate_list):

    logic_1 = gate_list[0]
    logic_2 = gate_list[1]

    content = f"""
    node A {{
        rate_up   = 0.0;
        rate_down = C ? C*1.0 : 0.0;
    }}

    node B {{
        rate_up   = 0.0;
        rate_down = D ? D*1.0 : 0.0;
    }}

    node C {{
        rate_up   = A ? A*1.0 : 0.0;
        rate_down = E ? E*1.0 : 0.0;
    }}

    node D {{
        rate_up   = {logic_1} ? ({logic_1})*1.0 : 0.0;
        rate_down = E ? E*1.0 : 0.0;
    }}

    node E {{
        rate_up   = {logic_2} ? ({logic_2})*1.0 : 0.0;
        rate_down = 0.0;
    }}
        """
    with open('model.bnd', 'w') as file:
        file.write(content)


def create_cfg(init_conditions_list):

    content = f"""
    [A].istate = 1.0[{init_conditions_list[0]}], 0.0[{1 - init_conditions_list[0]}];
    [B].istate = 1.0[{init_conditions_list[1]}], 0.0[{1 - init_conditions_list[1]}];
    [C].istate = 1.0[{init_conditions_list[2]}], 0.0[{1 - init_conditions_list[2]}];
    [D].istate = 1.0[{init_conditions_list[3]}], 0.0[{1 - init_conditions_list[3]}];
    [E].istate = 1.0[{init_conditions_list[4]}], 0.0[{1 - init_conditions_list[4]}];

    time_tick = 0.5;
    max_time = 50;
    """

    with open('model.cfg', 'w') as file:
        file.write(content)

    
def run_maboss():

    command = "~/Libraries/MaBoSS-master/tools/MBSS_FormatTable.pl model.bnd model.cfg"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running MaBoSS: {e}")


def read_fixed_point_table(file_name):

    with open(file_name, 'r') as file:
        data = file.read()
        return data
    

def delete_files(file_list, folder_name):
    for file_name in file_list:
        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            print(f"File not found: {file_name}")

    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)
    else:
        print(f"Folder not found: {folder_name}")


def bn_vals_calculator(gate_list, init_conditions_list):

    create_bnd(gate_list)
    create_cfg(init_conditions_list)
    run_maboss()
    data = read_fixed_point_table("model/model_fp.csv")
    
    lines = data.splitlines()
    bn_vals = []

    for line in lines:
        if line.strip() and not line.startswith("FP"):
            columns = line.split()
            probability = columns[1]
            state = columns[-5:]
            bn_vals.append([state, probability])

    del bn_vals[0]

    for i in range(len(bn_vals)):
        for j in range(len(bn_vals[0][0])):
            bn_vals[i][0][j] = int(bn_vals[i][0][j])
            bn_vals[i][1] = float(bn_vals[i][1])

    scaled_list = []
    for i in bn_vals:
        scaler = i[1]
        unscaled_list = i[0]
        scaled_list.append([x*scaler for x in unscaled_list])

    bn_vals = np.sum(scaled_list, axis=0).tolist()

    delete_files(['model.bnd', 'model.cfg'], 'model')

    return bn_vals


def bn_matrix_calculator(gate_list):

    combinations = list(itertools.product([0, 1], repeat=5))
    combinations = [list(comb) for comb in combinations]
    matrix = np.empty((0, 5))

    for init_conditions_list in combinations:
        matrix = np.vstack([matrix, bn_vals_calculator(gate_list, init_conditions_list)])
    
    return matrix


def psn_vals_calculator(init_conditions_list):

    A_init, B_init, C_init, D_init, E_init = init_conditions_list

    model = f'''
    A -> C; A;
    A + B -> D; A + B;
    C -> E; C;
    D -> E; D;
    A = {A_init}; B = {B_init}; C = {C_init}; D = {D_init}; E = {E_init};
    '''

    r = te.loadAntimonyModel(model)
    result = r.simulate(0, 50, 100)

    steady_state = r.steadyState()
    steady_states = r.getFloatingSpeciesConcentrations()
    steady_states = [round(state) for state in steady_states]
    steady_states = [0 if round(state) == 0 else 1 for state in steady_states]

    return steady_states


def psn_matrix_calculator():

    combinations = list(itertools.product([0, 1], repeat=5))
    combinations = [list(comb) for comb in combinations]
    matrix = np.empty((0, 5))

    for init_conditions_list in combinations:
        matrix = np.vstack([matrix, psn_vals_calculator(init_conditions_list)])

    return matrix


def calculate_theta_f(gate_list):

    bn_matrix = bn_matrix_calculator(gate_list)
    psn_matrix = psn_matrix_calculator()

    # The sum of the differences of entries of the matrices, divided by the total number of entries (32x5)

    difference_sum = np.sum(np.abs(bn_matrix - psn_matrix))
    
    return difference_sum/(32*5)


def calculate_theta_s(gate_list):
    # Simply calculate the number of nodes in the gate list and we will scale this by the total number of nodes in the PSN

    letter_count = sum([sum(1 for char in item if char.isalpha()) for item in gate_list])

    return letter_count/5


def calculate_theta(gate_list, alpha):
    return calculate_theta_f(gate_list) + alpha*calculate_theta_s(gate_list)
