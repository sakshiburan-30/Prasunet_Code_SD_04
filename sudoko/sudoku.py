import tkinter as tk
from tkinter import messagebox


class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid

    def is_safe(self, row, col, num):
        # Check if `num` is not in the current row
        for x in range(9):
            if self.grid[row][x] == num:
                return False

        # Check if `num` is not in the current column
        for x in range(9):
            if self.grid[x][col] == num:
                return False

        # Check if `num` is not in the current 3x3 box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.grid[i + start_row][j + start_col] == num:
                    return False
        return True

    def solve(self):
        empty_pos = self.find_empty()
        if not empty_pos:
            return True  # Puzzle solved
        row, col = empty_pos

        for num in range(1, 10):
            if self.is_safe(row, col, num):
                self.grid[row][col] = num

                if self.solve():
                    return True

                # Reset the cell (backtrack)
                self.grid[row][col] = 0

        return False

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:  # 0 represents an empty cell
                    return (i, j)  # Row, Column
        return None

    def print_grid(self):
        for row in self.grid:
            print(" ".join(str(num) if num != 0 else '.' for num in row))


class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.geometry("400x500")

        self.grid = [[0] * 9 for _ in range(9)]
        self.entries = [[None] * 9 for _ in range(9)]

        # Create input grid
        for i in range(9):
            for j in range(9):
                self.entries[i][j] = tk.Entry(root, width=3, font=('Arial', 18), justify='center')
                self.entries[i][j].grid(row=i, column=j, padx=5, pady=5)

        self.solve_button = tk.Button(root, text="Solve", command=self.solve_sudoku, font=('Arial', 14))
        self.solve_button.grid(row=10, columnspan=9, pady=10)

    def solve_sudoku(self):
        # Read input from entries and fill the grid
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                if val.isdigit() and 1 <= int(val) <= 9:
                    self.grid[i][j] = int(val)
                else:
                    self.grid[i][j] = 0

        solver = SudokuSolver(self.grid)

        if solver.solve():
            self.update_grid(solver.grid)
        else:
            messagebox.showinfo("No Solution", "This Sudoku puzzle cannot be solved.")

    def update_grid(self, solved_grid):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, solved_grid[i][j])


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
