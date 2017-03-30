package gps.engines;

import gps.GPSNode;
import gps.api.GPSProblem;

public class IterativeDeepeningDFSEngine extends DFSEngine {

  private long level = 0;

  public IterativeDeepeningDFSEngine(GPSProblem problem) {
    super(problem);
  }

  @Override
  protected void explode(GPSNode node) {
    if (node.getCost() >= level) {
      level += 1;
      alreadyVisited.clear();
      open.add(new GPSNode(getProblem().getInitState(), 0));
    }
    super.explode(node);
  }
}
