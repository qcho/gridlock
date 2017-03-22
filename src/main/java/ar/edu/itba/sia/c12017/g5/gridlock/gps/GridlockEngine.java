package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import gps.GPSEngine;
import gps.SearchStrategy;
import gps.api.GPSProblem;

public class GridlockEngine extends GPSEngine {
  public GridlockEngine(GPSProblem myProblem, SearchStrategy myStrategy) {
    super(myProblem, myStrategy);
  }
}
