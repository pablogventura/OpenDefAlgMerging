import random

N = 5 # cantidad de elementos
J=[[None]*N]*N
M=[None]*N
Q=[None]*N
for i in range(N):
    for j in range(N):
        if i != j:
            J[i][i] = i
            J[i][j] = -1

def S(i):
    # the least positive integer j such that j**2 >= i and j >= 2.
    j=2
    while True:
        if j**2>=i:
            return j
        j+=1

def rnd(i):
    return random.randint(0,i-1)

def FindMax (i):
    global N
    global J
    global M
    global Q
    k = 0;
    j, s, a = 0,0,0
    for j in range(i):
        s = 1
        for a in range(i):
            if (a  != j and J[a][j] == a):
                s = 0
            if (s):
                M[k] = j
                k+=1
    a = rnd (k)
    a+=1
    for j in range(k):
        Q[j] = 0;
    for s in range(a):
        j = rnd (k);
        if (Q[j]):
            s-=1
        else:
            Q[j] = 1;
    return k;


def Work (i):
    global N
    global J
    global M
    global Q
    j, l, w, s, q, u = 0,0,0,0,0,0
    if (i == N - 1):
    
        for j in range(N):
            for l in range(N):
                if (J[j][l] == -1):
                    J[j][l] = N - 1;
        return;
    
    q = S(N - i)
    if (i == 1):
    
        u = 1;
        M[0] = 0;
        Q[0] = 1;

    elif ( not rnd (q)):
        u = FindMax (i);
    for j in range(u):
        if (Q[j]):
        
            J[M[j]][i] = i;
            J[i][M[j]] = i;
        
    w = 1;
    while (w):
    
        w = 0;
        for j in range(i):
            if (J[j][i] == i):
                for s in range(i):
                    if (J[s][j] == j and J[s][i]  != i):
                    
                        w = 1;
                        J[s][i] = i;
                        J[i][s] = i;
                    
        for j in range(i):
            if (J[j][i] == i):
                for l in range(i):
                    if (J[l][i] == i):
                        
                        s = J[j][l];
                        if (s  != -1 and J[s][i]  != i):
                        
                            w = 1;
                            J[s][i] = i;
                            J[i][s] = i;

    for j in range(i):
        if (J[j][i] == i):
            for l in range(i):
                if (J[l][i] == i and J[j][l] == -1):
                    
                    J[j][l] = i;
                    J[l][j] = i;

def main():
    Work(2)
    for j in J:
        print(j)
if __name__ == "__main__":
    main()
