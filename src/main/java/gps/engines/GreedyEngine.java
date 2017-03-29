package gps.engines;

import gps.GPSEngine;
import gps.GPSNode;
import gps.api.GPSProblem;

import java.util.Comparator;
import java.util.LinkedList;
import java.util.PriorityQueue;

public class GreedyEngine extends GPSEngine {
    private final Comparator<GPSNode> byMinorH = Comparator.comparingInt(n -> getProblem().getHValue(n.getState()));

    public GreedyEngine(GPSProblem problem) {
        super(problem);
        this.open = new PriorityQueue<>(byMinorH);
    }

    @Override
    protected void explode(GPSNode node) {
        if (alreadyVisited.containsKey(node.getState())) {
            return;
        }
        addCandidates(node, open);
    }
}
