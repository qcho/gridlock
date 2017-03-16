package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import gps.api.GPSState;

/**
 * Created by alebian on 14/03/17.
 */
public class GridlockState implements GPSState {
  private Board board;

  public GridlockState(Board board) {
    this.board = board;
  }

  public boolean isGoal() {
    return board.isGoal();
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;

    GridlockState that = (GridlockState) o;

    return board.equals(that.board);
  }

  @Override
  public int hashCode() {
    return board.hashCode();
  }
}
