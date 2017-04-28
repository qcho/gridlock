package ar.edu.itba.sia.c12017.g5.gridlock;

import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockProblem;
import ar.edu.itba.sia.c12017.g5.gridlock.gps.GridlockState;
import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import ar.edu.itba.sia.c12017.g5.gridlock.utilities.BoardParser;
import ar.edu.itba.sia.c12017.g5.gridlock.utilities.ProgramArguments;
import gps.GPSEngine;
import gps.GPSEngineFactory;
import gps.GPSNode;
import gps.api.GPSProblem;
import org.pmw.tinylog.Configurator;
import org.pmw.tinylog.Level;
import org.pmw.tinylog.writers.FileWriter;

import java.nio.file.Path;
import java.nio.file.Paths;

public class Main {
  /**
   * Main function.
   *
   * @param args should contain at least a board.
   */
  public static void main(String[] args) {
    initLogging();
    ProgramArguments arguments = ProgramArguments.build(args);
    timedRun(arguments);
  }

  private static void initLogging() {
    Configurator.defaultConfig()
        .writer(new FileWriter("log.txt"))
        .level(Level.DEBUG)
        .activate();
  }

  private static void timedRun(ProgramArguments arguments) {
    System.out.println(String.format("Starting to solve with %s for %s",
        arguments.strategy, arguments.boardPath));
    long startTime = System.currentTimeMillis();
    long endTime;

    run(arguments);

    endTime = System.currentTimeMillis();
    System.out.println(String.format("  * Duration: %.2f seconds", (endTime - startTime) / 1000.0));
  }

  private static void run(ProgramArguments arguments) {
    // Parse board
    Path boardPath = Paths.get(arguments.boardPath);
    assert (boardPath.toFile().exists());
    Board board = BoardParser.parse(boardPath);
    //  System.out.println(board.toString());
    //  Create gps objects
    GPSProblem gridlockProblem =
        new GridlockProblem(new GridlockState(board), arguments.strategy);
    GPSEngine engine = GPSEngineFactory.build(gridlockProblem, arguments.strategy, arguments.plot);
    engine.findSolution();
    if (!engine.isFailed()) {
      GPSNode node = engine.getSolutionNode();
      if (arguments.showSolution) {
        System.out.println(node.getSolution());
      }
      if (arguments.showStats) {
        printStats(engine, node);
      }
    } else {
      System.out.println("Could not find a solution, tried "
          + engine.getExplosionCounter() + " nodes");
    }
  }

  private static void printStats(GPSEngine engine, GPSNode solution) {
    GPSNode parent = solution;
    int count = 0;
    while ((parent = parent.getParent()) != null) {
      count++;
    }
    System.out.println("  * Solution found in " + count + " steps");
    System.out.println("  * Exploded " + engine.getExplosionCounter() + " nodes");
    System.out.println("  * Added " + engine.getCandidatesCounter() + " candidates");
  }
}
