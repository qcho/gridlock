package ar.edu.itba.sia.c12017.g5.gridlock.gps;

import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Chip;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Movement;
import gps.api.GPSProblem;
import gps.api.GPSRule;
import gps.api.GPSState;

import java.util.*;
import java.util.stream.IntStream;

public class GridlockProblem implements GPSProblem {
  private GridlockState initState;
  private List<GPSRule> rules;

  public GridlockProblem(GridlockState initState) {
    this.initState = initState;
    this.rules = calculateRules();
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
    Set<Integer> heuristics = new TreeSet<>(Comparator.reverseOrder());
    heuristics.add(firstHeuristic(state));
    heuristics.add(secondHeuristic(state));
    heuristics.add(thirdHeuristic(state));
    return heuristics.iterator().next();
  }

  // Naive heuristic, it only checks how many blocks are between the main chip and exit
  private Integer firstHeuristic(GPSState state) {
    GridlockState gs = (GridlockState)state;
    Board board = gs.getBoard();
    Chip mainChip = board.getMainChip();
    int[][] grid = board.getBoard();

    int chipsBetweenGoal = 0;
    if (mainChip.isVertical()) {
      if (board.getExitY() > mainChip.getEndPosition().y) {
        // Main chip needs to move DOWN
        for (int i = mainChip.getEndPosition().y; i < board.getExitY(); i++) {
          int cell = grid[i][mainChip.getEndPosition().x];
          if (isAnotherChip(cell)) {
            chipsBetweenGoal++;
          }
        }
      } else {
        // Main chip needs to move UP
        for (int i = mainChip.getStartPosition().y; i > board.getExitY(); i--) {
          int cell = grid[i][mainChip.getEndPosition().x];
          if (isAnotherChip(cell)) {
            chipsBetweenGoal++;
          }
        }
      }
    } else {
      if (board.getExitX() > mainChip.getEndPosition().x) {
        // Main chip needs to move RIGHT
        for (int i = mainChip.getEndPosition().x; i < board.getExitX(); i++) {
          int cell = grid[mainChip.getEndPosition().y][i];
          if (isAnotherChip(cell)) {
            chipsBetweenGoal++;
          }
        }
      } else {
        // Main chip needs to move LEFT
        for (int i = mainChip.getStartPosition().x; i > board.getExitX(); i--) {
          int cell = grid[mainChip.getEndPosition().y][i];
          if (isAnotherChip(cell)) {
            chipsBetweenGoal++;
          }
        }
      }
    }
    return chipsBetweenGoal;
  }

  private Integer secondHeuristic(GPSState state) {
    return 2;
  }

  private Integer thirdHeuristic(GPSState state) {
    return 3;
  }

  private boolean isAnotherChip(Integer symbol) {
    switch (symbol) {
      case Board.MAIN_CHIP_SYMBOL:
      case Board.EMPTY_SYMBOL:
      case Board.EXIT_SYMBOL:
      case Board.WALL_SYMBOL:
        return false;
      default:
        return true;
    }
  }
}
