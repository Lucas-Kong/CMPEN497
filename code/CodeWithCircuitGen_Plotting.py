#Sample L-6 ion-trap data structure with 15 slots per trap (but keeping 2 open in each initially):
#[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
#[27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39], [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52],
#[53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65], [66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78]]

import random
from collections import Counter
import matplotlib.pyplot as plt

# Generate a circuit based on input parameter j

def generate_circuit(j):
    gates = []  # Initialize the gates list

    # Generate initial gates based on conditions
    for i in range(0, 78, 2):
        gates.append([i, i + 1])  # Add a gate connecting i and i+1

        # Add extra gates based on divisibility conditions
        if i % 5 == 0:
            gates.append([i, i + 1])
        if i % 7 == 0:
            gates.append([i, i + 1])
        if i % 13 == 0:
            gates.append([i, i + 1])
        if i % 2 == 0:
            gates.append([i + 1, i + 2])
        if i % 23 == 0:
            gates.append([i, i + 2])
        if i % 29 == 0:
            gates.append([i, i + 1])
        if i % 41 == 0:
            gates.append([i, i + 1])

    default_len = len(gates)  # Store the default length of the gates list

    # Count occurrences of gates to find "preferred" gates
    tuple_data = [tuple(sorted(sublist)) for sublist in gates]  # Convert gates to tuples for counting
    counter = Counter(tuple_data)  # Count occurrences of each gate

    # Get the 15 most common gates and store them as preferred gates
    top_15 = counter.most_common(15)  # List of tuples [(element, count), ...]
    preferred_gates = [list(element) for element, count in top_15]  # Convert back to lists

    # Generate a pool of random gates, avoiding self-loops
    other_gates_pool = [[random.randint(0, 78), random.randint(0, 78)] for _ in range(10)]
    other_gates_pool = [gate if gate[0] != gate[1] else [gate[0], (gate[1] + 1) % 79] for gate in other_gates_pool]

    # Symmetric (j % 2 == 0) or asymmetric (j % 2 == 1) case
    if j % 2 == 0:  # Symmetric case
        for _ in range(200 - default_len):  # Add additional gates to reach a total of 200 gates
            if random.random() < 0.6:  # 60% chance to pick a preferred gate
                gates.append(random.choice(preferred_gates))
            else:  # 40% chance to pick a less frequent gate
                gates.append(random.choice(other_gates_pool))
        gates = gates * 4  # Repeat the symmetric gates 4 times

    if j % 2 == 1:  # Asymmetric case
        for _ in range(800 - default_len):  # Add additional gates to reach a total of 800 gates
            if random.random() < 0.6:  # 60% chance to pick a preferred gate
                gates.append(random.choice(preferred_gates))
            else:  # 40% chance to pick a less frequent gate
                gates.append(random.choice(other_gates_pool))

    return gates  # Return the generated gates list



'''
def generate_circuit(j):
    # Number of gates
    num_gates = 500

    # Generate a pool of "preferred" gates to increase repetition
    preferred_gates = [
        [0, 1], [1, 2], [3, 4], [2, 3], [4, 5], [28, 9], [35, 76], [42, 69], [17, 12], [9, 6], [32, 14],  [40, 41],
        [26, 23], [7, 45], [8, 19], [5, 17], [4, 59], [10, 11], [12, 13], [14, 15], [16, 17], [18, 19],
        [20, 21], [22, 23], [24, 25], [26, 27], [28, 29], [30, 31], [32, 33], [34, 35], [36, 37], [38, 39]
    ]
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
def generate_circuit(j):
    gates = []

    # Generate gates and apply additional logic based on divisibility
    for i in range(0, 78, 2):
        gates.append([i, i + 1])
        if i % 5 == 0:
            gates.append([i, i + 1])
        if i % 7 == 0:
            gates.append([i, i + 1])
        if i % 13 == 0:
            gates.append([i, i + 1])
        if i % 2 == 0:
            gates.append([i + 1, i + 2])
        if i % 23 == 0:
            gates.append([i, i + 2])
        if i % 29 == 0:
            gates.append([i, i + 3])
        if i % 11 == 0:
            gates.append([i, i + 1])
        if i % 31 == 0:
            gates.append([i, i + 1])
        if i % 17 == 0:
            gates.append([i + 1, i + 2])
        if i % 37 == 0:
            gates.append([i, i + 3])   

    buffer = []

    # Modify gates based on the value of j
    match j:
        case 0:
            buffer = gates[25:75]
            gates.extend(buffer)
            buffer.reverse()
            gates.extend(gates)
        case 1:
            buffer = gates
            gates.extend(gates)
        case 2:
            buffer = gates[:50]
            gates.extend(buffer)
            buffer.reverse()
            gates.extend(gates)
        case 3:
            buffer = gates[:50]
            gates.extend(buffer)
            gates.extend(buffer)
        case 4:
            buffer = gates[50:]
            gates.extend(buffer)
            buffer.reverse()
            gates.extend(gates)
        case 5:
            buffer = gates[50:]
            gates.extend(buffer)
            gates.extend(buffer)
        case 6:
            buffer = gates[25:75]
            gates.extend(buffer)
            buffer.reverse()
            gates.extend(gates)
        case 7:
            buffer = gates
            gates.extend(gates)
        case 8:
            buffer = gates[:50]
            gates.extend(buffer)
            buffer.reverse()
            gates.extend(gates)
        case 9:
            buffer = gates[:50]
            gates.extend(buffer)
            gates.extend(buffer)   

    return gates'''

