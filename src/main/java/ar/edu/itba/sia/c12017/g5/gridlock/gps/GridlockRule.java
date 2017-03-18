package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import gps.api.GpsRule;
import gps.api.GpsState;
import gps.exception.NotApplicableException;

public class GridlockRule implements GpsRule {
  @Override
  public Integer getCost() {
    return null;
  }

  @Override
  public String getName() {
    return null;
  }

  @Override
  public GpsState evalRule(GpsState state) throws NotApplicableException {
    return null;
  }
}
