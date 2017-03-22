package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Chip;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Movement;
import gps.api.GPSRule;
import gps.api.GPSState;
import gps.exception.NotAppliableException;

public class GridlockRule implements GPSRule {
  private Chip chip;
  private Movement movement;

  public GridlockRule(Chip chip, Movement movement) {
    this.chip = chip;
    this.movement = movement;
  }

  @Override
  public Integer getCost() {
    return 1;
  }

  @Override
  public String getName() {
    return String.format("Moving chip %d %s", chip.getSymbol(), movement.toString());
  }

  @Override
  public GPSState evalRule(GPSState state) throws NotAppliableException {
    Board newBoard = ((GridlockState) state).board.applyMovement(chip, movement);
    if (newBoard == null) {
      throw new NotAppliableException();
    }
    return new GridlockState(newBoard);
  }
}
