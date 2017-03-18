package ar.edu.itba.sia.c12017.g5.gridlock.models;

import java.util.Arrays;
import java.util.stream.IntStream;

/**
 * Created by alebian on 14/03/17.
 */
/*
* The board has centinel cells around the board.
* The board positions are interpreted as:
*    (x = 1, y = 1) +-----+-----+-----+ (y = 1, x = cols)
*                   |     |     |     |
*                   +-----+-----+-----+
*                   |     |     |     |
*                   +-----+-----+-----+
*                   |     |     |     |
* (y = rows, x = 1) +-----+-----+-----+ (rows, cols)
* */
public class Board {
  private static final int MAIN_CHIP_SYMBOL = 1;
  private static final int WALL_SYMBOL = -2;
  private static final int EXIT_SYMBOL = -1;
  private static final int EMPTY_SYMBOL = 0;

  private int rows;
  private int cols;
  private int exitX;
  private int exitY;
  private int[][] board;
  private int nextChip = MAIN_CHIP_SYMBOL + 1;

  public Board(int rows, int cols, int exitX, int exitY) {
    this.rows = rows + 1;
    this.cols = cols + 1;
    this.exitX = exitX;
    this.exitY = exitY;
    createBoard();
  }

  private void createBoard() {
    this.board = new int[this.rows + 1][this.cols + 1];
    fillWalls();
    fillBoard();
    board[this.exitY][this.exitX] = EXIT_SYMBOL;
  }

  private void fillWalls() {
    IntStream.rangeClosed(0, rows).forEach(y -> {
      board[y][0] = WALL_SYMBOL;
      board[y][cols] = WALL_SYMBOL;
    });
    IntStream.rangeClosed(0, cols).forEach(x -> {
      board[0][x] = WALL_SYMBOL;
      board[rows][x] = WALL_SYMBOL;
    });
  }

  private void fillBoard() {
    IntStream.rangeClosed(1, rows - 1).forEach(i ->
      IntStream.rangeClosed(1, cols - 1).forEach(j -> board[i][j] = EMPTY_SYMBOL)
    );
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;

    Board that = (Board) o;

    return Arrays.deepEquals(board, that.board);
  }

  @Override
  public int hashCode() {
    return Arrays.deepHashCode(board);
  }

  public void addChip(boolean main, int sx, int sy, int ex, int ey) {
    int symbol = main ? MAIN_CHIP_SYMBOL : nextChip;
    if (sx == ex) {
      assert (sy < ey);
      // VERTICAL CHIP
      IntStream.rangeClosed(sy, ey).forEach(y -> board[y][sx] = symbol);
    } else if (sy == ey) {
      assert (sx < ex);
      // HORIZONTAL CHIP
      IntStream.rangeClosed(sx, ex).forEach(x -> board[sy][x] = symbol);
    } else {
      throw new IllegalArgumentException("Cannot insert diagonal chips");
    }
    if (!main) {
      nextChip++;
    }
  }

  public boolean isGoal() {
    // TODO
    return false;
  }

  private static final String MAIN_CHIP_PRINT_SYMBOL = "X";
  private static final String VERTICAL_WALL_PRINT_SYMBOL = "|";
  private static final String HORIZONTAL_WALL_PRINT_SYMBOL = "-";
  private static final String CORNER_WALL_PRINT_SYMBOL = "+";
  private static final String EXIT_PRINT_SYMBOL = " ";
  private static final String EMPTY_PRINT_SYMBOL = " ";

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    // Column numbers
    IntStream.rangeClosed(0, cols + 1).forEach(x -> {
      sb.append(String.valueOf(x));
      sb.append(" ");
    });
    sb.append("\n");

    IntStream.rangeClosed(0, rows).forEach(y -> {
      // Row number
      sb.append(String.valueOf(y + 1));
      sb.append(" ");
      // Board
      IntStream.rangeClosed(0, cols).forEach(x -> {
        switch (board[y][x]) {
          case WALL_SYMBOL:
            if (isCorner(x, y)) {
              sb.append(CORNER_WALL_PRINT_SYMBOL);
            }
            if (isVerticalWall(x, y)) {
              sb.append(VERTICAL_WALL_PRINT_SYMBOL);
            } else if (isHorizontalWall(x, y)) {
              sb.append(HORIZONTAL_WALL_PRINT_SYMBOL);
            }
            break;
          case EXIT_SYMBOL:
            sb.append(EXIT_PRINT_SYMBOL);
            break;
          case EMPTY_SYMBOL:
            sb.append(EMPTY_PRINT_SYMBOL);
            break;
          case MAIN_CHIP_SYMBOL:
            sb.append(MAIN_CHIP_PRINT_SYMBOL);
            break;
          default:
            sb.append(board[y][x]);
        }
        sb.append(" ");
      });
      sb.append("\n");
    });
    return sb.toString();
  }

  private boolean isCorner(int x, int y) {
    return (y == 0 && x == 0) || (y == 0 && x == cols) || (y == rows && x == 0) || (y == rows && x == cols);
  }

  private boolean isVerticalWall(int x, int y) {
    return (x == 0 || x == cols) && (y != 0 && y != rows);
  }

  private boolean isHorizontalWall(int x, int y) {
    return (y == 0 || y == rows) && (x != 0 && x != cols);
  }
}
