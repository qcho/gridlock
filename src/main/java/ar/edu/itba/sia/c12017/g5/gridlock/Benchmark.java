package ar.edu.itba.sia.c12017.g5.gridlock;

import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockProblem;
import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockState;
import ar.edu.itba.sia.c12017.g5.gridlock.gps.ShuffleGridlockProblem;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.utilities.BoardParser;
import gps.GPSEngine;
import gps.GPSEngineFactory;
import gps.GPSNode;
import gps.SearchStrategy;
import gps.api.GPSProblem;
import org.pmw.tinylog.Configurator;
import org.pmw.tinylog.Level;
import org.pmw.tinylog.writers.FileWriter;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class Benchmark {
  private static int NUMBER_OF_RUNS = 100;

  private static class Tuple {
    long explosionCounter = 0;
    long totalNodes = 0;

    public Tuple(GPSEngine engine, GPSNode solution) {
      GPSNode parent = solution;
      while ((parent = parent.getParent()) != null) {
        totalNodes++;
      }
      this.explosionCounter = engine.getExplosionCounter();
    }
  }

  static Map<String, List<Tuple>> results = new HashMap<>();

  /**
   * Benchmark main.
   * @param args none.
   */
  public static void main(String[] args) {
    initLogging();
    warmUp();

    String[] boards = {
//        "src/main/resources/boards/371.json",
        "src/main/resources/boards/700.json",
//        "src/main/resources/boards/800.json",
//        "src/main/resources/boards/1200.json"
    };

    SearchStrategy[] strategies = {
//        SearchStrategy.BFS,
        SearchStrategy.DFS,
//        SearchStrategy.IDDFS,
//        SearchStrategy.FIDDFS,
//        SearchStrategy.GREEDY,
//        SearchStrategy.ASTAR
    };

    Stream.of(boards).forEach(board ->
        Stream.of(strategies).forEach(strategy ->
            run(board, strategy)
        )
    );

    printManyStats();
  }

  @SuppressWarnings("checkstyle:variabledeclarationusagedistance")
  private static void run(String stringPath, SearchStrategy strategy) {
    String[] pathSliced = stringPath.split("/");
//    System.out.println(String.format(
//        "Starting to solve with %s for %s", strategy, pathSliced[pathSliced.length - 1]));
    long startTime = System.currentTimeMillis();
    long endTime;

    // Parse board
    Path boardPath = Paths.get(stringPath);
    assert (boardPath.toFile().exists());
    Board board = BoardParser.parse(boardPath);
    //  Create gps objects

    GPSProblem gridlockProblem = new ShuffleGridlockProblem(new GridlockState(board), strategy);
    ;
    GPSEngine engine = null;
    GPSNode solution = null;
    for (int i = 0; i < NUMBER_OF_RUNS; i++) {
      System.out.println(i + " " + (new Date()).toString());
      engine = GPSEngineFactory.build(gridlockProblem, strategy);
      engine.findSolution();
      if (engine.isFailed()) {
        throw new RuntimeException("Could not find a solution");
      } else {
        solution = engine.getSolutionNode();
      }
      results.putIfAbsent(pathSliced[pathSliced.length - 1], new ArrayList<>());
      results.get(pathSliced[pathSliced.length - 1]).add(new Tuple(engine, solution));
    }

//    printStats(engine, solution);
    endTime = System.currentTimeMillis();
    double totalTime = (endTime - startTime) / 1000.0;

//    System.out.println(String.format(
//        "  * Total duration: %.2f seconds of %d runs", totalTime, NUMBER_OF_RUNS));
//    System.out.println(String.format(
//        "  * Each duration: %.2f seconds", totalTime / NUMBER_OF_RUNS));
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

  private static void printManyStats() {
    results.keySet().forEach(board -> {
      System.out.println("Solutions for " + board);
      int totalNodes = 0;
      int explosionCounter = 0;

      for (int i = 0; i < results.get(board).size(); i++) {
        totalNodes += results.get(board).get(i).totalNodes;
        explosionCounter += results.get(board).get(i).explosionCounter;
      }
      System.out.println("  * Average solution " + (totalNodes / NUMBER_OF_RUNS) + " steps");
      System.out.println("  * Average tried " + (explosionCounter / NUMBER_OF_RUNS) + " nodes");
    });
  }

  private static void initLogging() {
    Configurator.defaultConfig()
        .writer(new FileWriter("log.txt"))
        .level(Level.WARNING)
        .activate();
  }

  public static void warmUp() {
    System.out.println("Warming up...");
    Board board = BoardParser.parse(Paths.get("src/main/resources/boards/supereasyboard.json"));
    IntStream.range(0, 1000).forEach(t -> {
      GPSProblem gridlockProblem =
          new GridlockProblem(new GridlockState(board), SearchStrategy.DFS);
      GPSEngineFactory.build(gridlockProblem, SearchStrategy.DFS).findSolution();
    });
    System.out.println("");
  }
}
