package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import gps.api.GPSRule;
import gps.api.GPSState;
import gps.exception.NotAppliableException;

/**
 * Created by alebian on 14/03/17.
 */
public class GridlockRule implements GPSRule {
  @Override
  public Integer getCost() {
    return null;
  }

  @Override
  public String getName() {
    return null;
  }

  @Override
  public GPSState evalRule(GPSState state) throws NotAppliableException {
    return null;
  }
}
