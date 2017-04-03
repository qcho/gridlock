import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockProblem;
import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockState;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Chip;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Movement;
import ar.edu.itba.sia.c12017.g5.gridlock.utilities.BoardParser;
import gps.SearchStrategy;
import org.junit.Before;
import org.junit.Test;

import java.nio.file.Path;
import java.nio.file.Paths;

import static junit.framework.TestCase.assertFalse;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.assertNull;

public class BoardTest {
  private Board board1;
  private Board regularBoard;
  private Board easyBoard;
  private Board easyBoardWon;
  private Board verticalMovementBoard;
  private Board horizontalMovementBoard;

  @Before
  public void initialize() {
    String boardsFolder = "src/test/resources/boards/";
    Path verticalBoardPath = Paths.get(boardsFolder + "vertical_movement_test.json");
    verticalMovementBoard = BoardParser.parse(verticalBoardPath);
    horizontalMovementBoard = BoardParser.parse(
        Paths.get(boardsFolder + "horizontal_movement_test.json"));
    board1 = BoardParser.parse(verticalBoardPath);
    regularBoard = BoardParser.parse(Paths.get("src/main/resources/boards/easyboard.json"));
    easyBoard = BoardParser.parse(Paths.get("src/main/resources/boards/supereasyboard.json"));
    easyBoardWon = BoardParser.parse(Paths.get(boardsFolder + "easyboard_won.json"));
  }

  @Test
  public void testEquals() {
    assertTrue(board1.equals(verticalMovementBoard));
    assertTrue(verticalMovementBoard.equals(board1));
    assertTrue(verticalMovementBoard.equals(verticalMovementBoard));
    assertFalse(verticalMovementBoard.equals(horizontalMovementBoard));
    assertFalse(horizontalMovementBoard.equals(verticalMovementBoard));
  }

  @Test
  public void testHashCode() {
    assertNotEquals(verticalMovementBoard.hashCode(), horizontalMovementBoard.hashCode());
    assertEquals(verticalMovementBoard.hashCode(), board1.hashCode());
  }

  @Test
  public void testChipAlignment() {
    assertTrue(verticalMovementBoard.getMainChip().isVertical());
    assertFalse(verticalMovementBoard.getMainChip().isHorizontal());
    assertFalse(horizontalMovementBoard.getMainChip().isVertical());
    assertTrue(horizontalMovementBoard.getMainChip().isHorizontal());
  }

  @Test
  public void testIsGoal() {
    assertTrue(verticalMovementBoard.isGoal());
    assertTrue(horizontalMovementBoard.isGoal());
    assertFalse(regularBoard.isGoal());
    assertFalse(easyBoard.isGoal());
    assertTrue(easyBoardWon.isGoal());

    GridlockState state = new GridlockState(easyBoardWon);
    GridlockState state2 = new GridlockState(verticalMovementBoard);
    GridlockProblem problem = new GridlockProblem(state, SearchStrategy.BFS);
    assertTrue(problem.isGoal(state));
    assertTrue(problem.isGoal(state2));
  }

  @Test
  public void testMoveUp() {
    Chip main = verticalMovementBoard.getMainChip();
    assertEquals(1, main.getStartPosition().x);
    assertEquals(1, main.getEndPosition().x);
    assertEquals(3, main.getStartPosition().y);
    assertEquals(4, main.getEndPosition().y);

    Board nextMove = verticalMovementBoard.applyMovement(main.getSymbol(), Movement.UP);
    main = nextMove.getMainChip();
    assertEquals(1, main.getStartPosition().x);
    assertEquals(1, main.getEndPosition().x);
    assertEquals(2, main.getStartPosition().y);
    assertEquals(3, main.getEndPosition().y);
    int[][] originalBoard = verticalMovementBoard.getBoard();
    int[][] newBoard = nextMove.getBoard();
    assertEquals(originalBoard.length, newBoard.length);
    assertEquals(originalBoard[0].length, newBoard[0].length);
    assertNotEquals(originalBoard, newBoard);

    nextMove = nextMove.applyMovement(main.getSymbol(), Movement.UP);
    main = nextMove.getMainChip();
    assertEquals(1, main.getStartPosition().x);
    assertEquals(1, main.getEndPosition().x);
    assertEquals(1, main.getStartPosition().y);
    assertEquals(2, main.getEndPosition().y);

    nextMove = nextMove.applyMovement(main.getSymbol(), Movement.UP);
    assertNull(nextMove);
  }

