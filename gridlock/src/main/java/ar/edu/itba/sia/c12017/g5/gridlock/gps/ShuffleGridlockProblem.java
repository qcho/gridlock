package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import ar.edu.itba.sia.c12017.g5.gridlock.models.Movement;
import gps.SearchStrategy;

import java.util.Collections;
import java.util.List;

public class ShuffleGridlockProblem extends GridlockProblem {
  public ShuffleGridlockProblem(GridlockState initState, SearchStrategy strategy) {
    super(initState, strategy);
  }

  @Override
  protected List<Movement> getMovements() {
    List<Movement> movements = super.getMovements();
    Collections.shuffle(movements);
    return movements;
  }
}
