package gps.engines;

import gps.GPSEngine;
import gps.GPSNode;
import gps.api.GPSProblem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;

public class DFSEngine extends GPSEngine {
  public DFSEngine(GPSProblem problem) {
    super(problem);
    this.open = new LinkedList<>();

  }

  @Override
  protected void explode(GPSNode node) {
    if (alreadyVisited.containsKey(node.getState())) {
      return;
    }
    List<GPSNode> newCandidates = new ArrayList<>();
    addCandidates(node, newCandidates);
    Collections.reverse((ArrayList) newCandidates);
    LinkedList<GPSNode> list = new LinkedList<>();
    list.addAll(newCandidates);
    list.addAll(open);
    open = list;
  }
}
