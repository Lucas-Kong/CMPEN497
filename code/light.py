import random
from collections import Counter

def generate_circuit():
    # Number of gates
    num_gates = 500

    # Generate a pool of "preferred" gates to increase repetition
    preferred_gates = [[0, 1], [1, 2], [3, 4], [2, 3], [4, 5], [28, 9], [35, 76], [42, 69], [17, 12], [9, 6], [32, 14], [26, 23], [7, 45], [8, 19], [5, 17], [4, 59]]
    other_gates_pool = [[random.randint(0, 78), random.randint(0, 78)] for _ in range(20)]
    other_gates_pool = [gate if gate[0] != gate[1] else [gate[0], (gate[1] + 1) % 79] for gate in other_gates_pool]

    # Create the gates list with some repetition
    gates = []
    for _ in range(num_gates):
        if random.random() < 0.6:  # 60% chance to pick a preferred gate
            gates.append(random.choice(preferred_gates))
        else:  # 40% chance to pick a less frequent gate
            gates.append(random.choice(other_gates_pool))

    return gates

def num_qubits(gates):
    all_qubits = []
    for gate in gates:
        for qubit in gate:
            if qubit not in all_qubits:
                all_qubits.append(qubit)
    return len(all_qubits)

# Calculate circuit depth
def calculate_circuit_depth(gates):
    layers = []
    for gate in gates:
        for layer in layers:
            if all(gate[0] not in layer and gate[1] not in layer for layer in layers):
                layer.update(gate)
                break
        else:
            layers.append(set(gate))
    return len(layers)


def greedy(interaction):
    usr_input = interaction
    weight_dict = {}
    for qubit_pair in usr_input:
        squbit_pair = str(qubit_pair)
        reversed_qubit_pair = str(qubit_pair[::-1])
        
        if squbit_pair in weight_dict:
            weight_dict[squbit_pair] += 1
        elif reversed_qubit_pair in weight_dict:
            weight_dict[reversed_qubit_pair] += 1
        else:
            weight_dict[squbit_pair] = 1
    sorted_dict = dict(sorted(weight_dict.items(), key=lambda item: item[1], reverse=True))

    return sorted_dict
    
def decay_step(interaction, corresponding_weight):
    usr_input = interaction
    size_of_list = len(usr_input)
    n = size_of_list//corresponding_weight

    weight_dict = {}

    groupcount = 1
    for qubit_pair in usr_input:
        if ((n + 1) - groupcount == 0):
            corresponding_weight -= 1
            groupcount = 1

        squbit_pair = str(qubit_pair)
        reversed_qubit_pair = str(qubit_pair[::-1])

        if squbit_pair in weight_dict:
            weight_dict[squbit_pair] += corresponding_weight
        elif reversed_qubit_pair in weight_dict:
            weight_dict[reversed_qubit_pair] += corresponding_weight
        else:
            weight_dict[squbit_pair] = size_of_list

        groupcount += 1

    sorted_dict = dict(sorted(weight_dict.items(), key=lambda item: item[1], reverse=True))

    return sorted_dict
def linear_decay(interaction):
    usr_input = interaction
    size_of_list = float(len(usr_input))
    count = 0
    a_val = 0.1
    weight_dict = {}

    for qubit_pair in usr_input:
        squbit_pair = str(qubit_pair)
        reversed_qubit_pair = str(qubit_pair[::-1])
        
        corresponding_weight = size_of_list - (a_val * count)

        if squbit_pair in weight_dict:
            weight_dict[squbit_pair] += corresponding_weight
        elif reversed_qubit_pair in weight_dict:
            weight_dict[reversed_qubit_pair] += corresponding_weight
        else:
            weight_dict[squbit_pair] = corresponding_weight
        
        count += 1

    sorted_dict = dict(sorted(weight_dict.items(), key=lambda item: item[1], reverse=True))

    return sorted_dict
    
def exp_decay(interaction):
    usr_input = interaction
    size_of_list = float(len(usr_input))
    count = 0
    a_val = 2
    weight_dict = {}

    for qubit_pair in usr_input:
        squbit_pair = str(qubit_pair)
        reversed_qubit_pair = str(qubit_pair[::-1])
        
        corresponding_weight = size_of_list * (a_val**-(count/size_of_list))

        if squbit_pair in weight_dict:
            weight_dict[squbit_pair] += corresponding_weight
        elif reversed_qubit_pair in weight_dict:
            weight_dict[reversed_qubit_pair] += corresponding_weight
        else:
            weight_dict[squbit_pair] = corresponding_weight
        
        count += 1

    sorted_dict = dict(sorted(weight_dict.items(), key=lambda item: item[1], reverse=True))

    return sorted_dict
    
