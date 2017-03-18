package ar.edu.itba.sia.c12017.g5.gridlock.models;

import java.awt.*;

/**
 * Created by alebian on 3/18/17.
 */
public class Chip {
  public Boolean main;
  public Point start_position;
  public Point end_position;

  public Chip(Boolean main, Point start_position, Point end_position) {
    this.main = main;
    this.start_position = start_position;
    this.end_position = end_position;
  }

  public boolean isVertical() {
    return start_position.x == end_position.x;
  }

  public boolean isHorizontal() {
    return start_position.y == end_position.y;
  }
}
