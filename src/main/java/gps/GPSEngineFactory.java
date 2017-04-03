package gps;

import gps.api.GPSProblem;
import gps.engines.AStarEngine;
import gps.engines.BFSEngine;
import gps.engines.DFSEngine;
import gps.engines.GreedyEngine;
import gps.engines.IterativeDeepeningDFSEngine;

public class GPSEngineFactory {
  public static GPSEngine build(GPSProblem problem, SearchStrategy strategy) {
    switch (strategy) {
      case BFS:
        return new BFSEngine(problem);
      case DFS:
        return new DFSEngine(problem);
      case IDDFS:
        return new IterativeDeepeningDFSEngine(problem, 10);
      case ASTAR:
        return new AStarEngine(problem);
      case GREEDY:
        return new GreedyEngine(problem);
      default:
        throw new UnsupportedOperationException("Provided strategy is not supported");
    }
  }
}
