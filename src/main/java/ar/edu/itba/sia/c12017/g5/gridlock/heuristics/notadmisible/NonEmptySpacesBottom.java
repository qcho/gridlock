package ar.edu.itba.sia.c12017.g5.gridlock.heuristics.notadmisible;

import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockState;
import ar.edu.itba.sia.c12017.g5.gridlock.heuristics.Heuristic;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import gps.api.GPSState;

/**
 * Created by alebian on 29/03/17.
 */
public class NonEmptySpacesBottom extends Heuristic {
  /**
   * This heuristic checks how many empty spaces are in the bottom rectangle of the board.
   */
  @Override
  public Integer calculate(GPSState state) {
    Board board = ((GridlockState) state).getBoard();
    int[][] grid = board.getBoard();
    int count = 0;
    for (int x = 0; x < grid[0].length; x++) {
      for (int y = board.getExitY(); y < grid.length; y++) {
        if (grid[y][x] != Board.EMPTY_SYMBOL && grid[y][x] != Board.WALL_SYMBOL) {
          count++;
        }
      }
    }
    return count;
  }
}
