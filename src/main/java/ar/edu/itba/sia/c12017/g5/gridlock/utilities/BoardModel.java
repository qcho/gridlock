package ar.edu.itba.sia.c12017.g5.gridlock.utilities;

import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import edu.umd.cs.findbugs.annotations.SuppressFBWarnings;

import java.util.List;

@SuppressWarnings("checkstyle:membername")
@SuppressFBWarnings
class BoardModel {
  Size size;
  Exit exit;
  List<Chip> chips;

  Board toBoard() {
    Board board = new Board(size.rows, size.columns,
        exit.position.x, exit.position.y);
    chips.forEach(c -> board.addChip(c.main,
        c.start_position.x,c.start_position.y,
        c.end_position.x, c.end_position.y));
    return board;
  }

  class Size {
    int rows;
    int columns;
  }

  class Exit {
    Position position;
  }

  class Position {
    int x;
    int y;
  }

  class Chip {
    Boolean main;
    Position start_position;
    Position end_position;
  }
}
