package gps;

import ar.edu.itba.sia.c12017.g5.gridlock.utilities.GraphBuilder;
import gps.api.GPSProblem;
import gps.engines.AStarEngine;
import gps.engines.BFSEngine;
import gps.engines.DFSEngine;
import gps.engines.FrontierIterativeDeepeningDFSEngine;
import gps.engines.GreedyEngine;
import gps.engines.IterativeDeepeningDFSEngine;

public class GPSEngineFactory {

  public static GPSEngine build(GPSProblem problem, SearchStrategy strategy) {
    return build(problem, strategy, false);
  }

  public static GPSEngine build(GPSProblem problem, SearchStrategy strategy, boolean plot) {
    GPSEngine out;
    switch (strategy) {
      case BFS:
        out = new BFSEngine(problem);
        break;
      case DFS:
        out = new DFSEngine(problem);
        break;
      case IDDFS:
        out = new IterativeDeepeningDFSEngine(problem, 1);
        break;
      case FIDDFS:
        out = new FrontierIterativeDeepeningDFSEngine(problem, 1);
        break;
      case ASTAR:
        out = new AStarEngine(problem);
        break;
      case GREEDY:
        out = new GreedyEngine(problem);
        break;
      default:
        throw new UnsupportedOperationException("Provided strategy is not supported");
    }
    if (plot) {
      out.setGraphBuilder(new GraphBuilder(out));
    }
    return out;
  }
}
