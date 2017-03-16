package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import gps.GPSEngine;
import gps.SearchStrategy;
import gps.api.GPSProblem;

/**
 * Created by alebian on 14/03/17.
 */
public class GridlockEngine extends GPSEngine {
    public GridlockEngine(GPSProblem myProblem, SearchStrategy myStrategy) {
        super(myProblem, myStrategy);
    }
}
