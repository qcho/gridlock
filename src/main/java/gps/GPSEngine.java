package gps;

import gps.api.GPSProblem;
import gps.api.GPSRule;
import gps.api.GPSState;
import org.pmw.tinylog.Logger;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.Queue;

public abstract class GPSEngine {
  protected Queue<GPSNode> open;
  protected Map<GPSState, Integer> alreadyVisited;
  private GPSProblem problem;
  private long explosionCounter;
  private long candidatesCounter;
  private boolean finished;
  private boolean failed;
  private GPSNode solutionNode;

  public GPSEngine(GPSProblem problem) {
    this.problem = problem;
    this.alreadyVisited = new HashMap<>();
    this.explosionCounter = 0;
    this.candidatesCounter = 0;
    this.finished = false;
    this.failed = false;
  }

  public void findSolution() {
    GPSNode rootNode = new GPSNode(problem.getInitState(), 0, null);
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

  protected void addCandidates(GPSNode node, Collection<GPSNode> candidates) {
    explosionCounter++;
    updateBest(node);
    for (GPSRule rule : problem.getRules()) {
      Optional<GPSState> newState = rule.evalRule(node.getState());
      newState.ifPresent(state -> {
        int cost = node.getCost() + rule.getCost();
        if (!isBest(state, cost)) {
          return;
        }
        GPSNode newNode = new GPSNode(state, cost, rule);
        newNode.setParent(node);
        candidates.add(newNode);
      });
      candidatesCounter += candidates.size();
    }
  }

  public long getCandidatesCounter() {
    return candidatesCounter;
  }

  protected boolean isBest(GPSState state, Integer cost) {
    return !alreadyVisited.containsKey(state) || cost < alreadyVisited.get(state);
  }

  protected void updateBest(GPSNode node) {
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
