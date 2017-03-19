package ar.edu.itba.sia.c12017.g5.gridlock.models;

/**
 * Created by alebian on 3/18/17.
 */
public enum Movement {
  UP(0, -1),
  DOWN(0, 1),
  LEFT(-1, 0),
  RIGHT(1, 0);

  public final int horizontalMovement;
  public final int verticalMovement;

  Movement(int horizontalMovement, int verticalMovement) {
    this.horizontalMovement = horizontalMovement;
    this.verticalMovement = verticalMovement;
  }
}
