import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.utilities.BoardParser;
import org.junit.Before;
import org.junit.Test;

import java.nio.file.Path;
import java.nio.file.Paths;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;

/**
 * Created by alebian on 3/18/17.
 */
public class BoardTest {
  private Board board1;
  private Board regularBoard;
  private Board verticalMovementBoard;
  private Board horizontalMovementBoard;

  @Before
  public void initialize() {
    String boardsFolder = "src/test/resources/boards/";
    Path horizontalBoardPath = Paths.get(boardsFolder + "horizontal_movement_test.json");
    Path verticalBoardPath = Paths.get(boardsFolder + "vertical_movement_test.json");
    Path regularBoardPath = Paths.get("src/main/resources/boards/board1.json");

    verticalMovementBoard = BoardParser.parse(verticalBoardPath);
    horizontalMovementBoard = BoardParser.parse(horizontalBoardPath);
    board1 = BoardParser.parse(verticalBoardPath);
    regularBoard = BoardParser.parse(regularBoardPath);
  }

  @Test
  public void testEquals() {
    assertEquals(true, board1.equals(verticalMovementBoard));
    assertEquals(true, verticalMovementBoard.equals(board1));
    assertEquals(true, verticalMovementBoard.equals(verticalMovementBoard));
    assertEquals(false, verticalMovementBoard.equals(horizontalMovementBoard));
    assertEquals(false, horizontalMovementBoard.equals(verticalMovementBoard));
  }

  @Test
  public void testHashCode() {
    assertNotEquals(verticalMovementBoard.hashCode(), horizontalMovementBoard.hashCode());
    assertEquals(verticalMovementBoard.hashCode(), board1.hashCode());
  }

  @Test
  public void testChipAlignment() {
    assertEquals(true, verticalMovementBoard.getMainChip().isVertical());
    assertEquals(false, verticalMovementBoard.getMainChip().isHorizontal());
    assertEquals(false, horizontalMovementBoard.getMainChip().isVertical());
    assertEquals(true, horizontalMovementBoard.getMainChip().isHorizontal());
  }

  @Test
  public void testIsGoal() {
    assertEquals(true, verticalMovementBoard.isGoal());
    assertEquals(true, horizontalMovementBoard.isGoal());
    assertEquals(false, regularBoard.isGoal());
  }
}
