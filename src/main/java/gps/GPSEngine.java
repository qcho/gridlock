package gps;

import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockState;
import gps.api.GPSProblem;
import gps.api.GPSRule;
import gps.api.GPSState;

import java.util.*;

public class GPSEngine {

  private final Queue<GPSNode> open;
  private final Map<GPSState, Integer> alreadyVisited;
  private GPSProblem problem;
  private long explosionCounter;
  private boolean finished;
  private boolean failed;
  private GPSNode solutionNode;

  private final SearchStrategy strategy;

  public GPSEngine(GPSProblem myProblem, SearchStrategy myStrategy) {
    strategy = myStrategy;
    open = createQueue();
    alreadyVisited = new HashMap<>();
    problem = myProblem;
    explosionCounter = 0;
    finished = false;
    failed = false;
  }

  private Queue<GPSNode> createQueue() {
    if (strategy.equals(SearchStrategy.ASTAR) || strategy.equals(SearchStrategy.GREEDY)) {
      return new PriorityQueue<>();
    } else {
      return new LinkedList<>();
    }
  }

  public void findSolution() {
    GPSNode rootNode = new GPSNode(problem.getInitState(), 0);
    open.add(rootNode);
    // TODO: ¿Lógica de IDDFS?
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

  private void explode(GPSNode node) {
    Collection<GPSNode> newCandidates;
    switch (strategy) {
      case BFS:
        if (alreadyVisited.containsKey(node.getState())) {
          return;
        }
        newCandidates = new ArrayList<>();
        addCandidates(node, newCandidates);
        // TODO: Es correcto?
        open.addAll(newCandidates);
        break;
      case DFS:
        if (alreadyVisited.containsKey(node.getState())) {
          return;
        }
        newCandidates = new ArrayList<>();
        addCandidates(node, newCandidates);
//        // TODO: Es correcto?
//        LinkedList<GPSNode> list = new LinkedList<>();
//        list.addAll(newCandidates);
//        list.addAll(open);
//        open = list;
        break;
      case IDDFS:
        if (alreadyVisited.containsKey(node.getState())) {
          return;
        }
        newCandidates = new ArrayList<>();
        addCandidates(node, newCandidates);
        // TODO: ¿Cómo se agregan los nodos a open en IDDFS?
        break;
      case GREEDY:
        newCandidates = new PriorityQueue<>(/* TODO: Comparator! */);
        addCandidates(node, newCandidates);
        // TODO: ¿Cómo se agregan los nodos a open en GREEDY?
        break;
      case ASTAR:
        if (!isBest(node.getState(), node.getCost())) {
          return;
        }
        newCandidates = new ArrayList<>();
        addCandidates(node, newCandidates);
        // TODO: ¿Cómo se agregan los nodos a open en A*?
        break;
    }
  }

  private void addCandidates(GPSNode node, Collection<GPSNode> candidates) {
    explosionCounter++;
    updateBest(node);
    System.out.println(node.getState());
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

  public SearchStrategy getStrategy() {
    return strategy;
  }

}
