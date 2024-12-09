#Sample L-6 ion-trap data structure with 15 slots per trap (but keeping 2 open in each initially):
#[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
#[27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39], [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52],
#[53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65], [66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78]]
import random
from collections import Counter

def generate_circuit(j):
    gates = []
    for i in range(0,78,2):
        gates.append([i, i+1])
        if i%5 == 0:
            gates.append([i,i+1])
        if i%7 == 0: 
            gates.append([i, i+1])
        if i%13 == 0:
            gates.append([i,i+1])
        if i%2 == 0:
            gates.append([i+1,i+2])
        if i%23 == 0:
            gates.append([i, i+2])
        if i%29 == 0:
            gates.append([i, i+1])
        if i%41 == 0:
            gates.append([i,i+1])
    default_len = len(gates)
        # Generate a pool of "preferred" gates to increase repetition
    # Count occurrences
    
    tuple_data = [tuple(sorted(sublist)) for sublist in gates]
        
    counter = Counter(tuple_data)

    # Get the top 20 most common elements
    top_15 = counter.most_common(15)  # Returns a list of tuples [(element, count), ...]

    # Extract only the elements (optional)
    preferred_gates= [list(element) for element, count in top_15]
    other_gates_pool = [[random.randint(0, 78), random.randint(0, 78)] for _ in range(10)]
    other_gates_pool = [gate if gate[0] != gate[1] else [gate[0], (gate[1] + 1) % 79] for gate in other_gates_pool]


    # j % 2 == 0: symmetric, j % 2 == 1: asymmetric

    if j % 2 == 0: # Repeat 4
        for _ in range(200-default_len):
            if random.random() < 0.6:  # 60% chance to pick a preferred gate
                gates.append(random.choice(preferred_gates))
            else:  # 40% chance to pick a less frequent gate
                gates.append(random.choice(other_gates_pool))
        gates = gates * 4
    if j % 2 == 1:
        for _ in range(800-default_len):
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

######################################################################################################################################

#Qubit mapper:
def Qubit_allocator(weight_dict):
    ion_map = [[],[],[],[],[],[]]

    while len(weight_dict) != 0:
        max_key = max(weight_dict, key=weight_dict.get)
        max_weight = weight_dict.pop(max_key)

        max_key = eval(max_key)
        qa = max_key[0]
        qb = max_key[1]
        flaga = False
        flagb = False
        index = 0
        for trap in ion_map:
            if qa in trap:
                flaga = True
                saved_index_a = index
            if qb in trap:
                flagb = True
                saved_index_b = index
            index += 1

        shortest_index = min(range(len(ion_map)), key=lambda i: len(ion_map[i]))
        if (flaga == False) and (flagb == False):
            ion_map[shortest_index].append(qa)
            ion_map[shortest_index].append(qb)
        elif (flaga == True) and (flagb == False):
            if len(ion_map[saved_index_a]) < 13:
                ion_map[saved_index_a].append(qb)
            else:
                ion_map[shortest_index].append(qb)
        elif (flaga == False) and (flagb == True):
            if len(ion_map[saved_index_b]) < 13:
                ion_map[saved_index_b].append(qa)
            else:
                ion_map[shortest_index].append(qa)

    #print("Initial mapping of qubits in L-6 trap system: ", ion_map)
    return(ion_map)

######################################################################################################################################

#Greedy weight allocation algorithm
#Sample input:
#[[0, 1], [4, 5], [2, 3], [3, 5], [4, 2], [0, 1], [1, 2], [0, 1], [1, 2], [0, 1]]
def Greedy_qubit_mapper(usr_input):
    #usr_input = eval(input("Put your 2-qubit interaction matrix: "))
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

    #print("Dictionary of weights for 2-qubit interactions: ", weight_dict)

    return(Qubit_allocator(weight_dict))

######################################################################################################################################

