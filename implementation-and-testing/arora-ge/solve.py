#Source: https://11dimensions.moe/archives/267

from sage.all import *
from tqdm import tqdm

q = 127
n = 20
r = 5

def enc(z):
    for con, mon in z:
        return (con, mon.degrees())

def dec(p, l):
    cons, degs = p
    for i, j in zip(degs, l):
        if i != 0:
            cons *= F(j)**i
    return cons

F = GF(q)
Q = F[','.join([f'a{i}' for i in range(n)] + ['b'])]
aas = vector(Q.gens()[:-1])
bb = Q.gens()[-1]
T = Q[','.join([f'x{i}' for i in range(n)] + ['e'])]
g = vector(T.gens()[:-1])
ee = T.gens()[-1]
y = prod(1 + sum(g) + ee for _ in range(r)).monomials()
ff = prod(bb - aas * g - ee for _ in range(r))
pat = [ff.monomial_coefficient(z) for z in y]

ppat = [enc(p) for p in pat]
test = set(deg for _, deg in ppat)
print(len(y))

inss = []
with open('data.txt', 'r') as f:
    for line in f.readlines():
        _, ins = line.split(':')
        ins = eval(ins)
        inss.append(ins)

m = len(y)

cs = []

for i in tqdm(range(m)):
    a, b = inss[i]
    a.append(b)
    cs.append([dec(p, a) for p in ppat])

cs = matrix(cs)
A = cs.right_kernel_matrix()

v = vector(A)
v /= v[-1]

print(''.join(chr(i) for i in v[-2 - n:-2]))