# Count the number of unique qubits used in the gates
def num_qubits(gates):
    all_qubits = set()
    for gate in gates:
        all_qubits.update(gate)
    return len(all_qubits)

# Calculate the depth of the circuit
def calculate_circuit_depth(gates):
    layers = []
    for gate in gates:
        for layer in layers:
            if not (gate[0] in layer or gate[1] in layer):
                layer.update(gate)
                break
        else:
            layers.append(set(gate))
    return len(layers)

# Allocate qubits to ion traps
def Qubit_allocator(weight_dict):
    ion_map = [[] for _ in range(6)]  # Initialize 6 traps
    while weight_dict:
        max_key = max(weight_dict, key=weight_dict.get)
        max_weight = weight_dict.pop(max_key)
        qa, qb = eval(max_key)

        flaga, flagb = False, False
        index = 0

        for idx, trap in enumerate(ion_map):
            if qa in trap:
                flaga = True
                saved_index_a = idx
            if qb in trap:
                flagb = True
                saved_index_b = idx

        shortest_index = min(range(len(ion_map)), key=lambda i: len(ion_map[i]))

        if not flaga and not flagb:
            ion_map[shortest_index].extend([qa, qb])
        elif flaga and not flagb:
            if len(ion_map[saved_index_a]) < 13:
                ion_map[saved_index_a].append(qb)
            else:
                ion_map[shortest_index].append(qb)
        elif not flaga and flagb:
            if len(ion_map[saved_index_b]) < 13:
                ion_map[saved_index_b].append(qa)
            else:
                ion_map[shortest_index].append(qa)

    return ion_map

# Map qubits using a greedy algorithm
def Greedy_qubit_mapper(usr_input):
    weight_dict = Counter(map(lambda pair: str(pair), usr_input))
    return Qubit_allocator(weight_dict)

# Decaying step function mapper
def Decaying_Step_Function_mapper(usr_input):
    size_of_list = len(usr_input)
    weight_dict = {}
    corresponding_weight = 4
    n = size_of_list // corresponding_weight

    for idx, qubit_pair in enumerate(usr_input):
        if (n + 1 - idx) == 0:
            corresponding_weight -= 1
        key = str(qubit_pair)
        reversed_key = str(qubit_pair[::-1])
        weight_dict[key] = weight_dict.get(key, weight_dict.get(reversed_key, 0)) + corresponding_weight
    return Qubit_allocator(weight_dict)

# Linear decay function mapper
def Linear_Decay_Function_mapper(usr_input):
    a_val = 0.1
    size_of_list = float(len(usr_input))
    weight_dict = {}

    for idx, qubit_pair in enumerate(usr_input):
        weight = size_of_list - (a_val * idx)
        key = str(qubit_pair)
        reversed_key = str(qubit_pair[::-1])
        weight_dict[key] = weight_dict.get(key, weight_dict.get(reversed_key, 0)) + weight
    return Qubit_allocator(weight_dict)

# Exponential decay function mapper
def Exponential_Decay_Function_mapper(usr_input):
    a_val = 2
    size_of_list = len(usr_input)
    weight_dict = {}

    for idx, qubit_pair in enumerate(usr_input):
        weight = size_of_list * (a_val ** -(idx / size_of_list))
        key = str(qubit_pair)
        reversed_key = str(qubit_pair[::-1])
        weight_dict[key] = weight_dict.get(key, weight_dict.get(reversed_key, 0)) + weight
    return Qubit_allocator(weight_dict)

# Penalized decay function mapper
def Penalized_Decay_Function_mapper(usr_input, symmetric, qubit_count, depth):
    size_of_list = len(usr_input)
    weight_dict = {}

    for idx, qubit_pair in enumerate(usr_input):
        weight = size_of_list - ((symmetric * qubit_count * (depth / size_of_list)) * idx)
        key = str(qubit_pair)
        reversed_key = str(qubit_pair[::-1])
        weight_dict[key] = weight_dict.get(key, weight_dict.get(reversed_key, 0)) + weight
    return Qubit_allocator(weight_dict)


 

######################################################################################################################################

