import matplotlib.pyplot as plt
import numpy as np
import tellurium as te

# model = '''
#     A + B -> C; A*B;
#     C -> B; C;
#     A = 1; B = 1; C = 0;
#     '''

def simulate_bn(model, init_state, n_real=1000, histogram=False, trajectories=False):
        
    r = te.loadAntimonyModel(model)
    rng = np.random.default_rng()

    # boundary of continuous values for 0 and 1
    zeros = np.array([[0, 0.5], [0, 0.5], [0, 0.5]])
    ones = np.array([[0.5, 1], [0.5, 1], [0.5, 1]])
    # specify initial state here
    init_state_integer = init_state[0] * 4 + init_state[1] * 2 + init_state[2]

    # initial conditions
    init_cond = np.empty((n_real, 3))
    for i in range(3):
        if init_state[i] == 1:
            init_cond[:,i] = rng.uniform(low=ones[i,0], high=ones[i,1], size=n_real)
        else:
            init_cond[:,i] = rng.uniform(low=zeros[i,0], high=zeros[i,1], size=n_real)

    n_steps = 40
    t_final = 5
    results = np.empty((n_steps, 4, n_real))
    for j in range(n_real):
        r.A = init_cond[j,0]
        r.B = init_cond[j,1]
        r.C = init_cond[j,2]
        results[:,:,j] = r.simulate(0, t_final, n_steps)

    # convert continuous results to binary
    results_binary = np.zeros((n_steps, 3, n_real), dtype=int)
    for i in range(3):
        results_binary[:,i,:] = (results[:,i+1,:] >= ones[i,0]) * (results[:,i+1,:] <= ones[i,1])

    # convert a binary array to an integer for easy comparison, this is now of shape (n_steps, n_real)
    results_integer = results_binary[:,0,:] * 4 + results_binary[:,1,:] * 2 + results_binary[:,2,:]
    # identify first new state
    first_change = -np.ones(n_real, dtype=int)
    for j in range(n_real):
        t_first_change = np.where(results_integer[:,j] != init_state_integer)[0]
        if len(t_first_change) > 0:
            first_change[j] = results_integer[t_first_change[0],j]
    valid_states = {0:[1,2,4], 1:[0,3,5], 2:[3,0,6], 3:[2,1,7], 4:[5,6,0], 5:[4,7,1], 6:[7,4,2], 7:[6,5,3]}
    valid_changes = []
    for k in range(len(first_change)):
        if first_change[k] in valid_states[init_state_integer]:
            valid_changes.append(first_change[k])
    valid_changes = [x for x in valid_changes if x>=0]

    if histogram==True:
        plt.hist(valid_changes); plt.show()

    if trajectories==True:
        # plot trajectories of simulation
        fig, (ax1, ax2, ax3) = plt.subplots(3)
        for j in range(0, n_real, n_real//50):
            ax1.plot(results[:,0,j], results[:,1,j])
            ax2.plot(results[:,0,j], results[:,2,j])
            ax3.plot(results[:,0,j], results[:,3,j])
        plt.show()

    return valid_changes

model = '''
    A + B -> C; A*B;
    C -> B; C;
    A = 0; B = 1; C = 1;
    '''
n_real = 1000 # number of realisations

initial_conditions = [[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]
transition_probs = np.zeros((8,8), dtype=float)
row_number = 0

for i in initial_conditions: # For estimating the probability of transitioning from state i to state j
    valid_changes = simulate_bn(model, i, n_real)
    n = len(valid_changes)
    state_j_probs = []
    for j in range(8):
        j_count = valid_changes.count(j)
        state_j_probs.append(j_count/n)
    transition_probs[row_number, :] = state_j_probs
    row_number += 1

print(transition_probs)