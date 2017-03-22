package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Chip;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Movement;
import gps.api.GPSRule;
import gps.api.GPSState;

import java.util.Optional;

public class GridlockRule implements GPSRule {
  private Integer symbol;
  private Movement movement;

  public GridlockRule(Chip chip, Movement movement) {
    this.symbol = chip.getSymbol();
    this.movement = movement;
  }

  @Override
  public Integer getCost() {
    return 1;
  }

  @Override
  public String getName() {
    return String.format("Moving chip %d %s", symbol, movement.toString());
  }

  @Override
  public Optional<GPSState> evalRule(GPSState state) {
    Board newBoard = ((GridlockState) state).board.applyMovement(symbol, movement);
    if (newBoard == null) {
      return Optional.empty();
    }
    return Optional.of(new GridlockState(newBoard));
  }
}
