import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

INF = float('inf')
random.seed(0x2024)
GRAPH_STRUCURE = [
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
]
GRAPH = [[INF if not val else val for val in row] for row in GRAPH_STRUCURE]
GOAL = 0x3200
INITIAL_HEALTH = 128

def is_valid(v, pos, path, graph):
    if graph[path[pos - 1]][v] == 0:
        return False

    if v in path:
        return False
    return True

def hamiltonian_circuit(graph, path, pos, circuits):
    if pos == len(graph):
        if graph[path[pos - 1]][path[0]] == 1:
            temp = path.copy()
            temp.append(0)
            if temp[::-1] not in circuits:
                circuits.append(temp)
            return 1
        else:
            return 0

    for v in range(1, len(graph)):
        if is_valid(v, pos, path, graph):
            path[pos] = v
            hamiltonian_circuit(graph, path, pos + 1, circuits)
            path[pos] = -1

def get_hamiltonian_circuits(graph):
    circuits = []
    
    path = [-1] * len(graph)
    path[0] = 0
    hamiltonian_circuit(graph, path, 1, circuits)

    return circuits

circuits = get_hamiltonian_circuits(GRAPH_STRUCURE)

def generate_graph(val, graph):
    for i in range(16):
        if (i+1) % 4 != 0:
            graph[i][i+1] = val.pop(0)
            graph[i+1][i] = graph[i][i+1]
        if i < 12:
            graph[i][i+4] = val.pop(0)
            graph[i+4][i] = graph[i][i+4]

def calculate_cost(graph, circuit):
    cost = 0
    for i in range(len(circuit) - 1):
        cost += graph[circuit[i]][circuit[i + 1]]
    return cost


def get_best_health_remaining():
    generate_graph([random.randint(1,10) for _ in range(4*3*2)], GRAPH)

    # Variabel untuk menyimpan sirkuit dengan cost minimum
    min_cost = INF

    # Menghitung cost untuk setiap Hamiltonian circuit dan mencari yang minimum
    for circuit in circuits:
        min_cost = min(calculate_cost(GRAPH, circuit), min_cost)
    return INITIAL_HEALTH - min_cost

history = [get_best_health_remaining() for _ in range(GOAL)]
keys = [bytes(((b1 + b2) for b1, b2 in zip(history[x:x+32], history[x+32:x+64]))) for x in range(len(history)//64)]

data = open("flag.txt", "rb").read()

for key in keys[::-1]:
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    data = ciphertext
cip = ciphertext.hex()
open("secret.txt", "w").write(cip)