package ar.edu.itba.sia.c12017.g5.gridlock.models;

import edu.umd.cs.findbugs.annotations.SuppressFBWarnings;

import java.awt.Point;

@SuppressWarnings({"checkstyle:membername", "checkstyle:parametername"})
@SuppressFBWarnings
public class Chip {
  private Boolean main;
  private Point start_position;
  private Point end_position;
  private Integer symbol;

  /**
   * Copy constructor.
   * @param other Chip to copy.
   */
  public Chip(Chip other) {
    this.main = other.isMain();
    this.start_position = other.getStartPosition();
    this.end_position = other.getEndPosition();
    this.symbol = other.getSymbol();
  }

  /**
   * Board chip
   * @param main true if the chip is the main one.
   * @param startPosition indicates where the chip starts.
   * @param endPosition indicates where the chip ends.
   */

  public Chip(Boolean main, Point startPosition, Point endPosition, Integer symbol) {
    this.main = main;
    this.start_position = startPosition;
    this.end_position = endPosition;
    this.symbol = symbol;
  }

  public boolean isVertical() {
    return start_position.x == end_position.x;
  }

  public boolean isHorizontal() {
    return !isVertical();
  }

  public Boolean isMain() {
    return main;
  }

  public Point getStartPosition() {
    return new Point(start_position);
  }

  public Point getEndPosition() {
    return new Point(end_position);
  }

  public Integer getSymbol() {
    return symbol;
  }

  public void setStartPosition(Point start_position) {
    this.start_position = start_position;
  }

  public void setEndPosition(Point end_position) {
    this.end_position = end_position;
  }
}
