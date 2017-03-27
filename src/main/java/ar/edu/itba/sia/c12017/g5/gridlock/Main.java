package ar.edu.itba.sia.c12017.g5.gridlock;

import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockProblem;
import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockState;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.utilities.BoardParser;
import gps.GPSEngine;
import gps.GPSEngineFactory;
import gps.GPSNode;
import gps.SearchStrategy;
import gps.api.GPSProblem;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class Main {
  private static final boolean SHOW_SOLUTION = false;
  private static final boolean SHOW_STATS = true;

  /**
   * Main function.
   *
   * @param args should contain at least a board.
   */
  public static void main(String[] args) {
    warmUp();
    String board = "src/main/resources/boards/easyboard.json";
  
    // Which strategies to run
    SearchStrategy[] strategies = {
        SearchStrategy.BFS,
        SearchStrategy.DFS,
        SearchStrategy.GREEDY,
        SearchStrategy.ASTAR
    };

    Stream.of(strategies).forEach(strategy ->
        timedRun(board, strategy, SHOW_SOLUTION, SHOW_STATS)
    );
  }

  private static void timedRun(String board, SearchStrategy strategy, boolean showSolution,
                               boolean showStats) {
    System.out.println(String.format("Starting to solve with %s", strategy));
    long startTime = System.currentTimeMillis();
    long endTime;

    run(board, strategy, showSolution, showStats);

    endTime = System.currentTimeMillis();
    System.out.println(String.format("  * Duration: %.2f seconds", (endTime - startTime) / 1000.0));
  }

  private static void run(String stringPath, SearchStrategy strategy, boolean showSolution,
                          boolean showStats) {
    // Parse board
    Path boardPath = Paths.get(stringPath);
    assert (boardPath.toFile().exists());
    Board board = BoardParser.parse(boardPath);
    //  System.out.println(board.toString());
    //  Create gps objects
    GPSProblem gridlockProblem = new GridlockProblem(new GridlockState(board));
    GPSEngine engine = GPSEngineFactory.build(gridlockProblem, strategy);
    engine.findSolution();
    if (!engine.isFailed()) {
      GPSNode node = engine.getSolutionNode();
      if (showSolution) {
        System.out.println(node.getSolution());
      }
      if (showStats) {
        printStats(engine, node);
      }
    } else {
      System.out.println("Could not find a solution");
    }
  }

  private static void printStats(GPSEngine engine, GPSNode solution) {
    GPSNode parent = solution;
    int count = 0;
    while ((parent = parent.getParent()) != null) {
      count++;
    }
    System.out.println("  * Solution found in " + count + " steps");
    System.out.println("  * Tried " + engine.getExplosionCounter() + " nodes");
  }

  private static void warmUp() {
    System.out.print("Warming up...");
    IntStream.range(0, 100).forEach(t -> {
      System.out.print(".");
      run("src/main/resources/boards/easyboard.json", SearchStrategy.DFS, false, false);
    });
    System.out.println("");
  }
}
