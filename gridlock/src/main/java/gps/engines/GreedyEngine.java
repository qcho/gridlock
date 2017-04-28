package gps.engines;

import gps.GPSEngine;
import gps.GPSNode;
import gps.api.GPSProblem;

import java.util.Comparator;
import java.util.PriorityQueue;

public class GreedyEngine extends GPSEngine {

  public GreedyEngine(GPSProblem problem) {
    super(problem);
    this.open = new PriorityQueue<>(
        Comparator.comparingInt(n -> getProblem().getHValue(n.getState()))
    );
  }

  @Override
  protected void explode(GPSNode node) {
    if (!isBest(node.getState(), node.getCost())) {
      return;
    }
    addCandidates(node, open);
  }
}
