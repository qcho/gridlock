package ar.edu.itba.sia.c12017.g5.gridlock;

import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.utilities.BoardParser;

import java.nio.file.Path;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) {
        Path boardPath = Paths.get("src/main/resources/boards/board1.json");
        assert (boardPath.toFile().exists());
        BoardParser parser = new BoardParser(boardPath);
        Board board = parser.parse();
        System.out.println(board.toString());
    }
}
