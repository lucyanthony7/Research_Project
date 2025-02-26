import exhaustive_fun
import numpy as np
from scipy.stats import bootstrap

node_sets = [{'A', 'B'}, {'C', 'D'}]
best_nodes, output = exhaustive_fun.evaluate_logic_gates(node_sets)
theta_f_scores = [i[1] for i in output]
print(f"Theta_f scores: {theta_f_scores}")

res = bootstrap((theta_f_scores,), np.mean, confidence_level=0.90, n_resamples=10000)
ci_lower, ci_upper = res.confidence_interval.low, res.confidence_interval.high

print(f"90% CI for mean: [{ci_lower}, {ci_upper}]")