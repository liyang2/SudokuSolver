from Queue import Queue

# this advanced version of sudoku solver combined inference with search
# thus it can tackle much more hard sudoku puzzles
class Assignment:
    def __init__(self, pos, val):
        self.pos = pos
        self.val = val

    def __str__(self):
        return "Assign " + str(self.val) + " to " + str((self.pos[0]+1, self.pos[1]+1))


class Sudoku:
    def __init__(self):
        self.range = {}
        self.row_cells = [[(i, j) for j in range(9)] for i in range(9)]
        self.column_cells = [[(j, i) for j in range(9)] for i in range(9)]
        self.box_cells = {}
        '''
        nine boxes indexed by
        (0,0), (0,3), (0,6)
        (3,0), (3,3), (3,6)
        (6,0), (6,3), (6,6)
        '''
        # fill box cells
        for pos in [(i, j) for i in range(0, 7, 3) for j in range(0, 7, 3)]:
            self.box_cells[pos] = []
            for i in range(pos[0], pos[0] + 3):
                for j in range(pos[1], pos[1] + 3):
                    self.box_cells[pos].append((i, j))

        #inititialize each cell's range
        for i in range(9):
            for j in range(9):
                self.range[(i, j)] = range(1, 10)

    # try to narrow down each cell's range before searching
    def inference(self, board):
        self.assignments = Queue()
        for i in range(9):
            for j in range(9):
                if board[i][j] != None:
                    self.assignments.put(Assignment( (i,j),board[i][j] ))

        while not self.assignments.empty():
            a = self.assignments.get()
            board[a.pos[0]][a.pos[1]] = a.val

            self.update_range(a.pos, a.val)
            if self.assignments.empty():
                for assign in set(self.naked_single(board) + self.hidden_single(board)):
                    self.assignments.put(assign)

    # select an empty cell according to the minimum- remaining-values heuristic
    def empty_cell(self, board):
        returnPos = None
        for i in range(9):
            for j in range(9):
                if board[i][j] == None and len(self.range[(i,j)]) == 0:
                    return 'fail'
                elif board[i][j] == None:
                    if returnPos == None:
                        returnPos = (i,j)
                    else:
                        if len(self.range[(i,j)]) < len(self.range[returnPos]):
                            returnPos = (i,j)
        return returnPos

    def sudoku_solve(self,board):
        self.inference(board)
        self.solve(board)

    # search for solution recursively
    def solve(self, board):  # board is 9*9 array
        pos = self.empty_cell(board)

        if pos == None:
            return 'success'
        elif pos == 'fail':
            return 'fail'
        else:
            for val in self.range[pos]:
                board[pos[0]][pos[1]] = val
                if self.is_valid(board,pos) and self.solve(board) == 'success':
                    return 'success'
                else:
                    # recover the board
                    board[pos[0]][pos[1]] = None

    # check whether the board is still valid after assigning some value to a cell
    def is_valid(self, board, position):
        # check column
        mset = set()
        for pos in self.column_cells[position[1]]:
            if board[pos[0]][pos[1]] != None:
                if board[pos[0]][pos[1]] in mset:
                    return False
                else:
                    mset.add(board[pos[0]][pos[1]])
        # check row
        mset.clear()
        for pos in self.row_cells[position[0]]:
            if board[pos[0]][pos[1]] != None:
                if board[pos[0]][pos[1]] in mset:
                    return False
                else:
                    mset.add(board[pos[0]][pos[1]])
        # check box
        mset.clear()
        for pos in self.box_cells[(position[0] / 3 * 3, position[1] / 3 * 3)]:
            if board[pos[0]][pos[1]] != None:
                if board[pos[0]][pos[1]] in mset:
                    return False
                else:
                    mset.add(board[pos[0]][pos[1]])
        return True


    def update_range(self, pos, val):
        # remove all in current square
        del self.range[pos][:]

        # update cells' range in the same row, same column, same box
        left_top = (pos[0] / 3 * 3, pos[1] / 3 * 3)
        for pos in self.column_cells[pos[1]] + self.row_cells[pos[0]] + self.box_cells[left_top]:
            if val in self.range[pos]:
                self.range[pos].remove(val)

    # strategies to find new assignments
    def naked_single(self, board):
        new_assigns = []
        for i in range(9):
            for j in range(9):
                if board[i][j] != None:
                    continue
                if len(self.range[(i, j)]) == 1:
                    new_assigns.append(Assignment((i, j), self.range[(i, j)][0]))
        return new_assigns

    def hidden_single(self, board):
        new_assigns = []
        for i in range(9):
            for j in range(9):
                if board[i][j] != None:
                    continue
                for val in self.range[(i, j)]:
                    # check same row
                    cell_contain_val = False
                    for pos in self.row_cells[i]:
                        if pos != (i, j) and self.range[pos].count(val) > 0:
                            cell_contain_val = True
                            break
                    if cell_contain_val == False:
                        new_assigns.append(Assignment((i, j), val))
                        break

                    # check same column
                    cell_contain_val = False
                    for pos in self.column_cells[j]:
                        if pos != (i, j) and self.range[pos].count(val) > 0:
                            cell_contain_val = True
                            break
                    if cell_contain_val == False:
                        new_assigns.append(Assignment((i, j), val))
                        break

                    # check same box
                    cell_contain_val = False
                    for pos in self.box_cells[(i / 3 * 3, j / 3 * 3)]:
                        if pos != (i, j) and self.range[pos].count(val) > 0:
                            cell_contain_val = True
                            break
                    if cell_contain_val == False:
                        new_assigns.append(Assignment((i, j), val))
                        break

        return new_assigns


board = [[7,4,None,None,None,None,6,None,None],
         [None,None,None,None,None,None,5,None,8],
         [None,None,9,None,3,8,None,None,7],
         [None,9,None,1,8,None,None,None,None],
         [None,None,6,None,None,None,7,None,None],
         [None,None,None,None,7,4,None,8,None],
         [3,None,None,2,6,None,8,None,None],
         [9,None,1,None,None,None,None,None,None],
         [None,None,2,None,None,None,None,1,3]]


solver = Sudoku()
solver.sudoku_solve(board)


for row in board:
    print row


