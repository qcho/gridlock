package ar.edu.itba.sia.c12017.g5.gridlock.models;

import java.awt.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.stream.IntStream;

/*
* The board has sentinel cells around the actual game grid.
* The board positions are interpreted as:
*    (x = 1, y = 1) +-----+-----+-----+ (y = 1, x = cols)
*                   |     |     |     |
*                   +-----+-----+-----+
*                   |     |     |     |
*                   +-----+-----+-----+
*                   |     |     |     |
* (y = rows, x = 1) +-----+-----+-----+ (rows, cols)
* */
@SuppressWarnings("checkstyle:parametername")
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

  private Chip mainChip;
  private List<Chip> chips;

  /**
   * Builds a board of the given dimensions with the given exit.
   * @param rows amount of rows in the board
   * @param cols amount of columns in the board
   * @param exitX exit x-position
   * @param exitY exit y-position
   */
  public Board(int rows, int cols, int exitX, int exitY) {
    this.rows = rows + 1;
    this.cols = cols + 1;
    this.exitX = exitX;
    this.exitY = exitY;
    chips = new ArrayList<>();
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

  /**
   * Compares another object to this board.
   * @param other object to compare.
   * @return true if other is a board and with my same contents.
   */
  @Override
  public boolean equals(Object other) {
    if (this == other) {
      return true;
    }
    if (other == null || getClass() != other.getClass()) {
      return false;
    }
    return Arrays.deepEquals(board, ((Board) other).board);
  }

  @Override
  public int hashCode() {
    return Arrays.deepHashCode(board);
  }

  /**
   * Adds a new chip to the board.
   * @param main indicates if it is the main chip. Only one should exist.
   * @param sx x-position for the beginning of the chip.
   * @param sy y-position for the beginning of the chip.
   * @param ex x-position for the end of the chip.
   * @param ey y-position for the end of the chip.
   */
  public void addChip(final boolean main, final int sx, final int sy, final int ex, final int ey) {
    int symbol = main ? MAIN_CHIP_SYMBOL : nextChip;
    Chip chip = new Chip(main, new Point(sx, sy), new Point(ex, ey));
    if (chip.start_position.x == chip.end_position.x) {
      assert (chip.start_position.y < chip.end_position.y);
      // VERTICAL CHIP
      IntStream.rangeClosed(chip.start_position.y, chip.end_position.y).forEach(y -> board[y][chip.start_position.x] = symbol);
    } else if (chip.start_position.y == chip.end_position.y) {
      assert (chip.start_position.x < chip.end_position.x);
      // HORIZONTAL CHIP
      IntStream.rangeClosed(chip.start_position.x, chip.end_position.x).forEach(x -> board[chip.start_position.y][x] = symbol);
    } else {
      throw new IllegalArgumentException("Cannot insert diagonal chips");
    }
    chips.add(chip);
    if (!main) {
      nextChip++;
    } else {
      if (mainChip != null) {
        throw new IllegalArgumentException("Only one main chip is allowed");
      }
      if (!chipCanScape(chip)) {
        throw new IllegalArgumentException("The main chip can't scape from this board!");
      }
      mainChip = chip;
    }
  }

  private boolean chipCanScape(Chip chip) {
    if (chip.isHorizontal()) {
      return chip.end_position.y == exitY;
    } else {
      return chip.end_position.x == exitX;
    }
  }

  /**
   * Indicates whether the current board configuration is a solution.
   * @return true if current board has a goal configuration.
   */
  public boolean isGoal() {
    if (mainChip.isHorizontal()) {
      for (int x = mainChip.end_position.x; x < exitX; x++) {
        int symbol = board[mainChip.end_position.y][x];
        if (symbol != MAIN_CHIP_SYMBOL && symbol != EMPTY_SYMBOL) {
          return false;
        }
      }
    } else {
      for (int y = mainChip.end_position.y; y < exitY; y++) {
        int symbol = board[y][mainChip.end_position.x];
        if (symbol != MAIN_CHIP_SYMBOL && symbol != EMPTY_SYMBOL) {
          return false;
        }
      }
    }
    return true;
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
    IntStream.rangeClosed(0, cols).forEach(x -> {
      sb.append(x < 2 ? " " : x - 2);
      sb.append(" ");
    });
    sb.append("\n");

    IntStream.rangeClosed(0, rows).forEach(y -> {
      // Row number
      if (y < rows) {
        sb.append(y < 1 ? " " : y - 1);
        sb.append(" ");
      } else {
        sb.append("  ");
      }
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
    return (y == 0 && x == 0) || (y == 0 && x == cols)
            || (y == rows && x == 0) || (y == rows && x == cols);
  }

  private boolean isVerticalWall(int x, int y) {
    return (x == 0 || x == cols) && (y != 0 && y != rows);
  }

  private boolean isHorizontalWall(int x, int y) {
    return (y == 0 || y == rows) && (x != 0 && x != cols);
  }

  public Chip getMainChip() {
    return mainChip;
  }
}
