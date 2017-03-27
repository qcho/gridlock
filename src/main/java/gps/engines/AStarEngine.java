package gps.engines;

import gps.GPSEngine;
import gps.GPSNode;
import gps.api.GPSProblem;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedList;
import java.util.List;

public class AStarEngine extends GPSEngine {
    private Comparator<GPSNode> byMinorF;

    public AStarEngine(GPSProblem problem) {
        super(problem);
        this.open = new LinkedList<>();
        this.byMinorF = new Comparator<GPSNode>() {
            @Override
            public int compare(GPSNode n1, GPSNode n2) {
                Integer n1H = getProblem().getHValue(n1.getState());
                Integer n1G = n1.getCost();
                Integer n1F = n1G + n1H;
                Integer n2H = getProblem().getHValue(n2.getState());
                Integer n2G = n2.getCost();
                Integer n2F = n2G + n2H;
                if (!n1F.equals(n2F)) {
                    return n1F - n2F;
                } else {
                    // We return the node with the minor H
                    if (n1H <= n2H) {
                        return - 1;
                    } else {
                        return 1;
                    }
                }
            }
        };
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
        newCandidatesList.sort(byMinorF);
        LinkedList<GPSNode> list = new LinkedList<>();
        list.addAll(newCandidatesList);
        list.addAll(open);
        open = list;
    }
}
