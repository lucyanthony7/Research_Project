import function
import itertools

def systematic_logic_gates(node_sets):
    operators = ['&', '|']
    all_logic_gates = []

    for nodes in node_sets:
        node_list = list(nodes)
        logic_expressions = []

        for node in node_list:
            logic_expressions.append(node)

        for node1, node2 in itertools.combinations(node_list, 2):
            for op in operators:
                logic_expressions.append(f"{node1} {op} {node2}")

        for node1, node2, node3 in itertools.permutations(node_list, 3):
            for op1, op2 in itertools.product(operators, repeat=2):
                expr = f"({node1} {op1} {node2}) {op2} {node3}"
                logic_expressions.append(expr)

        logic_expressions = list(set(logic_expressions))
        all_logic_gates.append(logic_expressions)

    return [list(combination) for combination in itertools.product(*all_logic_gates)]


def evaluate_logic_gates(node_sets):
    logic_gate_combinations = systematic_logic_gates(node_sets)
    output = []

    for gate_list in logic_gate_combinations:
        theta_f_score = function.calculate_theta_f(gate_list)
        output.append([gate_list, theta_f_score])

    best_gate_list, best_score = min(output, key=lambda x: x[1])
    return [best_gate_list, best_score]

node_sets = [{'A', 'B'}, {'C', 'D'}]

print(evaluate_logic_gates(node_sets))