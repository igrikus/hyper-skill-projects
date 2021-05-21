class Field:
    grid = []

    def __init__(self):
        self.__fill()
        self.print()

    def __fill(self):
        input_string = "         "
        for i in range(0, 9, 3):
            row = list(input_string[i:(i + 3)])
            self.grid.append(row)

    def print(self):
        print("---------")
        for row in self.grid:
            print("|", end=" ")
            for symbol in row:
                print(symbol, end=" ")
            print("|")
        print("---------")


class Game:
    field = Field()
    now_step = 'X'

    input_row = -1
    input_col = -1

    def __check_row(self, row_num, symbol):
        first_row_symbol = self.field.grid[row_num][0]
        second_row_symbol = self.field.grid[row_num][1]
        third_row_symbol = self.field.grid[row_num][2]
        return first_row_symbol == second_row_symbol == third_row_symbol == symbol

    def __check_col(self, col_num, symbol):
        first_col_symbol = self.field.grid[0][col_num]
        second_col_symbol = self.field.grid[1][col_num]
        third_col_symbol = self.field.grid[2][col_num]
        if first_col_symbol == second_col_symbol == third_col_symbol == symbol:
            return True
        return False

    def __check_diagonal(self, symbol):
        if self.__check_left_diagonal(symbol):
            return True
        if self.__check_right_diagonal(symbol):
            return True
        return False

    def __check_left_diagonal(self, symbol):
        top_left_symbol = self.field.grid[0][0]
        middle_symbol = self.field.grid[1][1]
        bottom_right_symbol = self.field.grid[2][2]
        return top_left_symbol == middle_symbol == bottom_right_symbol == symbol

    def __check_right_diagonal(self, symbol):
        top_right_symbol = self.field.grid[0][2]
        middle_symbol = self.field.grid[1][1]
        bottom_left_symbol = self.field.grid[2][0]
        return top_right_symbol == middle_symbol == bottom_left_symbol == symbol

    def __check_empty_cells(self):
        for row in self.field.grid:
            for symbol in row:
                if symbol == ' ':
                    return True
        return False

    # def __check_for_impossible(self):
    #     x_count = 0
    #     o_count = 0
    #     for row in self.field.grid:
    #         for symbol in row:
    #             if symbol == 'X':
    #                 x_count += 1
    #             if symbol == 'O':
    #                 o_count += 1
    #     return True if abs(x_count - o_count) > 1 else False

    def __check_win(self, symbol):
        for num in range(3):
            if self.__check_row(num, symbol):
                return True
            if self.__check_col(num, symbol):
                return True
        if self.__check_diagonal(symbol):
            return True
        return False

    def check_stage(self):
        x_win = self.__check_win('X')
        o_win = self.__check_win('O')
        # if x_win and o_win:
        #     return "Impossible"
        # if self.__check_for_impossible():
        #     return "Impossible"
        if not x_win and not o_win:
            if self.__check_empty_cells():
                return "Game not finished"
            else:
                return "Draw"
        if x_win and not o_win:
            return "X wins"
        if o_win and not x_win:
            return "O wins"

    def __get_coordinates(self):
        input_values = input("Enter the coordinates: ").split()
        if len(input_values) != 2 or not input_values[0].isdigit() or not input_values[1].isdigit():
            print("You should enter numbers!")
            self.__get_coordinates()
            return
        row = int(input_values[0])
        col = int(input_values[1])
        if row < 1 or row > 3 or col < 1 or col > 3:
            print("Coordinates should be from 1 to 3!")
            self.__get_coordinates()
            return
        row -= 1
        col -= 1
        if self.field.grid[row][col] != ' ':
            print("This cell is occupied! Choose another one!")
            self.__get_coordinates()
            return
        self.input_row = row
        self.input_col = col

    def __insert_cell(self):
        self.__get_coordinates()
        self.field.grid[self.input_row][self.input_col] = self.now_step
        self.__change_step()
        self.field.print()

    def __change_step(self):
        if self.now_step == 'X':
            self.now_step = 'O'
        elif self.now_step == 'O':
            self.now_step = 'X'

    def play(self):
        stage = self.check_stage()
        while stage == "Game not finished":
            self.__insert_cell()
            stage = self.check_stage()
        print(stage)


game = Game()
game.play()
