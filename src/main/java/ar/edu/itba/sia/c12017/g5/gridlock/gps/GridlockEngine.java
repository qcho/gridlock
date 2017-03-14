package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import gps.GPSEngine;
import gps.SearchStrategy;

/**
 * Created by alebian on 14/03/17.
 */
public class GridlockEngine extends GPSEngine {
    public GridlockEngine(SearchStrategy strategy) {
        this.strategy = strategy;
    }
}