  @Test
  public void testMoveDown() {
    Chip main = verticalMovementBoard.getMainChip();
    assertEquals(1, main.getStartPosition().x);
    assertEquals(1, main.getEndPosition().x);
    assertEquals(3, main.getStartPosition().y);
    assertEquals(4, main.getEndPosition().y);

    Board nextMove = verticalMovementBoard.applyMovement(main.getSymbol(), Movement.DOWN);
    main = nextMove.getMainChip();
    assertEquals(1, main.getStartPosition().x);
    assertEquals(1, main.getEndPosition().x);
    assertEquals(4, main.getStartPosition().y);
    assertEquals(5, main.getEndPosition().y);
    int[][] originalBoard = verticalMovementBoard.getBoard();
    int[][] newBoard = nextMove.getBoard();
    assertEquals(originalBoard.length, newBoard.length);
    assertEquals(originalBoard[0].length, newBoard[0].length);
    assertNotEquals(originalBoard, newBoard);

    nextMove = nextMove.applyMovement(main.getSymbol(), Movement.DOWN);
    main = nextMove.getMainChip();
    assertEquals(1, main.getStartPosition().x);
    assertEquals(1, main.getEndPosition().x);
    assertEquals(5, main.getStartPosition().y);
    assertEquals(6, main.getEndPosition().y);

    nextMove = nextMove.applyMovement(main.getSymbol(), Movement.DOWN);
    assertNull(nextMove);
  }

  @Test
  public void testMoveLeft() {
    Chip main = horizontalMovementBoard.getMainChip();
    assertEquals(3, main.getStartPosition().x);
    assertEquals(4, main.getEndPosition().x);
    assertEquals(1, main.getStartPosition().y);
    assertEquals(1, main.getEndPosition().y);

    Board nextMove = horizontalMovementBoard.applyMovement(main.getSymbol(), Movement.LEFT);
    main = nextMove.getMainChip();
    assertEquals(2, main.getStartPosition().x);
    assertEquals(3, main.getEndPosition().x);
    assertEquals(1, main.getStartPosition().y);
    assertEquals(1, main.getEndPosition().y);
    int[][] originalBoard = horizontalMovementBoard.getBoard();
    int[][] newBoard = nextMove.getBoard();
    assertEquals(originalBoard.length, newBoard.length);
    assertEquals(originalBoard[0].length, newBoard[0].length);
    assertNotEquals(originalBoard, newBoard);

    nextMove = nextMove.applyMovement(main.getSymbol(), Movement.LEFT);
    main = nextMove.getMainChip();
    assertEquals(1, main.getStartPosition().x);
    assertEquals(2, main.getEndPosition().x);
    assertEquals(1, main.getStartPosition().y);
    assertEquals(1, main.getEndPosition().y);

    nextMove = nextMove.applyMovement(main.getSymbol(), Movement.LEFT);
    assertNull(nextMove);
  }

  @Test
  public void testMoveRight() {
    Chip main = horizontalMovementBoard.getMainChip();
    assertEquals(3, main.getStartPosition().x);
    assertEquals(4, main.getEndPosition().x);
    assertEquals(1, main.getStartPosition().y);
    assertEquals(1, main.getEndPosition().y);

    Board nextMove = horizontalMovementBoard.applyMovement(main.getSymbol(), Movement.RIGHT);
    main = nextMove.getMainChip();
    assertEquals(4, main.getStartPosition().x);
    assertEquals(5, main.getEndPosition().x);
    assertEquals(1, main.getStartPosition().y);
    assertEquals(1, main.getEndPosition().y);
    int[][] originalBoard = horizontalMovementBoard.getBoard();
    int[][] newBoard = nextMove.getBoard();
    assertEquals(originalBoard.length, newBoard.length);
    assertEquals(originalBoard[0].length, newBoard[0].length);
    assertNotEquals(originalBoard, newBoard);

    nextMove = nextMove.applyMovement(main.getSymbol(), Movement.RIGHT);
    main = nextMove.getMainChip();
    assertEquals(5, main.getStartPosition().x);
    assertEquals(6, main.getEndPosition().x);
    assertEquals(1, main.getStartPosition().y);
    assertEquals(1, main.getEndPosition().y);

    nextMove = nextMove.applyMovement(main.getSymbol(), Movement.RIGHT);
    assertNull(nextMove);
  }
}