def penalized_decay(interaction, symmetric, qubit_count, depth):
#Penalized Decay Function:
#The edge weight function for this is given by Weight = number_of_gates - (Symmetry_factor * Total_number_of qubits * (Depth/number_of_gates)) * count
#The problem I'm having with this is: what do we consider to be our givens?
#Number of gates is given to us in the user input interaction matrix, but do we simply ask the user if their circuit is symmetric?
#Do we ask the user how many qubits their circuit uses or do we have to deduce it from the user inputted matrix? What about the depth?
#Right now it's being implemented with all of these as 'givens', but idk if this is correct.
    usr_input = interaction
    size_of_list = len(usr_input)
    count = 0

    weight_dict = {}

    for qubit_pair in usr_input:
        squbit_pair = str(qubit_pair)
        reversed_qubit_pair = str(qubit_pair[::-1])
        
        corresponding_weight = size_of_list - ((symmetric * qubit_count * (depth/size_of_list)) * count)

        if squbit_pair in weight_dict:
            weight_dict[squbit_pair] += corresponding_weight
        elif reversed_qubit_pair in weight_dict:
            weight_dict[reversed_qubit_pair] += corresponding_weight
        else:
            weight_dict[squbit_pair] = corresponding_weight
        
        count += 1

    sorted_dict = dict(sorted(weight_dict.items(), key=lambda item: item[1], reverse=True))

    return sorted_dict

#main
gates = generate_circuit()  
    
# Count the number of gates and compute circuit depth
num_lists = len(gates)
circuit_depth = calculate_circuit_depth(gates)
num_qubit = num_qubits(gates)
# Print results
print("Sample gates list:")
print(gates)  # Display the first 10 gates for brevity
print("\nNumber of gates:", num_lists)
print("Circuit depth: ", circuit_depth)
print("Qubit Number: ", num_qubit)
# Analyze gate frequencies for insight
gate_counts = Counter(tuple(sorted(gate)) for gate in gates)
print("\nMost common gates:")
print(gate_counts.most_common(5))


i = 0 # index of name
for _ in [greedy(gates), decay_step(gates, 10), linear_decay(gates), exp_decay(gates), penalized_decay(gates, 0, num_qubit, circuit_depth)]:
    name = ['greedy', 'decay', 'linear', 'exp', 'penalized']
    print(f"Interaction of {name[i]} sorted: {_}")
    i+= 1
    
# 6 ions per group, 1 vacant for shuttling, maximum capacity : 7
trap_num = num_qubit//6
if num_qubit%6 !=0:
    trap_num += 1
print("Number of Traps: ",trap_num)

trap_dict = {}
i = 0
for interactions in [greedy(gates), decay_step(gates, 10), linear_decay(gates), exp_decay(gates), penalized_decay(gates, 0, num_qubit, circuit_depth)]:
    name = ['greedy', 'decay', 'linear', 'exp', 'penalized']
    trap = []
    for _ in range(trap_num):
        trap.append([])
    trap_index = 0
    inside_count = 0
    visited = []
    for interaction in interactions.keys():
        interaction = eval(interaction)
        for element in interaction:
            if element not in visited:
                visited.append(element)
                if inside_count < 6:
                    trap[trap_index].append(element)
                    inside_count += 1
                    if inside_count == 6:
                        trap_index += 1
                        inside_count = 0
                
    print(f"Trap of {name[i]} : {trap}")
    trap_dict[name[i]] = trap
    i+= 1
print(trap_dict)
# Should we shuttle back?
# How to set the size of trap?
# How to set the consistency?

# greedy algorithm trap


from itertools import tee
def is_subsequence(sub, main):
    return set(sub).issubset(set(main))
#print(f"TEST {is_subsequence([1,2], [2,1,3,4,5])}")
for name in ['greedy', 'decay', 'linear', 'exp', 'penalized']:
    current_trap = trap_dict[name]
    #print(current_trap)
    shuttle = 0
    for gate in gates:
        in_same_trap = False
        for trap in current_trap:
            if is_subsequence(gate, trap):
                in_same_trap = True
        if in_same_trap == False:
            element1 = gate[0]
            element2 = gate[1]
            index = 0
            for trap in current_trap:
                if element1 in trap:
                    element1_trap_index = index
                if element2 in trap:
                    element2_trap_index = index
                index += 1
            # LET there is an 6 ions in one trap with capacity 7
            #Shuttling process: if there is additional space just move one ion from one trap to another: no switch
            if len(current_trap[element2_trap_index]) < 7:
                current_trap[element2_trap_index].append(element1)
                current_trap[element1_trap_index].remove(element1)
                shuttle += 1
            elif len(current_trap[element1_trap_index]) < 7:
                current_trap[element1_trap_index].append(element2)
                current_trap[element2_trap_index].remove(element2)
                shuttle += 1
            # If both traps are all in maximum capacity, swap the ions. 
            else:
                current_trap[element2_trap_index].append(element1)
                temp = current_trap[element2_trap_index][-2]
                if temp == element2:
                    temp = current_trap[element2_trap_index][-3]
                current_trap[element1_trap_index].remove(element1)
                current_trap[element1_trap_index].append(temp)
                current_trap[element2_trap_index].remove(temp)
                shuttle += 1
    trap_dict[name] = current_trap
    print(f"Total number of shuttle of {name} is {shuttle}")
print(trap_dict)
