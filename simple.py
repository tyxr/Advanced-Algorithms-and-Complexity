import numpy as np
from sys import stdin

class Simplex(object):
    def __init__(self, obj, max_mode=False):  # default is solve min LP, if want to solve max lp,should * -1
        self.mat, self.max_mode = np.array([[0] + obj]) * (-1 if max_mode else 1), max_mode
 
    def add_constraint(self, a, b):
        self.mat = np.vstack([self.mat, [b] + a])
 
    def _simplex(self, mat, B, m, n):
        while mat[0, 1:].min() < 0:
            col = np.where(mat[0, 1:] < 0)[0][0] + 1  # use Bland's method to avoid degeneracy. use mat[0].argmin() ok?
            row = np.array([mat[i][0] / mat[i][col] if mat[i][col] > 0 else 0x7fffffff for i in
                            range(1, mat.shape[0])]).argmin() + 1  # find the theta index
            if mat[row][col] <= 0:
                return "Infinity"  # the theta is ∞, the problem is unbounded
            self._pivot(mat, B, row, col)
        value = mat[0][0] * (1 if self.max_mode else -1)
        obj_dict = {B[i]: mat[i, 0] for i in range(1, m) if B[i] < n}
        return value,obj_dict
 
    def _pivot(self, mat, B, row, col):
        mat[row] /= mat[row][col]
        ids = np.arange(mat.shape[0]) != row
        mat[ids] -= mat[row] * mat[ids, col:col + 1]  # for each i!= row do: mat[i]= mat[i] - mat[row] * mat[i][col]
        B[row] = col
 
    def solve(self):
        m, n = self.mat.shape  # m - 1 is the number slack variables we should add
        temp, B = np.vstack([np.zeros((1, m - 1)), np.eye(m - 1)]), list(range(n - 1, n + m - 1))  # add diagonal array
        mat = self.mat = np.hstack([self.mat, temp])  # combine them!
        if mat[1:, 0].min() < 0:  # is the initial basic solution feasible?
            row = mat[1:, 0].argmin() + 1  # find the index of min b
            temp, mat[0] = np.copy(mat[0]), 0  # set first row value to zero, and store the previous value
            mat = np.hstack([mat, np.array([1] + [-1] * (m - 1)).reshape((-1, 1))])
            self._pivot(mat, B, row, mat.shape[1] - 1)
            if self._simplex(mat, B, m, n)[0] != 0:
                return "No solution"  # the problem has no answer
            if mat.shape[1] - 1 in B:  # if the x0 in B, we should pivot it.
                self._pivot(mat, B, B.index(mat.shape[1] - 1), np.where(mat[0, 1:] != 0)[0][0] + 1)
            self.mat = np.vstack([temp, mat[1:, :-1]])  # recover the first line
            for i, x in enumerate(B[1:]):
                self.mat[0] -= self.mat[0, x] * self.mat[i + 1]
        temp = self._simplex(self.mat, B, m, n)
        if isinstance(temp,str):
            return temp
        else:
            value,obj_dict = temp

        return value,obj_dict
def main():
    '''
    t = Simplex([-1, 2],max_mode=True)
    t.add_constraint([-1,-1],-1)
    t.add_constraint([1,0],2)
    t.add_constraint([0,1],2)
    print(t.solve())
    
    
    
    
    t = Simplex([1, 1],max_mode=True)
    t.add_constraint([1,1],1)
    t.add_constraint([-1,-1],-2)
    print(t.solve())
    print(t.mat)
    
    t = Simplex([1,1,1],max_mode=True)
    t.add_constraint([0,0,1],3)
    
    print(t.solve())
    print(t.mat)
    
    t = Simplex([1, 1],max_mode=True)
    t.add_constraint([1,1],1)
    t.add_constraint([-1,-1],-2)
    print(t.solve())
    print(t.mat)
    '''
    n, m = list(map(int, stdin.readline().split()))
    A = []
    for i in range(n):
        A += [list(map(int, stdin.readline().split()))]
    b = list(map(int, stdin.readline().split()))
    c = list(map(int, stdin.readline().split()))
    t = Simplex(c,max_mode=True)
    for i in range(n):
        t.add_constraint(A[i],b[i])
    ans = t.solve()
    if isinstance (ans,str):
        print (ans)
    else:
        value,obj_dict = ans
        temp = []
        for i in range(1,m+1):
            
            if i in obj_dict:
                temp.append(obj_dict[i])
            else:
                temp.append(0)
        print("Bounded solution")
        print(' '.join(list(map(lambda x : '%.18f' % x, temp))))
    
if __name__ == '__main__':
    main()

