package ar.edu.itba.sia.c12017.g5.gridlock.models;

import edu.umd.cs.findbugs.annotations.SuppressFBWarnings;

import java.awt.Point;

@SuppressWarnings("checkstyle:membername")
@SuppressFBWarnings
public class Chip {
  public Boolean main;
  public Point start_position;
  public Point end_position;

  /**
   * Board chip
   * @param main true if the chip is the main one.
   * @param startPosition indicates where the chip starts.
   * @param endPosition indicates where the chip ends.
   */
  public Chip(Boolean main, Point startPosition, Point endPosition) {
    this.main = main;
    this.start_position = startPosition;
    this.end_position = endPosition;
  }

  public boolean isVertical() {
    return start_position.x == end_position.x;
  }

  public boolean isHorizontal() {
    return !isVertical();
  }
}
