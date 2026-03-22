# ============================================================
# Level 3 - Task 3: N-Queens Problem
# Codveda Python Development Internship
#
# Finds ALL solutions for the N-Queens problem using
# backtracking. Displays each solution as a chessboard.
# ============================================================

def is_safe(board, row, col, n):
    """
    Check whether placing a queen at (row, col) is safe:
      - no queen in the same column
      - no queen on either diagonal
    (Row safety is guaranteed by placing exactly one queen per row.)
    """
    # Check column
    for r in range(row):
        if board[r] == col:
            return False

    # Check upper-left diagonal
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0:
        if board[r] == c:
            return False
        r -= 1
        c -= 1

    # Check upper-right diagonal
    r, c = row - 1, col + 1
    while r >= 0 and c < n:
        if board[r] == c:
            return False
        r -= 1
        c += 1

    return True

def solve(board, row, n, solutions):
    """
    Backtracking solver.
    board[r] = column index of the queen placed in row r.
    """
    if row == n:
        solutions.append(board[:])   # found a complete solution
        return

    for col in range(n):
        if is_safe(board, row, col, n):
            board[row] = col
            solve(board, row + 1, n, solutions)
            board[row] = -1           # backtrack

def get_all_solutions(n):
    """Return a list of all solutions for the N-Queens problem."""
    board = [-1] * n
    solutions = []
    solve(board, 0, n, solutions)
    return solutions

def display_board(solution):
    """Print an ASCII chessboard for one solution."""
    n = len(solution)
    border = "+" + ("---+" * n)
    print(border)
    for row in range(n):
        row_str = "|"
        for col in range(n):
            cell = " Q " if solution[row] == col else " . "
            row_str += cell + "|"
        print(row_str)
        print(border)

def main():
    print("=" * 45)
    print("        N-Queens Problem Solver")
    print("=" * 45)

    while True:
        try:
            n = int(input("\nEnter N (board size, 1–15 recommended): "))
            if n < 1:
                print("[Error] N must be at least 1.")
            elif n > 15:
                confirm = input(
                    f"N={n} may produce a very large number of solutions. Continue? (yes/no): "
                ).strip().lower()
                if confirm not in ("yes", "y"):
                    continue
            break
        except ValueError:
            print("[Error] Please enter a valid integer.")

    print(f"\nSolving {n}-Queens …")
    solutions = get_all_solutions(n)
    total = len(solutions)

    if total == 0:
        print(f"No solution exists for N={n}.")
        return

    print(f"Found {total} solution(s) for N={n}.\n")

    # Ask how many to display
    display_limit = min(total, 3)
    try:
        limit = int(input(f"How many solutions to display? (1-{total}, default {display_limit}): ") or display_limit)
        limit = max(1, min(limit, total))
    except ValueError:
        limit = display_limit

    for i, sol in enumerate(solutions[:limit], start=1):
        print(f"\n─── Solution {i}/{total} ───")
        display_board(sol)
        queens = ", ".join(f"Row {r+1} → Col {c+1}" for r, c in enumerate(sol))
        print(f"  Positions: {queens}")

    if limit < total:
        print(f"\n… and {total - limit} more solution(s) not displayed.")

    print(f"\n✅ Total solutions for {n}-Queens: {total}")

if __name__ == "__main__":
    main()
