import pytest

# =========================
# 共通ヘルパ
# =========================

VALID_COLORS = {"R", "G", "B", "Y"}


def make_board(rows, cols, fill="."):
    return [[fill for _ in range(cols)] for _ in range(rows)]


def fill_all(board, color):
    for r in range(len(board)):
        for c in range(len(board[0])):
            board[r][c] = color
    return board


def fill_row(board, row, color):
    for c in range(len(board[0])):
        board[row][c] = color


def fill_col(board, col, color):
    for r in range(len(board)):
        board[r][col] = color


def fill_alternating(board, colors=("R", "Y")):
    for r in range(len(board)):
        for c in range(len(board[0])):
            board[r][c] = colors[(r + c) % len(colors)]


def count_result(result):
    return len(result)


# =========================
# (C) 入力バリデーション
# =========================

@pytest.mark.parametrize("rows, cols", [
    (0, 0),
    (1, 1),
    (5, 12),
    (6, 11),
])
def test_invalid_size(rows, cols):
    sol = Solution()
    board = make_board(rows, cols)

    with pytest.raises(ValueError):
        sol.deleteArea(board)


def test_empty_input():
    sol = Solution()
    with pytest.raises(Exception):
        sol.deleteArea([])


# =========================
# (A) 正常系（生成パターン）
# =========================

@pytest.mark.parametrize("color", list(VALID_COLORS))
def test_all_same_color(color):
    sol = Solution()
    rows, cols = 6, 12
    board = make_board(rows, cols)
    fill_all(board, color)

    result = sol.deleteArea(board)

    assert count_result(result) == rows * cols


@pytest.mark.parametrize("rows, cols", [
    (6, 12),
    (8, 10),  # 拡張ケース
])
def test_one_row(rows, cols):
    sol = Solution()
    board = make_board(rows, cols)

    fill_row(board, 0, "R")

    result = sol.deleteArea(board)

    assert count_result(result) == cols


@pytest.mark.parametrize("rows, cols", [
    (6, 12),
    (8, 10),
])
def test_one_col(rows, cols):
    sol = Solution()
    board = make_board(rows, cols)

    fill_col(board, 0, "R")

    result = sol.deleteArea(board)

    assert count_result(result) == rows


@pytest.mark.parametrize("rows, cols", [
    (6, 12),
    (8, 10),
])
def test_diagonal_not_counted(rows, cols):
    sol = Solution()
    board = make_board(rows, cols)

    fill_alternating(board, ("R", "Y"))

    result = sol.deleteArea(board)

    assert result == []


def test_invalid_char_as_blank():
    sol = Solution()
    rows, cols = 6, 12
    board = make_board(rows, cols, fill="X")

    result = sol.deleteArea(board)

    assert result == []


@pytest.mark.parametrize("colors", [
    ["R", "G", "B", "Y"],
    ["R", "G"],  # 色が減るケース
])
def test_color_variation(colors):
    sol = Solution()
    rows, cols = 6, 12
    board = make_board(rows, cols)

    # 2x2 の塊を作る
    for r in range(2):
        for c in range(2):
            board[r][c] = colors[0]

    result = sol.deleteArea(board)

    assert count_result(result) == 4


# =========================
# 固定ケース（鋭いテスト）
# =========================

def test_exactly_four():
    sol = Solution()
    board = make_board(6, 12)

    coords = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for r, c in coords:
        board[r][c] = "R"

    result = sol.deleteArea(board)

    assert count_result(result) == 4


def test_three_not_deleted():
    sol = Solution()
    board = make_board(6, 12)

    coords = [(0, 0), (0, 1), (0, 2)]
    for r, c in coords:
        board[r][c] = "R"

    result = sol.deleteArea(board)

    assert result == []


def test_separated_groups():
    sol = Solution()
    board = make_board(6, 12)

    group1 = [(0, 0), (0, 1), (1, 0), (1, 1)]
    group2 = [(4, 4), (4, 5), (5, 4), (5, 5)]

    for r, c in group1 + group2:
        board[r][c] = "R"

    result = sol.deleteArea(board)

    assert count_result(result) == 8


def test_mixed_colors_no_merge():
    sol = Solution()
    board = make_board(6, 12)

    # 隣接しているが色が違う
    board[0][0] = "R"
    board[0][1] = "G"
    board[1][0] = "G"
    board[1][1] = "R"

    result = sol.deleteArea(board)

    assert result == []
