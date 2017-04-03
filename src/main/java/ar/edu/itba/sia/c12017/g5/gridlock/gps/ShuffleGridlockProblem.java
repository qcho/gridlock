package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import gps.SearchStrategy;
import gps.api.GPSRule;

import java.util.Collections;
import java.util.List;

public class ShuffleGridlockProblem extends GridlockProblem {
  public ShuffleGridlockProblem(GridlockState initState, SearchStrategy strategy) {
    super(initState, strategy);
  }

  @Override
  public List<GPSRule> getRules() {
    Collections.shuffle(rules);
    return rules;
  }
}
