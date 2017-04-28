package ar.edu.itba.sia.c12017.g5.gridlock.heuristics.admisible;

import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockState;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Chip;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Movement;
import gps.api.GPSState;

import java.util.HashSet;
import java.util.Optional;
import java.util.Set;

public class ThirdHeuristic extends SecondHeuristic {

  Board board;
  Chip mainChip;
  Set<Integer> obstacles = new HashSet<>();
  int heuristicValue;

  /**
   * Checks how many obstacles are in between main and exit,
   * and afterwards checks for each of said obstacles
   * how many obstacles they need to move to clear the path.
   */
  @Override
  public Integer calculate(GPSState state) {
    GridlockState gs = (GridlockState) state;
    board = gs.getBoard();
    mainChip = board.getMainChip();
    Set<Integer> blockingChipsSet;
    heuristicValue = 0;

    if (mainChip.isVertical()) {
      if (board.getExitY() > mainChip.getEndPosition().y) {
        // Main chip needs to move DOWN
        blockingChipsSet = blockingChipsFor(mainChip, board, Movement.DOWN);
        heuristicValue = blockingChipsSet.size();
        if (blockingChipsSet.size() != 0) {
          blockingChipsSet.forEach(y -> checkBlockers(y, Movement.DOWN));
        }
      } else {
        // Main chip needs to move UP
        blockingChipsSet = blockingChipsFor(mainChip, board, Movement.UP);
        heuristicValue = blockingChipsSet.size();
        if (blockingChipsSet.size() != 0) {
          blockingChipsSet.forEach(y -> checkBlockers(y, Movement.UP));
        }
      }
    } else {
      if (board.getExitX() > mainChip.getEndPosition().x) {
        // Main chip needs to move RIGHT
        blockingChipsSet = blockingChipsFor(mainChip, board, Movement.RIGHT);
        heuristicValue = blockingChipsSet.size();
        if (blockingChipsSet.size() != 0) {
          blockingChipsSet.forEach(y -> checkBlockers(y, Movement.RIGHT));
        }
      } else {
        // Main chip needs to move LEFT
        blockingChipsSet = blockingChipsFor(mainChip, board, Movement.LEFT);
        heuristicValue = blockingChipsSet.size();
        if (blockingChipsSet.size() != 0) {
          blockingChipsSet.forEach(y -> checkBlockers(y, Movement.LEFT));
        }
      }
    }
    return heuristicValue;
  }

  /**
   * Movement stands for the movement the main chip must do,
   * so obstacles know what way they must move.
   */
  private void checkBlockers(Integer symbol, Movement movement) {
    int weight = 0;
    Optional<Integer> firstEffort;
    Optional<Integer> secondEffort;

    if (movement == Movement.RIGHT || movement == Movement.LEFT) {
      firstEffort = effortToFit(symbol, Movement.UP);
      //small optimization, ain't getting better than that
      if (firstEffort.isPresent() && firstEffort.get() == 0) {
        return;
      }
      secondEffort = effortToFit(symbol, Movement.DOWN);
    } else {
      firstEffort = effortToFit(symbol, Movement.LEFT);
      //small optimization, ain't getting better than that
      if (firstEffort.isPresent() && firstEffort.get() == 0) {
        return;
      }
      secondEffort = effortToFit(symbol, Movement.RIGHT);
    }
    if (firstEffort.isPresent()) {
      if (secondEffort.isPresent()) {
        weight = secondEffort.get() > firstEffort.get() ? firstEffort.get() : secondEffort.get();
      } else {
        weight = firstEffort.get();
      }
    } else {
      weight = secondEffort.get();
    }

    heuristicValue += weight;
  }

  private Optional<Integer> effortToFit(Integer symbol, Movement movement) {
    Chip chip = board.getChips().stream().filter(c -> c.getSymbol() == symbol).findAny().get();

    Optional<Integer> effort = Optional.empty();
    int cell;
    int chipLength;
    int countOfObstacles = 0;
    int movesToClear = 0;

    if (chip.isHorizontal()) {
      chipLength = chip.getEndPosition().x - chip.getStartPosition().x + 1;
    } else {
      chipLength = chip.getEndPosition().y - chip.getStartPosition().y + 1;
    }

    switch (movement) {
      case UP:
        if ((board.getRows() - 1) - mainChip.getStartPosition().y  >= chipLength) {
          int endsAtToFit = mainChip.getStartPosition().y + chipLength;
          for (int i = chip.getEndPosition().y + 1; i <= endsAtToFit ; i++) {
            movesToClear++;
            cell = board.getBoard()[chip.getStartPosition().x][i];
            if (cell != Board.EMPTY_SYMBOL) {
              if (!obstacles.contains(cell)) {
                obstacles.add(cell);
                countOfObstacles++;
              }
            }
          }
          effort = Optional.of(countOfObstacles + movesToClear);
        }
        break;

      case DOWN:
        if (mainChip.getStartPosition().y - 1 >= chipLength) {
          int startToFit = mainChip.getStartPosition().y - chipLength;
          for (int i = chip.getStartPosition().y - 1 ; i >= startToFit; i--) {
            movesToClear++;
            cell = board.getBoard()[chip.getStartPosition().x][i];
            if (cell != Board.EMPTY_SYMBOL) {
              if (!obstacles.contains(cell)) {
                obstacles.add(cell);
                countOfObstacles++;
              }
            }
          }
          effort = Optional.of(countOfObstacles + movesToClear);
        }
        break;

      case LEFT:
        if (mainChip.getStartPosition().x - 1 >= chipLength) {
          int startToFit = mainChip.getStartPosition().x - chipLength;
          for (int i = chip.getStartPosition().x - 1; i >= startToFit; i--) {
            movesToClear++;
            cell = board.getBoard()[i][chip.getStartPosition().y];
            if (cell != Board.EMPTY_SYMBOL) {
              if (!obstacles.contains(cell)) {
                obstacles.add(cell);
                countOfObstacles++;
              }
            }
          }
          effort = Optional.of(countOfObstacles + movesToClear);
        }
        break;

      case RIGHT:
        if ((board.getCols() - 1) - mainChip.getStartPosition().x >= chipLength) {
          int endsAtToFit = mainChip.getStartPosition().x + chipLength;
          for (int i = chip.getEndPosition().x + 1; i <= endsAtToFit; i++) {
            movesToClear++;
            cell = board.getBoard()[i][chip.getStartPosition().y];
            if (cell != Board.EMPTY_SYMBOL) {
              if (!obstacles.contains(cell)) {
                obstacles.add(cell);
                countOfObstacles++;
              }
            }
          }
          effort = Optional.of(countOfObstacles + movesToClear);
        }
        break;
      default:
        throw new IllegalArgumentException("Illegal move.");
    }
    return effort;
  }

}
