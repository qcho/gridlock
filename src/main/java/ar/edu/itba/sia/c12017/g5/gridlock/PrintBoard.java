package ar.edu.itba.sia.c12017.g5.gridlock;

import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.utilities.BoardParser;

import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Created by alebian on 02/04/17.
 */
public class PrintBoard {
  public static void main(String[] args) {
    String stringPath = "src/main/resources/boards/1200.json";
    Path boardPath = Paths.get(stringPath);
    assert (boardPath.toFile().exists());
    Board board = BoardParser.parse(boardPath);
    System.out.println(board.toString());
  }
}
