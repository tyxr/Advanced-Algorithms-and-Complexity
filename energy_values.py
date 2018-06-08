# python3

EPS = 1e-6
PRECISION = 20

class Equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row

def ReadEquation():
    size = int(input())
    a = []
    b = []
    for row in range(size):
        line = list(map(float, input().split()))
        a.append(line[:size])
        b.append(line[size])
    return Equation(a, b)

def SelectPivotElement(a, step):
    # This algorithm selects the first free element.
    # You'll need to improve it to pass the problem.
    '''pivot_element = Position(0, 0)
    while used_rows[pivot_element.row]:
        pivot_element.row += 1
    while used_columns[pivot_element.column]:
        pivot_element.column += 1
    return pivot_element'''
    max_= step
    for i in range(step+1,len(a)):
        if abs(a[i][step]) > abs(a[max_][step]):
            max_ = i
    return Position(max_, step)

def SwapLines(a, b, used_rows, pivot_element):
    a[pivot_element.column], a[pivot_element.row] = a[pivot_element.row], a[pivot_element.column]
    b[pivot_element.column], b[pivot_element.row] = b[pivot_element.row], b[pivot_element.column]
    used_rows[pivot_element.column], used_rows[pivot_element.row] = used_rows[pivot_element.row], used_rows[pivot_element.column]
    pivot_element.column = pivot_element.row
    
def ProcessPivotElement(a, b, pivot_element):
    # Write your code here
    
    for i in range(pivot_element.column+1,len(b)):
        
        alpha = a[i][pivot_element.column] / a[pivot_element.row][pivot_element.column]
        b[i] -= b[pivot_element.row] * alpha
        for j in range(pivot_element.column,len(a)):
            a[i][j] -= a[pivot_element.row][j] * alpha

def MarkPivotElementUsed(pivot_element, used_rows, used_columns):
    used_rows[pivot_element.row] = True
    used_columns[pivot_element.column] = True

def SolveEquation(equation):
    a = equation.a
    b = equation.b
    size = len(a)

    used_columns = [False] * size
    used_rows = [False] * size
    for step in range(size):
        pivot_element = SelectPivotElement(a, step)
        SwapLines(a, b, used_rows, pivot_element)
        ProcessPivotElement(a, b, pivot_element)
        MarkPivotElementUsed(pivot_element, used_rows, used_columns)
    for i in range(size-1,-1,-1):
        firstCoef = a[i][i]

        
        for j in range(i + 1,len(a[0])):
            b[i] -= b[j] * a[i][j]
        b[i] /= firstCoef
    return b

def PrintColumn(column):
    size = len(column)
    for row in range(size):
        print("%.20lf" % column[row])

if __name__ == "__main__":
    equation = ReadEquation()
    solution = SolveEquation(equation)
    PrintColumn(solution)
    exit(0)