#Decaying Step Function
#Sample input: 
#[[0, 1], [0, 1], [4, 5], [4, 5], [2, 3], [3, 5], [4, 2], [0, 1], [1, 2], [0, 1], [1, 2], [0, 1]]
#Divide into 4
def Decaying_Step_Function_mapper(usr_input):
    #usr_input = eval(input("Put your 2-qubit interaction matrix: "))
    size_of_list = len(usr_input)
    corresponding_weight = 4
    #int(input("How many blocks do you wish to divide your program into? "))
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

    #print("Dictionary of weights for 2-qubit interactions: ", weight_dict)

    return(Qubit_allocator(weight_dict))

######################################################################################################################################

#Linear Decay Function
def Linear_Decay_Function_mapper(usr_input):
    #usr_input = eval(input("Put your 2-qubit interaction matrix: "))
    a_val =0.1
    # float(input("What value do you want to give a? "))
    size_of_list = float(len(usr_input))
    count = 0

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

    #print(weight_dict)

    return(Qubit_allocator(weight_dict))

######################################################################################################################################

#Exponential Decay Function
def Exponential_Decay_Function_mapper(usr_input):
    #usr_input = eval(input("Put your 2-qubit interaction matrix: "))
    a_val = 2
    #float(input("What value do you want to give a? "))
    size_of_list = len(usr_input)
    count = 0

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

    #print(weight_dict)

    return(Qubit_allocator(weight_dict))

######################################################################################################################################

#Penalized Decay Function:
#The edge weight function for this is given by Weight = number_of_gates - (Symmetry_factor * Total_number_of qubits * (Depth/number_of_gates)) * count
#The problem I'm having with this is: what do we consider to be our givens?
#Number of gates is given to us in the user input interaction matrix, but do we simply ask the user if their circuit is symmetric?
#Do we ask the user how many qubits their circuit uses or do we have to deduce it from the user inputted matrix? What about the depth?
#Right now it's being implemented with all of these as 'givens', but idk if this is correct.
def Penalized_Decay_Function_mapper(usr_input, symmetric, qubit_count, depth):
    #usr_input = eval(input("Put your 2-qubit interaction matrix: "))
    #symmetric = int(input("Is your circuit symmetric? 0 if yes, 1 if no: "))
    #qubit_count = int(input("How many qubits are you using? "))
    #depth = int(input("What is the depth of your circuit? "))
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
    
    #print(weight_dict)

    return(Qubit_allocator(weight_dict))

######################################################################################################################################
#Average count of shuttling operation
#asym_performance = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
#sym_performance = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
asym_avg = [0,0,0,0,0]
sym_avg = [0,0,0,0,0]
#5 trial

