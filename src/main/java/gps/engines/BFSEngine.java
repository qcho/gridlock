package gps.engines;

import gps.GPSEngine;
import gps.GPSNode;
import gps.api.GPSProblem;

import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedList;

/**
 * Created by alebian on 3/25/17.
 */
public class BFSEngine extends GPSEngine {
  public BFSEngine(GPSProblem problem) {
    super(problem);
    this.open = new LinkedList<>();

  }

  @Override
  protected void explode(GPSNode node) {
    Collection<GPSNode> newCandidates;
    if (alreadyVisited.containsKey(node.getState())) {
      return;
    }
    newCandidates = new ArrayList<>();
    addCandidates(node, newCandidates);
    open.addAll(newCandidates);
  }
}
