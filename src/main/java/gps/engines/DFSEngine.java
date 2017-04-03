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
    if (!isBest(node.getState(), node.getCost())) {
      return;
    }
    List<GPSNode> newCandidates = new ArrayList<>();
    addCandidates(node, newCandidates);
    for (GPSNode newNode : newCandidates) {
      ((LinkedList<GPSNode>) open).addFirst(newNode);
    }
  }
}
