import numpy as np
import skfuzzy as fuzz
import random

f = open("text.txt", "rb").read()

O1 = np.arange(0, 10, 0.5)
O2  = np.arange(0, 10, 0.5)

O1_I = fuzz.trapmf(O1, [0, 0, 1.5, 2])
O1_II = fuzz.trimf(O1, [1.5, 3, 4.5])
O1_III = fuzz.trapmf(O1, [3, 4.5, 8, 10])

O2_I = fuzz.trapmf(O2, [0, 0, 6, 7])
O2_II = fuzz.trimf(O2, [6, 7, 8])
O2_III = fuzz.trapmf(O2, [7, 8, 9, 10])

random.seed(0x2024)

X = np.arange(0, 128, 1)
output_1 = []
output_2 = []
output_3 = []

for value in f:
    V = [random.randint(40, 128) for _ in range(4)]
    V.sort()

    X_I = fuzz.trapmf(X, [0, 0, 32, 45])
    X_II = fuzz.trimf(X, [40, V[0], V[1]])
    X_III = fuzz.trimf(X, [V[0], (V[1]+V[2])/2, V[3]])
    X_IV = fuzz.trimf(X, [V[2], V[3], 128])

    O1_r1 = np.fmin(fuzz.interp_membership(X, X_I, value), O1_III)
    O2_r1 = np.fmin(fuzz.interp_membership(X, X_I, value), O2_I)

    O1_r2 = np.fmin(fuzz.interp_membership(X, X_II, value), O1_II)
    O2_r2 = np.fmin(fuzz.interp_membership(X, X_II, value), O2_I)

    O1_r3 = np.fmin(fuzz.interp_membership(X, X_III, value), O1_I)
    O2_r3 = np.fmin(fuzz.interp_membership(X, X_III, value), O2_II)

    O1_r4 = np.fmin(fuzz.interp_membership(X, X_IV, value), O1_II)
    O2_r4 = np.fmin(fuzz.interp_membership(X, X_IV, value), O2_III)

    Aggr_O1 = np.fmax(O1_r1, np.fmax(O1_r2, np.fmax(O1_r3, O1_r4)))
    Aggr_O2 = np.fmax(O2_r1, np.fmax(O2_r2, np.fmax(O2_r3, O2_r4)))

    O1_defuzzy = fuzz.defuzz(O1, Aggr_O1, 'mom')
    O1_level = fuzz.interp_membership(O1, Aggr_O1, O1_defuzzy)

    O2_defuzzy = fuzz.defuzz(O2, Aggr_O2, 'lom')
    
    output_1.append(O1_defuzzy)
    output_2.append(O2_defuzzy)
    output_3.append(O1_level)

o = open("output.txt", "w")
o.write(str(output_1)+'\n')
o.write(str(output_2)+'\n')
o.write(str(output_3)+'\n')