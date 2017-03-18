package ar.edu.itba.sia.c12017.g5.gridlock;

import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.utilities.BoardParser;

import java.nio.file.Path;
import java.nio.file.Paths;

public class Main {
  /**
   * Main function.
   * @param args should contain at least a board.
   */
  public static void main(String[] args) {
    // Parse board
    String boardsFolder = "src/main/resources/boards/";
    String boardName = "easyboard.json";
    Path boardPath = Paths.get(boardsFolder + boardName);
    assert (boardPath.toFile().exists());
    Board board = BoardParser.parse(boardPath);
    System.out.println(board.toString());
  //  Create gps objects
  //  GpsState initialState = new GridlockState(board);
  //  GpsProblem gridlockProblem = new GridlockProblem(initialState);
  //  GpsEngine engine = new GridlockEngine(gridlockProblem, SearchStrategy.BFS);
  }
}
