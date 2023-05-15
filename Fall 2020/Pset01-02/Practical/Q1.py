import queue

RUBIC_3X3_DIS = [1, 1, 0, 1, 1]
PTR_3X3 = RUBIC_3X3_DIS[2:]

RUBIC_4X4_DIS = [1, 2, 1, 0, 1, 2, 1]
PTR_4X4 = RUBIC_4X4_DIS[3:]

n = 0

class Rubic:
    def __init__(self, mat):
        self.mat = mat
        self.heuristic = 0
        self.path = 0
        self.setHeuristic()
    
    def right(self, rub, row):
        for j in range(n, n * 2):
            self.mat[row][j % n] = rub.mat[row][(j - 1) % n]
    
    def left(self, rub, row):
        for j in range(n, n * 2):
            self.mat[row][j % n] = rub.mat[row][(j + 1) % n]
    
    def up(self, rub, col):
        for i in range(n, n * 2):
            self.mat[i % n][col] = rub.mat[(i + 1) % n][col]
    
    def down(self, rub, col):
        for i in range(n, n * 2):
            self.mat[i % n][col] = rub.mat[(i - 1) % n][col]
    
    def setHeuristic(self):
        self.heuristic = 2
        for i in range(n):
            for j in range(n):
                num = self.mat[i][j]
                r = num // n
                c = num % n
                if n == 4:
                    self.heuristic += PTR_4X4[r - i]
                    self.heuristic += PTR_4X4[c - j]
                else:
                    self.heuristic += PTR_3X3[r - i]
                    self.heuristic += PTR_3X3[c - j]
        self.heuristic //= n

    def pr(self):
        for i in range(n):
            for j in range(n):
                print(self.mat[i][j], "\t", end="")
            print()
        print()
        self.heuristic = 0
        for i in range(n):
            for j in range(n):
                num = self.mat[i][j]
                r = num // n
                c = num % n
                if n == 4:
                    self.heuristic += PTR_4X4[r - i]
                    self.heuristic += PTR_4X4[c - j]
                else:
                    self.heuristic += PTR_3X3[r - i]
                    self.heuristic += PTR_3X3[c - j]
                print("(", i, " ", j, ")")
                print("r:", r)
                print("c:", c)
                print("hue:", self.heuristic, "\n")
        self.heuristic //= n

mat = [[]]

n = int(input())

for i in range(n):
    mat.append(list(map(int, input().split())))
    mat[i] = [x - 1 for x in mat[i]]

stack = queue.PriorityQueue()
stack.put(Rubic(mat))

while not stack.empty():
    rub = stack.get()
    if rub.heuristic == 0:
        print(rub.path)
        # rub.pr()
        break
    for i in range(n * 4):
        stack.put(Rubic(rub, i))