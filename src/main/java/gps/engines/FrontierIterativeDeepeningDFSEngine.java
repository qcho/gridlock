package gps.engines;

import gps.GPSNode;
import gps.api.GPSProblem;

import java.util.LinkedList;
import java.util.List;

public class FrontierIterativeDeepeningDFSEngine extends DFSEngine {

  private long level = 0;
  private int levelStep;
  private List<GPSNode> frontier = new LinkedList<>();

  public FrontierIterativeDeepeningDFSEngine(GPSProblem problem, int levelStep) {
    super(problem);
    this.levelStep = levelStep;
  }

  @Override
  protected void explode(GPSNode node) {
    if (node.getCost() < level) {
      super.explode(node);
    } else if (node.getCost() == level) {
      frontier.add(node);
    }
    if (open.isEmpty()) {
      level += levelStep;
      open.clear();
      open.addAll(frontier);
    }
  }
}
