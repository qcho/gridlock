package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import gps.api.GPSProblem;
import gps.api.GPSRule;
import gps.api.GPSState;

import java.util.List;

public class GridlockProblem implements GPSProblem {
  private GridlockState initState;

  public GridlockProblem(GridlockState initState) {
    this.initState = initState;
  }

  @Override
  public GPSState getInitState() {
    return initState;
  }

  @Override
  public boolean isGoal(GPSState state) {
    return ((GridlockState) state).isGoal();
  }

  @Override
  public List<GPSRule> getRules() {
    // Ordenar las reglas por H-Value.
    return null;
  }

  @Override
  public Integer getHValue(GPSState state) {
    return null;
  }
}
