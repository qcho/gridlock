package ar.edu.itba.sia.c12017.g5.gridlock.heuristics;

import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Chip;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Movement;
import gps.api.GPSState;

import java.awt.Point;
import java.util.HashSet;
import java.util.Set;

public abstract class Heuristic {
  public abstract Integer calculate(GPSState state);

  protected static boolean isAnotherChip(Integer symbol) {
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

  protected static Set<Integer> blockingChipsFor(Chip chip, Board board, Movement movement) {
    Set<Integer> answer = new HashSet<>();

    int[][] grid = board.getBoard();
    Point startPosition = chip.getStartPosition();
    Point endPosition = chip.getEndPosition();
    Point exitPosition = board.getExitPoint();

    if (chip.isVertical()) {
      if (movement.equals(Movement.UP)) {
        if (isUpper(exitPosition, endPosition)) {
          for (int i = startPosition.y; i > board.getExitY(); i--) {
            int cell = grid[i][endPosition.x];
            if (isAnotherChip(cell)) {
              answer.add(cell);
            }
          }
        }
      } else if (movement.equals(Movement.DOWN)) {
        if (isLower(exitPosition, endPosition)) {
          for (int i = endPosition.y; i < board.getExitY(); i++) {
            int cell = grid[i][endPosition.x];
            if (isAnotherChip(cell)) {
              answer.add(cell);
            }
          }
        }
      }
    } else {
      if (movement.equals(Movement.LEFT)) {
        if (isToTheLeft(exitPosition, endPosition)) {
          for (int i = startPosition.x; i > board.getExitX(); i--) {
            int cell = grid[endPosition.y][i];
            if (isAnotherChip(cell)) {
              answer.add(cell);
            }
          }
        }
      } else if (movement.equals(Movement.RIGHT)) {
        if (isToTheRight(exitPosition, endPosition)) {
          for (int i = endPosition.x; i < board.getExitX(); i++) {
            int cell = grid[endPosition.y][i];
            if (isAnotherChip(cell)) {
              answer.add(cell);
            }
          }
        }
      }
    }
    return answer;
  }

  protected static boolean isToTheRight(Point p1, Point p2) {
    return p1.x > p2.x;
  }

  protected static boolean isToTheLeft(Point p1, Point p2) {
    return p1.x <= p2.x;
  }

  protected static boolean isUpper(Point p1, Point p2) {
    return p1.y <= p2.y;
  }

  protected static boolean isLower(Point p1, Point p2) {
    return p1.y > p2.y;
  }
}
