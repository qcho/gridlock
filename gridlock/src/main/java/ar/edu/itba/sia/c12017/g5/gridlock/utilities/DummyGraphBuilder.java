package ar.edu.itba.sia.c12017.g5.gridlock.utilities;

import gps.GPSNode;

public class DummyGraphBuilder extends GraphBuilder {
  public DummyGraphBuilder() {
    super(null);
  }

  @Override
  public void add(GPSNode node) {
    // NOOP
  }

  @Override
  public String toString() {
    return "DummyGraphBuilder";
  }

  @Override
  public void writeToFile() {
    // NOOP
  }
}
