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
    if (node.getCost() <= level) {
      super.explode(node);
    }
    if (open.isEmpty()) {
      level++;
      open.clear();
      alreadyVisited.clear();
      open.add(new GPSNode(getProblem().getInitState(), 0, null));
    }
  }
}
