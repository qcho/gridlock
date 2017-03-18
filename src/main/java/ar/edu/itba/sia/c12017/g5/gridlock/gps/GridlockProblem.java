package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import gps.api.GpsProblem;
import gps.api.GpsRule;
import gps.api.GpsState;

import java.util.List;

public class GridlockProblem implements GpsProblem {
  private GpsState initState;

  public GridlockProblem(GpsState initState) {
    this.initState = initState;
  }

  @Override
  public GpsState getInitState() {
    return initState;
  }

  @Override
  public boolean isGoal(GpsState state) {
    return ((GridlockState)state).isGoal();
  }

  @Override
  public List<GpsRule> getRules() {
    return null;
  }

  @Override
  public Integer getHValue(GpsState state) {
    return null;
  }
}