#Average count of shuttling operation
def compute_shuttle_count():
    # Initialize lists to store average shuttle operation counts for symmetric and asymmetric cases
    average_list_asym = [0, 0, 0, 0, 0]
    average_list_sym = [0, 0, 0, 0, 0]

    # Perform trials (6 iterations, where `j` determines symmetry)
    for j in range(6):
        # Generate a quantum circuit for the current trial
        usr_input = generate_circuit(j)
        
        # Determine the circuit characteristics
        num_lists = len(usr_input)  # Total gates
        depth = calculate_circuit_depth(usr_input)  # Circuit depth
        qubit_count = num_qubits(usr_input)  # Number of qubits involved

        # Define symmetry based on `j` (even: symmetric, odd: asymmetric)
        sym = j % 2

        # Iterate over the different qubit allocation strategies
        for i, output_map in enumerate([
            Greedy_qubit_mapper(usr_input),
            Decaying_Step_Function_mapper(usr_input),
            Linear_Decay_Function_mapper(usr_input),
            Exponential_Decay_Function_mapper(usr_input),
            Penalized_Decay_Function_mapper(usr_input, sym, qubit_count, depth)
        ]):
            # List of strategy names (used for debugging or display)
            name = ['Greedy', 'Decaying', 'Linear', 'Exponential', 'Penalized']
            shuttle_operations_count = 0  # Count shuttle operations for this strategy

            # Evaluate all gate operations for the current strategy
            for gate in usr_input:
                # Extract qubits for the current gate
                qa, qb = gate
                outer_index_a, outer_index_b = -1, -1  # Indices of traps containing qa and qb

                # Locate the traps containing qa and qb
                for counter, trap in enumerate(output_map):
                    if qa in trap:
                        inner_index_a = trap.index(qa)
                        outer_index_a = counter
                    if qb in trap:
                        inner_index_b = trap.index(qb)
                        outer_index_b = counter

                # Perform shuttle operations if qa and qb are in different traps
                if outer_index_a != outer_index_b:
                    if len(output_map[outer_index_a]) < 15:  # Ensure trap capacity is not exceeded
                        shuttled_qubit = output_map[outer_index_b].pop(inner_index_b)
                        output_map[outer_index_a].append(shuttled_qubit)
                    elif len(output_map[outer_index_b]) < 15:
                        shuttled_qubit = output_map[outer_index_a].pop(inner_index_a)
                        output_map[outer_index_b].append(shuttled_qubit)
                    else:
                        # If both traps are full, find the trap with the fewest qubits
                        shortest_index = min(range(len(output_map)), key=lambda i: len(output_map[i]))
                        shuttled_qubit = output_map[outer_index_a].pop(inner_index_a)
                        output_map[shortest_index].append(shuttled_qubit)
                        shuttled_qubit = output_map[outer_index_b].pop(inner_index_b)
                        output_map[shortest_index].append(shuttled_qubit)

                    # Increment the shuttle operations count
                    shuttle_operations_count += 1

            # Add shuttle operations count to the appropriate list (symmetric or asymmetric)
            if sym == 1:
                average_list_asym[i] += shuttle_operations_count
            else:
                average_list_sym[i] += shuttle_operations_count

    # Calculate average shuttle operation counts for each strategy
    for i in range(5):
        average_list_sym[i] /= 3  # Divide by 3 for the 3 symmetric trials
    for i in range(5):
        average_list_asym[i] /= 3  # Divide by 3 for the 3 asymmetric trials

    return average_list_sym, average_list_asym

def main():
    total_shuttle_sym, total_shuttle_asym = [0,0,0,0,0], [0,0,0,0,0]
    avg_shuttle_sym, avg_shuttle_asym  = [0,0,0,0,0], [0,0,0,0,0]

    num_samples = 5  # Set the number of samples to process

    for i in range(num_samples):  # Loop through the number of samples
        sample_shuttle_sym, sample_shuttle_asym = compute_shuttle_count()  # Compute shuttle counts for a single sample
        for j in range(5):  # Iterate over each index (bin) to update totals
            total_shuttle_sym[j] += sample_shuttle_sym[j]  # Add symmetric shuttle counts to total
            total_shuttle_asym[j] += sample_shuttle_asym[j]  # Add asymmetric shuttle counts to total

    for k in range(5):  # Calculate average shuttle counts for each bin
        avg_shuttle_sym[k] = total_shuttle_sym[k] / num_samples  # Compute average symmetric counts
        avg_shuttle_asym[k] = total_shuttle_asym[k] / num_samples  # Compute average asymmetric counts
        

    name = ['Greedy', 'Decaying', 'Linear', 'Exponential', 'Peanalized']
    # Plot for symmetric shuttle operations
    plt.figure(figsize=(10, 5))
    bars_sym = plt.bar(range(len(avg_shuttle_sym)), avg_shuttle_sym, color='blue', alpha=0.7, label="Symmetric")

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
    plt.xticks(range(len(avg_shuttle_sym)), [f"{name[i]}" for i in range(len(name))])
    plt.show()

    # Plot for asymmetric shuttle operations
    plt.figure(figsize=(10, 5))
    bars_sym = plt.bar(range(len(avg_shuttle_asym)), avg_shuttle_asym, color='green', alpha=0.7, label="Asymmetric")

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
    plt.xticks(range(len(avg_shuttle_asym)), [f"{name[i]}" for i in range(len(name))])
    plt.show()

main()

