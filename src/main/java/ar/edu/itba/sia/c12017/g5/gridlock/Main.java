package ar.edu.itba.sia.c12017.g5.gridlock;

import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockEngine;
import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockProblem;
import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockState;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.utilities.BoardParser;
import com.sun.tools.corba.se.idl.StringGen;
import gps.GPSEngine;
import gps.SearchStrategy;
import gps.api.GPSProblem;
import gps.api.GPSState;

import java.nio.file.Path;
import java.nio.file.Paths;

public class Main {
  public static void main(String[] args) {
    // Parse board
    String boardsFolder = "src/main/resources/boards/";
    String boardName = "easyboard.json";
    Path boardPath = Paths.get(boardsFolder + boardName);
    assert (boardPath.toFile().exists());
    BoardParser parser = new BoardParser(boardPath);
    Board board = parser.parse();
    System.out.println(board.toString());
    // Create the GPS objects
//    GPSState initialState = new GridlockState(board);
//    GPSProblem gridlockProblem = new GridlockProblem(initialState);
//    GPSEngine engine = new GridlockEngine(gridlockProblem, SearchStrategy.BFS);
  }
}
