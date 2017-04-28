package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.utilities.BoardParser;
import gps.api.GPSState;

import java.nio.file.Paths;

public class GridlockState implements GPSState {
  public Board board;

  public GridlockState(Board board) {
    this.board = board;
  }

  public boolean isGoal() {
    return board.isGoal();
  }

  @Override
  public boolean equals(Object other) {
    if (this == other) {
      return true;
    }
    if (other == null || getClass() != other.getClass()) {
      return false;
    }
    return board.equals(((GridlockState) other).board);
  }

  @Override
  public int hashCode() {
    return board.hashCode();
  }

  public Board getBoard() {
    return board;
  }

  @Override
  public String toString() {
    return board.toString();
  }
}
