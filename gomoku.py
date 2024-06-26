"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Vanessa Lu and Erin Stewart (and Michael Guerzhoy with tests contributed by Siavash Kazemian)
Last modified: Nov. 16, 2022
"""

def is_empty(board):
    for x in range(len(board)):
        for i in range(len(board[x])):
            if board[x][i] != " ":
                return False
    return True

def is_sq_in_board(board, y, x):
    return y < len(board) and y >= 0 and x >= 0 and x < len(board[0])

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    if is_sq_in_board(board, y_end - length*d_y, x_end - length*d_x) and board[y_end - length*d_y][x_end - length*d_x] == " ":
        if is_sq_in_board(board, y_end + d_y, x_end + d_x) and board[y_end + d_y][x_end + d_x] == " ":
            return "OPEN"
        else:
            return "SEMIOPEN"
    else:
        if is_sq_in_board(board, y_end + d_y, x_end + d_x) and board[y_end + d_y][x_end + d_x] == " ":
            return "SEMIOPEN"
        else:
            return "CLOSED"

def is_sequence_complete(board, col, y_start, x_start, d_y, d_x, length):
    if is_sq_in_board(board, y_start - d_y, x_start - d_x): #if at left edge of board
        if board[y_start - d_y][x_start - d_x] == col: #if same colour at beginning
            return False
    for i in range(length):
        if is_sq_in_board(board, y_start, x_start) and board[y_start][x_start] == col: #if whole length on board + are same col
            y_start += d_y
            x_start += d_x
        else:
            return False
    if is_sq_in_board(board, y_start, x_start):
        if board[y_start][x_start] == col:
            return False
    return True

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    num_open = 0
    num_semi = 0
    while is_sq_in_board(board, y_start, x_start):
        if is_sequence_complete(board, col, y_start, x_start, d_y, d_x, length):
            if is_bounded(board, y_start + (length - 1)*d_y, x_start + (length - 1)*d_x, length, d_y, d_x) == "OPEN":
                num_open += 1
            elif is_bounded(board, y_start + (length - 1)*d_y, x_start + (length - 1)*d_x, length, d_y, d_x) == "SEMIOPEN":
                num_semi += 1
        y_start += d_y
        x_start += d_x
    # print(num_open, num_semi)
    return num_open, num_semi

def detect_rows(board, col, length):
    num_open, num_semi = 0, 0
    for i in range(8):
        open, semi = detect_row(board, col, i, 0, length, 0, 1)
        num_open += open
        num_semi += semi
        open, semi = detect_row(board, col, 0, i, length, 1, 0)
        num_open += open
        num_semi += semi
        open, semi = detect_row(board, col, i, 0, length, 1, 1)
        num_open += open
        num_semi += semi
        if i > 0:
            open, semi = detect_row(board, col, 0, i, length, 1, 1)
            num_open += open
            num_semi += semi
        open, semi = detect_row(board, col, 0, i, length, 1, -1)
        num_open += open
        num_semi += semi
        if i > 0:
          open, semi = detect_row(board, col, i, 7, length, 1, -1)
          num_open += open
          num_semi += semi
    #print(num_open, num_semi)
    return num_open, num_semi

def search_max(board):
    move_y = 0
    move_x = 0
    max_score = -100001
    mid_score = 0

    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == " ":
                board[y][x] = "b"
                if is_sequence_complete(board, "b", y, x, 1, 0, 5) or is_sequence_complete(board, "b", y, x, 0, 1, 5) or is_sequence_complete(board, "b", y, x, 1, 1, 5) or is_sequence_complete(board, "b", y, x, 1, -1, 5): #check if closed win
                    return y, x
                mid_score = score(board)
                #print(mid_score)
                if mid_score > max_score:
                    max_score = mid_score
                    move_x = x
                    move_y = y
                board[y][x] = " "
    #print(move_y, move_x)
    return move_y, move_x

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6): #stores num of open + semi rows of black + white from lengths 2 to 5
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:   #if there is 5 blacks in a row (win)
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1: #if there is 5 whites in a row (lose)
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    for y in range(len(board)):
        for x in range(len(board[y])):
            if is_sequence_complete(board, "b", y, x, 1, 0, 5) or is_sequence_complete(board, "b", y, x, 0, 1, 5) or is_sequence_complete(board, "b", y, x, 1, 1, 5) or is_sequence_complete(board, "b", y, x, 1, -1, 5): #check if closed win
                return 'Black won'
            if is_sequence_complete(board, "w", y, x, 1, 0, 5) or is_sequence_complete(board, "w", y, x, 0, 1, 5) or is_sequence_complete(board, "w", y, x, 1, 1, 5) or is_sequence_complete(board, "w", y, x, 1, -1, 5): #check if closed win
                return 'White won'
    for i in range(len(board)):
        for x in range(len(board[i])):
            if board[i][x] == " ":
                return "Continue playing"
    return "Draw"

def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    #TEST OPEN CASES
    #test vertical
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    print(is_bounded(board, y_end, x_end, length, d_y, d_x))
    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

    #test horizontal
    board = make_empty_board(8)
    x = 4; y = 1; d_x = 1; d_y = 0; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 1
    x_end = 6

    print(is_bounded(board, y_end, x_end, length, d_y, d_x))
    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

    #test diagonal left to right
    board = make_empty_board(8)
    x = 4; y = 1; d_x = 1; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 6

    print(is_bounded(board, y_end, x_end, length, d_y, d_x))
    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

    #test diagonal right to left
    board = make_empty_board(8)
    x = 4; y = 1; d_x = -1; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 2

    print(is_bounded(board, y_end, x_end, length, d_y, d_x))
    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

    #TEST SEMIOPEN CASES
    #test vertical
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    put_seq_on_board(board, 4, 5, 0, 1, 1, "b")
    print_board(board)

    y_end = 3
    x_end = 5

    print(is_bounded(board, y_end, x_end, length, d_y, d_x))
    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'SEMIOPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

    #test horizontal
    board = make_empty_board(8)
    x = 4; y = 1; d_x = 1; d_y = 0; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    put_seq_on_board(board, 1, 3, 0, 1, 1, "b")
    print_board(board)

    y_end = 1
    x_end = 6

    print(is_bounded(board, y_end, x_end, length, d_y, d_x))
    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'SEMIOPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

    #test diagonal left to right
    board = make_empty_board(8)
    x = 4; y = 1; d_x = 1; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    put_seq_on_board(board, 0, 3, 0, 1, 1, "b")
    print_board(board)

    y_end = 3
    x_end = 6

    print(is_bounded(board, y_end, x_end, length, d_y, d_x))
    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'SEMIOPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

    #test diagonal right to left
    board = make_empty_board(8)
    x = 4; y = 1; d_x = -1; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    put_seq_on_board(board, 0, 5, 0, 1, 1, "b")
    print_board(board)

    y_end = 3
    x_end = 2

    print(is_bounded(board, y_end, x_end, length, d_y, d_x))
    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'SEMIOPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

    #TEST EDGE
    #test vertical
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    put_seq_on_board(board, 4, 5, 0, 1, 1, "b")
    print_board(board)

    y_end = 2
    x_end = 5

    print(is_bounded(board, y_end, x_end, length, d_y, d_x))
    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'SEMIOPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

    #test horizontal
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 1; d_y = 0; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    put_seq_on_board(board, 1, 3, 0, 1, 1, "b")
    print_board(board)

    y_end = 1
    x_end = 7

    print(is_bounded(board, y_end, x_end, length, d_y, d_x))
    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'SEMIOPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

    #test diagonal left to right
    board = make_empty_board(8)
    x = 5; y = 2; d_x = 1; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    put_seq_on_board(board, 0, 3, 0, 1, 1, "b")
    print_board(board)

    y_end = 4
    x_end = 7

    print(is_bounded(board, y_end, x_end, length, d_y, d_x))
    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'SEMIOPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

    #test diagonal right to left
    board = make_empty_board(8)
    x = 2; y = 2; d_x = -1; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    put_seq_on_board(board, 0, 5, 0, 1, 1, "b")
    print_board(board)

    y_end = 4
    x_end = 0

    print(is_bounded(board, y_end, x_end, length, d_y, d_x))
    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'SEMIOPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

def test_detect_row():
    #vertical
    board = make_empty_board(8)
    x = 4; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    print(detect_row(board, "w", y, x, length, d_y, d_x))
    if detect_row(board, "w", y,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

    #horizontal
    board = make_empty_board(8)
    x = 4; y = 1; d_x = 1; d_y = 0; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    print(detect_row(board, "w", y, x, length, d_y, d_x))
    if detect_row(board, "w", y,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

    #diagonal LR
    board = make_empty_board(8)
    x = 4; y = 1; d_x = 1; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    print(detect_row(board, "w", y, x, length, d_y, d_x))
    if detect_row(board, "w", y,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

    #diagonal RL
    board = make_empty_board(8)
    x = 4; y = 1; d_x = -1; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    print(detect_row(board, "w", y, x, length, d_y, d_x))
    if detect_row(board, "w", y,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 1; y = 1; d_x = 1; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (0,0):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

    board = make_empty_board(8)
    x = 5; y = 2; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 1; y = 1; d_x = 1; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    #analysis(board)
    if search_max(board) == (0,0):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




if __name__ == '__main__':
    play_gomoku(8)