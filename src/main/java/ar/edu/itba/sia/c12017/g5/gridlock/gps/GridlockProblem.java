package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import ar.edu.itba.sia.c12017.g5.gridlock.heuristics.BlockingChipsMovementHeuristic;
import ar.edu.itba.sia.c12017.g5.gridlock.heuristics.Heuristic;
import ar.edu.itba.sia.c12017.g5.gridlock.heuristics.NaiveHeuristic;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Chip;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Movement;
import gps.api.GPSProblem;
import gps.api.GPSRule;
import gps.api.GPSState;

import java.util.*;

public class GridlockProblem implements GPSProblem {
  private GridlockState initState;
  private List<GPSRule> rules;
  private List<Heuristic> heuristics;

  public GridlockProblem(GridlockState initState) {
    this.initState = initState;
    this.rules = calculateRules();
    this.heuristics = Arrays.asList(
      new NaiveHeuristic(),
      new BlockingChipsMovementHeuristic()
    );
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
    Set<Integer> heuristicsValues = new TreeSet<>(Comparator.reverseOrder());
    heuristics.forEach(h -> heuristicsValues.add(h.calculate(state)));
    return heuristicsValues.iterator().next();
  }
}