for j in range(40):
    #These are the actual calls to each function. Just uncomment the one you want to test.
    usr_input = generate_circuit(j)
    #eval(input("Put your 2-qubit interaction matrix: "))
    num_lists = len(usr_input)
    depth = calculate_circuit_depth(usr_input)
    qubit_count = num_qubits(usr_input)
    #output_map = Greedy_qubit_mapper(usr_input)
    #output_map = Decaying_Step_Function_mapper(usr_input)
    #output_map = Linear_Decay_Function_mapper(usr_input)
    #output_map = Exponential_Decay_Function_mapper(usr_input)
    #output_map = Penalized_Decay_Function_mapper(usr_input, 0, qubit_count, depth)

    ######################################################################################################################################

    #usr_input = eval(input("Input your 2-qubit interaction matrix again: "))
    i = 0
    sym = j % 2 
    for output_map in [Greedy_qubit_mapper(usr_input), Decaying_Step_Function_mapper(usr_input),Linear_Decay_Function_mapper(usr_input), Exponential_Decay_Function_mapper(usr_input), Penalized_Decay_Function_mapper(usr_input, sym, qubit_count, depth)]:    
        name = ['Greedy', 'Decaying', 'Linear', 'Exponential', 'Peanalized']
        shuttle_operations_count = 0
        for gate in usr_input:
            #Gets indices of each qubit that pertains to the gate operation we're currently looking at
            qa = gate[0]
            qb = gate[1]
            counter = 0
            for trap in output_map:
                if qa in trap:
                    inner_index_a = trap.index(qa)
                    outer_index_a = counter
                if qb in trap:
                    inner_index_b = trap.index(qb)
                    outer_index_b = counter
                counter += 1

            #Does the actual shuttle operation making sure it doesn't exceed the trap maximum of 15 slots
            if outer_index_a != outer_index_b:
                if len(output_map[outer_index_a]) < 15:
                    shuttled_qubit = output_map[outer_index_b].pop(inner_index_b)
                    output_map[outer_index_a].append(shuttled_qubit)
                elif len(output_map[outer_index_b]) < 15:
                    shuttled_qubit = output_map[outer_index_a].pop(inner_index_a)
                    output_map[outer_index_b].append(shuttled_qubit)
                else:
                    shortest_index = min(range(len(output_map)), key=lambda i: len(output_map[i]))

                    shuttled_qubit = output_map[outer_index_a].pop(inner_index_a)
                    output_map[shortest_index].append(shuttled_qubit)
                    shuttled_qubit = output_map[outer_index_b].pop(inner_index_b)
                    output_map[shortest_index].append(shuttled_qubit)

                shuttle_operations_count += 1
        if j % 2 == 1: #asym
            #idx = j//2
            #asym_performance[idx][i] = shuttle_operations_count
            asym_avg[i] += shuttle_operations_count
        if j % 2 == 0: #sym
            #idx = j//2
            #sym_performance[idx][i] = shuttle_operations_count
        #print(f"Final state of ion-trap map ({name[i]}): ", output_map)
        #print(f"Amount of shuttle operations ({name[i]}): ", shuttle_operations_count)
            sym_avg[i] += shuttle_operations_count
        i += 1

#print(f"asym circuit = {asym_performance}")
#print(f"sym circuit = {sym_performance}")

for i in range(5):
    asym_avg[i] = asym_avg[i]/20
    print(f"Average asymmetric shuttle operation count of {name[i]} = {asym_avg[i]}")
for i in range(5):
    sym_avg[i] = sym_avg[i]/20
    print(f"Average symmetric shuttle operation count of {name[i]} = {sym_avg[i]}")

import matplotlib.pyplot as plt
    # Plot for symmetric shuttle operations
plt.figure(figsize=(10, 5))
bars_sym = plt.bar(range(len(sym_avg)), sym_avg, color='blue', alpha=0.7, label="Symmetric")

# Add value labels above each bar
for bar in bars_sym:
    plt.text(
        bar.get_x() + bar.get_width() / 2,  # X position (center of the bar)
        bar.get_height(),                  # Y position (top of the bar)
        f'{bar.get_height():.3f}',       # Label text (bar height)
        ha='center',                       # Horizontal alignment
        va='bottom'                        # Vertical alignment
    )

plt.title("Average Shuttle Operations - Symetric Circuits")
plt.xlabel("Mapping Heuristic")
plt.ylabel("Average Number of Shuttles")
plt.xticks(range(len(sym_avg)), [f"{name[i]}" for i in range(len(name))])
plt.show()

# Plot for asymmetric shuttle operations
plt.figure(figsize=(10, 5))
bars_sym = plt.bar(range(len(asym_avg)), asym_avg, color='green', alpha=0.7, label="Asymmetric")

# Add value labels above each bar
for bar in bars_sym:
    plt.text(
        bar.get_x() + bar.get_width() / 2,  # X position (center of the bar)
        bar.get_height(),                  # Y position (top of the bar)
        f'{bar.get_height():.3f}',       # Label text (bar height)
        ha='center',                       # Horizontal alignment
        va='bottom'                        # Vertical alignment
    )

plt.title("Average Shuttle Operations - Asymetric Circuits")
plt.xlabel("Mapping Heuristic")
plt.ylabel("Average Number of Shuttles")
plt.xticks(range(len(asym_avg)), [f"{name[i]}" for i in range(len(name))])
plt.show()
    