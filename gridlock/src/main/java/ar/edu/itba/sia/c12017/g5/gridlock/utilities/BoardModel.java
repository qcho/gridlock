package ar.edu.itba.sia.c12017.g5.gridlock.utilities;

import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Chip;
import edu.umd.cs.findbugs.annotations.SuppressFBWarnings;

import java.awt.Point;
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
    chips.forEach(c -> board.addChip(c.isMain(),
        c.getStartPosition().x, c.getStartPosition().y,
        c.getEndPosition().x, c.getEndPosition().y));
    return board;
  }

  class Size {
    int rows;
    int columns;
  }

  class Exit {
    Point position;
  }
}
