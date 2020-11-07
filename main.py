
def print_board(board):
    count = 0
    line = ""
    domain = ''

    for var in self.variables:
        if len(board[var]) > 1:
            domain += '0'
        else:
            domain += str(board[var])

    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                #print(" | ", end="")
                line += ' | '

            if j == 8:
                print(board[i][j])

            else:
                print(str(board[i][j]) + " ", end="")
                line += domain[count]
                count += 1
        print(line + '|')
        line = ''


def find_empty(board):
    empty = []
    for i in range(len(board)):  # row
        for j in range(len(board[0])):  # col
            num = int(board[i][j])
            if num == 0:
                position = [i, j]
                empty.append(position)
                # return (i, j)
    return empty


def main():
    board = []

    filepath = 'test.txt'
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            values = line.split(' ')
            values.pop()
            board.append(values)
            line = fp.readline()

    # for x in board:
    #    print(*x)

    print_board(board)
    print()
    empty = find_empty(board)
    print("Empty spaces:")
    for i in empty:
        print(*i)


if "__name__" == "__main__":
    main()
