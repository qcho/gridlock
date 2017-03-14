package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import gps.api.GPSProblem;
import gps.api.GPSRule;
import gps.api.GPSState;

import java.util.List;

/**
 * Created by alebian on 14/03/17.
 */
public class GridlockProblem implements GPSProblem {
    private GPSState initState;

    public GridlockProblem(GPSState initState) {
        this.initState = initState;
    }

    @Override
    public GPSState getInitState() {
        return initState;
    }

    @Override
    public boolean isGoal(GPSState state) {
        return false;
    }

    @Override
    public List<GPSRule> getRules() {
        return null;
    }

    @Override
    public Integer getHValue(GPSState state) {
        return null;
    }
}
