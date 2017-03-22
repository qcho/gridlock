package ar.edu.itba.sia.c12017.g5.gridlock;

import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockEngine;
import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockProblem;
import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockState;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.utilities.BoardParser;
import gps.GPSEngine;
import gps.GPSNode;
import gps.SearchStrategy;
import gps.api.GPSProblem;

import java.nio.file.Path;
import java.nio.file.Paths;

public class Main {
  /**
   * Main function.
   *
   * @param args should contain at least a board.
   */
  public static void main(String[] args) {
    // Parse board
    String boardsFolder = "src/main/resources/boards/";
    String boardName = "easyboard.json";
    Path boardPath = Paths.get(boardsFolder + boardName);
    assert (boardPath.toFile().exists());
    Board board = BoardParser.parse(boardPath);
    //  System.out.println(board.toString());
    //  Create gps objects
    GPSProblem gridlockProblem = new GridlockProblem(new GridlockState(board));
    GPSEngine engine = new GridlockEngine(gridlockProblem, SearchStrategy.BFS);
    engine.findSolution();
    if (engine.isFinished()) {
      GPSNode node = engine.getSolutionNode();
      System.out.println(node.getSolution());
    } else {
      System.out.println("Could not find a solution");
    }
  }
}
