import random
import function

def generate_logic_gates(node_sets):
    operators = ['&', '|']
    max_nodes = 3
    
    logic_gates = []
    
    for nodes in node_sets:
        node_list = list(nodes)
        
        selected_nodes = random.sample(node_list, min(len(node_list), max_nodes))
        
        expression = []
        for i, node in enumerate(selected_nodes):

            if random.random() > 1.0:
                expression.append(f"!{node}")
            else:
                expression.append(node)
            
            if i < len(selected_nodes) - 1:
                expression.append(random.choice(operators))
        
        logic_gates.append(''.join(expression))
    
    print(logic_gates)
    return logic_gates

nodes = [{'A', 'B'}, {'C', 'D'}]

print(function.calculate_theta_f(generate_logic_gates(nodes)))