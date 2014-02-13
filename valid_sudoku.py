class Solution:
    # @param board, a 9x9 2D array
    # @return a boolean
    def isValidSudoku(self, board):
        # check rows
        for i in range(9):
            vset = set()
            for j in range(9):

                if board[i][j] != '.':
                    if board[i][j] in vset:
                        return False
                    else:
                        vset.add(board[i][j])
        # check columns
        for j in range(9):
            vset = set()
            for i in range(9):

                if board[i][j] != '.':
                    if board[i][j] in vset:
                        return False
                    else:
                        vset.add(board[i][j])

        # check boxes
        corners = [(i,j) for i in range(0,7,3) for j in range(0,7,3)]
        for x,y in corners:
            vset = set()
            for i in range(x, x+3):
                for j in range(y, y+3):
                    if board[i][j] != '.':
                        if board[i][j] in vset:
                            return False
                        else:
                            vset.add(board[i][j])
        return True

board = [".87654321","2........","3........","4........","5........","6........","7........","8........","9........"]
s = Solution()
print s.isValidSudoku(board)