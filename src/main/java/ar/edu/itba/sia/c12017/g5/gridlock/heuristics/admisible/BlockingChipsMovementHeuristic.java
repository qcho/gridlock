package ar.edu.itba.sia.c12017.g5.gridlock.heuristics.admisible;

import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockState;
import ar.edu.itba.sia.c12017.g5.gridlock.heuristics.Heuristic;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Chip;
import gps.api.GPSState;

/**
 * Created by alebian on 27/03/17.
 */
public class BlockingChipsMovementHeuristic extends Heuristic {
  /**
   * This heuristic is the next step of the naive one. After finding the blocking chips,
   * we calculate how many movements they would need to unblock the chip if the rest of
   * the board was empty.
   */
  @Override
  public Integer calculate(GPSState state) {
    GridlockState gs = (GridlockState) state;
    Board board = gs.getBoard();
    Chip mainChip = board.getMainChip();
    int[][] grid = board.getBoard();

    int chipsBetweenGoal = 0;
    if (mainChip.isVertical()) {
      if (board.getExitY() > mainChip.getEndPosition().y) {
        // Main chip needs to move DOWN
        for (int i = mainChip.getEndPosition().y; i < board.getExitY(); i++) {
          int cell = grid[i][mainChip.getEndPosition().x];
          if (isAnotherChip(cell)) {
            chipsBetweenGoal++;
          }
        }
      } else {
        // Main chip needs to move UP
        for (int i = mainChip.getStartPosition().y; i > board.getExitY(); i--) {
          int cell = grid[i][mainChip.getEndPosition().x];
          if (isAnotherChip(cell)) {
            chipsBetweenGoal++;
          }
        }
      }
    } else {
      if (board.getExitX() > mainChip.getEndPosition().x) {
        // Main chip needs to move RIGHT
        for (int i = mainChip.getEndPosition().x; i < board.getExitX(); i++) {
          int cell = grid[mainChip.getEndPosition().y][i];
          if (isAnotherChip(cell)) {
            chipsBetweenGoal++;
          }
        }
      } else {
        // Main chip needs to move LEFT
        for (int i = mainChip.getStartPosition().x; i > board.getExitX(); i--) {
          int cell = grid[mainChip.getEndPosition().y][i];
          if (isAnotherChip(cell)) {
            chipsBetweenGoal++;
          }
        }
      }
    }
    return chipsBetweenGoal;
  }
}
