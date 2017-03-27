package gps.engines;

import gps.GPSEngine;
import gps.GPSNode;
import gps.api.GPSProblem;

import java.util.*;

public class GreedyEngine extends GPSEngine {
    private final Comparator<GPSNode> byMinorH = Comparator
            .comparingInt((GPSNode node) -> getProblem().getHValue(node.getState()))
            .thenComparing((GPSNode node) -> getProblem().getHValue(node.getState()));

    public GreedyEngine(GPSProblem problem) {
        super(problem);
        this.open = new LinkedList<>();
    }

    @Override
    protected void explode(GPSNode node) {
        // TODO: Once heuristics are created, remove this
        //       because it is not theoretically needed
        if (alreadyVisited.containsKey(node.getState())) {
            return;
        }
        List<GPSNode> newCandidatesList = new ArrayList<>();
        addCandidates(node, newCandidatesList);
        newCandidatesList.sort(byMinorH);
        LinkedList<GPSNode> list = new LinkedList<>();
        list.addAll(newCandidatesList);
        list.addAll(open);
        open = list;
    }
}
