package ar.edu.itba.sia.c12017.g5.gridlock.models;

import java.util.stream.IntStream;

/**
 * Created by alebian on 14/03/17.
 */
/*
* The board positions are interpreted as:
*    (x = 0, y = 0) +-----+-----+-----+ (y = 0, x = cols)
*                   |     |     |     |
*                   +-----+-----+-----+
*                   |     |     |     |
*                   +-----+-----+-----+
*                   |     |     |     |
* (y = rows, x = 0) +-----+-----+-----+ (rows, cols)
* */
public class Board {
    private int rows;
    private int cols;
    private int exitX;
    private int exitY;
    private int[][] board;
    private static final int MAIN_CHIP_SYMBOL = 1;
    private int nextChip = 2;

    public Board(long rows, long cols, long exitX, long exitY) {
        this.rows = Long.valueOf(rows).intValue();
        this.cols = Long.valueOf(cols).intValue();
        this.exitX = Long.valueOf(exitX).intValue();
        this.exitY = Long.valueOf(exitY).intValue();
        this.board = new int[this.rows][this.cols];
        fillBoardWith(0);
    }

    private void fillBoardWith(int value) {
        IntStream.range(0, rows).forEach(i ->
                IntStream.range(0, cols).forEach(j ->
                        board[i][j] = value));
    }

    public void addChip(boolean main, long sx, long sy, long ex, long ey) {
        int symbol = main ? MAIN_CHIP_SYMBOL : nextChip;
        if (sx == ex) {
            assert (sy < ey);
            // VERTICAL CHIP
            IntStream.range(Long.valueOf(sy - 1).intValue(), Long.valueOf(ey).intValue()).forEach(y ->
                    board[y][Long.valueOf(sx - 1).intValue()] = symbol);
        }
        else if (sy == ey) {
            assert (sx < ex);
            // HORIZONTAL CHIP
            IntStream.range(Long.valueOf(sx - 1).intValue(), Long.valueOf(ex).intValue()).forEach(x ->
                    board[Long.valueOf(sy - 1).intValue()][x] = symbol);
        }
        else {
            throw new IllegalArgumentException("Cannot insert diagonal chips");
        }
        if (!main) {
            nextChip++;
        }
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        IntStream.range(0, rows).forEach(y -> {
            IntStream.range(0, cols).forEach(x -> {
                sb.append(board[y][x]);
                sb.append(" ");
            });
            if (y == exitY - 1) {
                sb.append("X");
            }
            sb.append("\n");
        });
        return sb.toString();
    }
}
