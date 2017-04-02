package ar.edu.itba.sia.c12017.g5.gridlock.heuristics.admisible;

import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockState;
import ar.edu.itba.sia.c12017.g5.gridlock.heuristics.Heuristic;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Chip;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Movement;
import gps.api.GPSState;

import java.awt.Point;

/**
 * Created by alebian on 27/03/17.
 */
public class NaiveHeuristic extends Heuristic {
  /**
   * Naive heuristic, it only checks how many blocks are between the main chip and exit.
   */
  @Override
  public Integer calculate(GPSState state) {
    GridlockState gs = (GridlockState)state;
    Board board = gs.getBoard();
    Chip mainChip = board.getMainChip();
    Point exitPosition = board.getExitPoint();

    int chipsBetweenGoal = 0;
    if (mainChip.isVertical()) {
      if (isLower(exitPosition, mainChip.getEndPosition())) {
        // Main chip needs to move DOWN
        chipsBetweenGoal += blockingChipsFor(mainChip, board, Movement.DOWN).size();
      } else {
        // Main chip needs to move UP
        chipsBetweenGoal += blockingChipsFor(mainChip, board, Movement.UP).size();
      }
    } else {
      if (isToTheRight(exitPosition, mainChip.getEndPosition())) {
        // Main chip needs to move RIGHT
        chipsBetweenGoal += blockingChipsFor(mainChip, board, Movement.RIGHT).size();
      } else {
        // Main chip needs to move LEFT
        chipsBetweenGoal += blockingChipsFor(mainChip, board, Movement.LEFT).size();
      }
    }
    return chipsBetweenGoal;
  }
}
