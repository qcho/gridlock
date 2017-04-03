package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import ar.edu.itba.sia.c12017.g5.gridlock.heuristics.Heuristic;
import ar.edu.itba.sia.c12017.g5.gridlock.heuristics.admisible.FirstHeuristic;
import ar.edu.itba.sia.c12017.g5.gridlock.heuristics.admisible.SecondHeuristic;
import ar.edu.itba.sia.c12017.g5.gridlock.heuristics.admisible.ThirdHeuristic;
import ar.edu.itba.sia.c12017.g5.gridlock.heuristics.notadmisible.NonEmptySpacesTop;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Chip;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Movement;
import gps.SearchStrategy;
import gps.api.GPSProblem;
import gps.api.GPSRule;
import gps.api.GPSState;

import java.util.*;

public class GridlockProblem implements GPSProblem {
  private GridlockState initState;
  private SearchStrategy strategy;
  private List<GPSRule> rules;
  private List<Heuristic> nonAdmisibleHeuristics;
  private List<Heuristic> admisibleHeuristics;
  private List<Heuristic> allHeuristics;

  public GridlockProblem(GridlockState initState, SearchStrategy strategy) {
    this.initState = initState;
    this.strategy = strategy;
    this.rules = calculateRules();
    this.admisibleHeuristics = Arrays.asList(
            new FirstHeuristic(),
            new SecondHeuristic(),
            new ThirdHeuristic()
    );
    this.nonAdmisibleHeuristics = Arrays.asList(
//            new EmptySpacesTop(),
            new NonEmptySpacesTop()
    );
    this.allHeuristics = new ArrayList<>(admisibleHeuristics);
    allHeuristics.addAll(nonAdmisibleHeuristics);
  }

  private List<GPSRule> calculateRules() {
    List<Chip> chips = initState.getBoard().getChips();
    List<GPSRule> rules = new ArrayList<>();
    List<Movement> movements = Arrays.asList(Movement.values());
    chips.forEach(chip ->
      movements.forEach(movement ->
        rules.add(new GridlockRule(chip, movement))
      )
    );
    return rules;
  }

  @Override
  public GPSState getInitState() {
    return initState;
  }

  @Override
  public boolean isGoal(GPSState state) {
    return ((GridlockState) state).isGoal();
  }

  @Override
  public List<GPSRule> getRules() {
    return rules;
  }

  @Override
  public Integer getHValue(GPSState state) {
    if (isGoal(state)) {
      return 0;
    }

    Set<Integer> heuristicsValues = setForHeuristics();

    if (strategy.equals(SearchStrategy.GREEDY)) {
      allHeuristics.forEach(h -> heuristicsValues.add(h.calculate(state)));
    }
    else if (strategy.equals(SearchStrategy.ASTAR)) {
      admisibleHeuristics.forEach(h -> heuristicsValues.add(h.calculate(state)));
    }
    return heuristicsValues.iterator().next();
  }

  private Set<Integer> setForHeuristics() {
    if (strategy.equals(SearchStrategy.GREEDY)) {
      return new TreeSet<>();
    }
    return new TreeSet<>(Comparator.reverseOrder());
  }
}
