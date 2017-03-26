package gps;

import gps.api.GPSProblem;
import gps.api.GPSRule;
import gps.api.GPSState;
import gps.engines.BFSEngine;
import gps.engines.DFSEngine;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.Optional;
import java.util.PriorityQueue;
import java.util.Queue;

public abstract class GPSEngine {
  protected Queue<GPSNode> open;
  protected Map<GPSState, Integer> alreadyVisited;
  private GPSProblem problem;
  private long explosionCounter;
  private boolean finished;
  private boolean failed;
  private GPSNode solutionNode;

  public static GPSEngine build(GPSProblem problem, SearchStrategy strategy) {
    switch (strategy) {
      case BFS:
        return new BFSEngine(problem);
      case DFS:
        return new DFSEngine(problem);
      case IDDFS:
        return null;
      case ASTAR:
        return null;
      case GREEDY:
        return null;
      default:
        return null;
    }
  }

  public GPSEngine(GPSProblem problem) {
    this.problem = problem;
    this.alreadyVisited = new HashMap<>();
    this.explosionCounter = 0;
    this.finished = false;
    this.failed = false;
  }

  public void findSolution() {
    GPSNode rootNode = new GPSNode(problem.getInitState(), 0);
    open.add(rootNode);
    while (open.size() > 0) {
      GPSNode currentNode = open.remove();
      if (problem.isGoal(currentNode.getState())) {
        finished = true;
        solutionNode = currentNode;
        return;
      } else {
        explode(currentNode);
      }
    }
    failed = true;
    finished = true;
  }

  protected abstract void explode(GPSNode node);

//  protected void explode(GPSNode node) {
//    Collection<GPSNode> newCandidates;
//    switch (strategy) {
//      case IDDFS:
//        if (alreadyVisited.containsKey(node.getState())) {
//          return;
//        }
//        newCandidates = new ArrayList<>();
//        addCandidates(node, newCandidates);
//        // TODO: ¿Cómo se agregan los nodos a open en IDDFS?
//        break;
//      case GREEDY:
//        newCandidates = new PriorityQueue<>(/* TODO: Comparator! */);
//        addCandidates(node, newCandidates);
//        // TODO: ¿Cómo se agregan los nodos a open en GREEDY?
//        break;
//      case ASTAR:
//        if (!isBest(node.getState(), node.getCost())) {
//          return;
//        }
//        newCandidates = new ArrayList<>();
//        addCandidates(node, newCandidates);
//        // TODO: ¿Cómo se agregan los nodos a open en A*?
//        break;
//    }
//  }

  protected void addCandidates(GPSNode node, Collection<GPSNode> candidates) {
    explosionCounter++;
    updateBest(node);
    for (GPSRule rule : problem.getRules()) {
      Optional<GPSState> newState = rule.evalRule(node.getState());
      newState.ifPresent(state -> {
        GPSNode newNode = new GPSNode(state, node.getCost() + rule.getCost());
        newNode.setParent(node);
        candidates.add(newNode);
      });
    }
  }

  private boolean isBest(GPSState state, Integer cost) {
    return !alreadyVisited.containsKey(state) || cost < alreadyVisited.get(state);
  }

  private void updateBest(GPSNode node) {
    alreadyVisited.put(node.getState(), node.hashCode());
  }

  public Queue<GPSNode> getOpen() {
    return open;
  }

  public Map<GPSState, Integer> getAlreadyVisited() {
    return alreadyVisited;
  }

  public GPSProblem getProblem() {
    return problem;
  }

  public long getExplosionCounter() {
    return explosionCounter;
  }

  public boolean isFinished() {
    return finished;
  }

  public boolean isFailed() {
    return failed;
  }

  public GPSNode getSolutionNode() {
    return solutionNode;
  }

}
