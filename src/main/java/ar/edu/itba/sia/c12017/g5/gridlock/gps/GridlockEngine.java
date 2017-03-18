package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import gps.GpsEngine;
import gps.SearchStrategy;
import gps.api.GpsProblem;

public class GridlockEngine extends GpsEngine {
  public GridlockEngine(GpsProblem myProblem, SearchStrategy myStrategy) {
    super(myProblem, myStrategy);
  }
}
