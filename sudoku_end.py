from membermgmt import * # - 파일에서 게임 기록 정보 읽기 함수, 파일에 게임기록 정보 쓰기 함수 내재함
import time
# 로그인 -- 변형
def login(members):
    username = input('Enter your name: (4letters max) ')
    while len(username) > 4:
        username = input('Enter your name: (4letters max) ')
    trypasswd = input('Enter your passwd: ')
    if username in members.keys():     # member dictionary에 입력한 username 있는 경우
        if trypasswd == members[username][0]:
            times = members[username][1]  ### 걸린시간
            print("현재 최고 기록은", times, "초 입니다.") #######
            return username, times, members
        else:
            return login(members)
    else:
        members[username] = (trypasswd, 0)  # members dictionary에 새로운 username을 추가한다.
        return username, 0.0, members

import random
def transpose(board):
    transposed = []
    size = len(board)
    transposed = [[] for _ in range(size)]
    for row in board:
        for i in range(size):
            transposed[i].append(row[i])
    return transposed

def make_holes(board, no_of_holes):
    while no_of_holes > 0:
        i = random.randint(0,8)
        j = random.randint(0,8)
        if board[i][j] != 0:
            board[i][j] = 0
            no_of_holes -= 1
    return board

def initialize_board_9x9():
    row0 = [i for i in range(1,10)]
    random.shuffle(row0)
    row1 = row0[3:6]+row0[6:]+row0[0:3]
    row2 = row0[6:]+row0[0:3]+row0[3:6]
    row3 = [row0[1],row0[2],row0[0],row0[4],row0[5],row0[3],row0[7],row0[8],row0[6]]
    row4 = row3[3:6]+row3[6:]+row3[0:3]
    row5 = row3[6:]+row3[0:3]+row3[3:6]
    row6 = [row3[1],row3[2],row3[0],row3[4],row3[5],row3[3],row3[7],row3[8],row3[6]]
    row7 = row6[3:6]+row6[6:]+row6[0:3]
    row8 = row6[6:]+row6[0:3]+row6[3:6]
    return [row0,row1,row2,row3,row4,row5,row6,row7,row8]

def shuffle_ribbons(board):
    top = board[:3]
    medium = board[3:6]
    bottom = board[6:]
    random.shuffle(top)
    random.shuffle(medium)
    random.shuffle(bottom)
    return top + medium + bottom

def create_solution_board_9x9():
    board = initialize_board_9x9()
    board = shuffle_ribbons(board)
    board = transpose(board)
    board = shuffle_ribbons(board)
    board = transpose(board)
    return board

def get_level():
    print("난이도를 선택해주세요")
    level = input("초심자=1, 중급자=2, 고급자=3 : ")
    while level not in ("1", "2", "3"):
        level = input("초심자=1, 중급자=2, 고급자=3 : ")
    if level == "1":
        return 8
    elif level == "2":
        return 16
    else:
        return 24

def show_board(board):
    for row in board:
        for entry in row:
            if entry == 0:
                print('.', end=' ')
            else:
                print(entry, end=' ')
        print()

def get_integer(message, i ,j):
    number = input(message)
    while not (number.isdigit() and i <= int(number) <= j):
        number = input(message)
    return int(number)

def copy_board(board):
    board_clone = []
    for row in board:
        board_clone.append(row[:])
    return board_clone

def re(message):
    while True:
        x = input(message)
        if x == 'n':
            return False
        elif x == 'y':
            return True

def time_record(a):
    if (a == 1):
        global start
        start = time.time()
    elif (a == 0):
        record = time.time() - start
        return round(record,2)


def sudoku_nineplus():
    a = 0
    attempt = 4
    print('스도쿠 게임에 오신걸 환영합니다.')
    username, times_sofar, members = login(load_members())
    solution_board = create_solution_board_9x9()
    puzzle_board = copy_board(solution_board)
    no_of_holes = get_level()
    puzzle_board = make_holes(puzzle_board, no_of_holes)
    show_board(puzzle_board)
    time_record(1)#시간측정 시작
    while no_of_holes > 0:
        i = get_integer("세로줄 번호(1,2,3,4,5,6,7,8,9): ",1,9) - 1
        j = get_integer("가로줄 번호(1,2,3,4,5,6,7,8,9): ",1,9) - 1
        if puzzle_board[i][j] != 0:
            print('빈 칸이 아닙니다!')
            continue
        n = get_integer('들어갈 숫자를 입력하세요(1,2,3,4,5,6,7,8,9): ',1,9)
        if n == solution_board[i][j]:
            puzzle_board[i][j] = solution_board[i][j]
            show_board(puzzle_board)
            no_of_holes -= 1
        else:
            if attempt == 1:
                if re("모든 기회를 소진하셨습니다. 다시 시도하겠습니까? (y/n) "):
                    a = 1
                    break
                else:
                    a = 2
                    print("다음에 다시시도해보세요.")
                    break
            attempt -= 1
            if attempt > 1:
                print(n,": 틀렸습니다", attempt, "번의 기회가 남아있습니다.")
            elif attempt == 1:
                print(n,": 틀렸습니다", "이제 마지막 기회입니다.")
    if a == 0:
        print("클리어하셨습니다! 축하합니다.")
        record = time_record(0)
        print('클리어까지', record, '초가 걸렸습니다..')#시간측정 종료 및 소요시간 출력
        if times_sofar == 0.0 or times_sofar > record:
            print("최고기록을 갱신합니다!")
            members[username] = (members[username][0],record)
        store_members(members)
    elif a == 1:
        sudoku_nineplus()

        
sudoku_nineplus()
