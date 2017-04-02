package ar.edu.itba.sia.c12017.g5.gridlock.heuristics.notadmisible;

import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockState;
import ar.edu.itba.sia.c12017.g5.gridlock.heuristics.Heuristic;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import gps.api.GPSState;

/**
 * Created by alebian on 29/03/17.
 */
public class NonEmptySpacesTop extends Heuristic {
  /**
   * This heuristic checks how many empty spaces are in the top rectangle of the board.
   * Greedy algorithm will choose boards with the lowest H values, this means that
   * it will try to clear the spaces in the top of the board.
   */
  @Override
  public Integer calculate(GPSState state) {
    Board board = ((GridlockState) state).getBoard();
    int[][] grid = board.getBoard();
    int count = 0;

    int startY = calculateStartY(board);
    int endY = calculateEndY(board);

    for (int x = 0; x < grid[0].length; x++) {
      for (int y = startY; y <= endY; y++) {
        if (grid[y][x] != Board.EMPTY_SYMBOL && grid[y][x] != Board.WALL_SYMBOL) {
          count++;
        }
      }
    }
    return count;
  }

  private static int calculateStartY(final Board board) {
    int middleBoard = calculateMiddle(board);
    if (board.getExitY() > middleBoard) {
      return middleBoard + 1;
    } else {
      return 0;
    }
  }

  private static int calculateEndY(final Board board) {
    int middleBoard = calculateMiddle(board);
    if (board.getExitY() > middleBoard) {
      return board.getBoard().length;
    } else {
      return board.getExitY();
    }
  }

  private static int calculateMiddle(final Board board) {
    return Math.floorDiv(board.getBoard().length - 1, 2);
  }
}
