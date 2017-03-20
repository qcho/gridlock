package gps;

import gps.api.GpsProblem;
import gps.api.GpsRule;
import gps.api.GpsState;
import gps.exception.NotAppliableException;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Queue;
import java.util.TreeSet;


public abstract class GpsEngine {

  protected Queue<GpsNode> open;
  protected Map<GpsState, Integer> bestCosts;

  protected GpsProblem problem;
  private long explosionCounter;

  // Use this variable in open set order.
  protected SearchStrategy strategy;

  /**
   * TODO
   * @param myProblem Problem to solve.
   * @param myStrategy Strategy for problem resolution.
   */
  public GpsEngine(GpsProblem myProblem, SearchStrategy myStrategy) {
    // TODO: Cambiar la Queue de open por algo que nos sirva. Puse PQ por ahora.
    open = new PriorityQueue<>();
    bestCosts = new HashMap<>();
    problem = myProblem;
    strategy = myStrategy;

    GpsNode rootNode = new GpsNode(problem.getInitState(), 0);
    explosionCounter = 0;
    boolean finished = false;
    boolean failed = false;
    open.add(rootNode);
    // TODO: ¿Lógica de IDDFS?
    while (!failed && !finished) {
      if (open.size() <= 0) {
        failed = true;
      } else {
        GpsNode currentNode = open.remove();
        if (problem.isGoal(currentNode.getState())) {
          finished = true;
          System.out.println(currentNode.getSolution());
          System.out.println("Expanded nodes: " + explosionCounter);
          System.out.println("Solution cost: " + currentNode.getCost());
        } else {
          explode(currentNode);
        }
      }
    }
    if (finished) {
      System.out.println("OK! solution found!");
    } else if (failed) {
      System.err.println("FAILED! solution not found!");
    }
  }

  private void explode(GpsNode node) {
    Collection<GpsNode> newCandidates;
    switch (strategy) {
      case ASTAR:
        if (!isBest(node.getState(), node.getCost())) {
          return;
        }
        newCandidates = new ArrayList<>();
        break;
      case BFS:
      case DFS:
      case IDDFS:
        if (bestCosts.containsKey(node.getState())) {
          return;
        }
        newCandidates = new ArrayList<>();
        break;
      case GREEDY:
        newCandidates = new TreeSet<>(/* TODO: Comparator! */);
        break;
      default:
        newCandidates = new ArrayList<>();
    }
    explosionCounter++;
    updateBest(node);
    for (GpsRule rule : problem.getRules()) {
      try {
        GpsNode newNode = new GpsNode(rule.evalRule(node.getState()),
                node.getCost() + rule.getCost());
        newNode.setParent(node);
        newCandidates.add(newNode);
      } catch (NotAppliableException exception) {
        // Si no es aplicable, se saltea.
      }
    }
    // TODO: ¿Cómo se agregan los nodos en las diferentes estrategias?
    switch (strategy) {
      case ASTAR:
        break;
      case BFS:
        break;
      case DFS:
        break;
      case IDDFS:
        break;
      case GREEDY:
        break;
      default:
        throw new IllegalArgumentException("Illegal strategy provided: " + strategy);
    }
  }

  private boolean isBest(GpsState state, Integer cost) {
    return !bestCosts.containsKey(state) || cost < bestCosts.get(state);
  }

  private void updateBest(GpsNode node) {
    bestCosts.put(node.getState(), node.getCost());
  }

}
