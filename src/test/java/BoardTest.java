import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.utilities.BoardParser;
import org.junit.Before;
import org.junit.Test;

import java.nio.file.Path;
import java.nio.file.Paths;

import static junit.framework.TestCase.assertFalse;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertTrue;

public class BoardTest {
  private Board board1;
  private Board regularBoard;
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
    regularBoard = BoardParser.parse(Paths.get("src/main/resources/boards/board1.json"));
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
  }
}
