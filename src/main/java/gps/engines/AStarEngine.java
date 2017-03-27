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
        this.byMinorF = getComparator();
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

    private Comparator<GPSNode> getComparator() {
        /*
         * n1 = First node
         * n2 = Second node
         * n{1,2}H = Heuristic value: Estimate cost from current position to goal.
         * n{1,2}G = Current cost: Cost from root node to current node.
         * n{1,2}F = Total cost: Total solution cost computed from current cost and expected remaining cost.
         */
        return (n1, n2) -> {
            Integer n1H = getProblem().getHValue(n1.getState());
            Integer n1G = n1.getCost();
            Integer n1F = n1G + n1H;
            Integer n2H = getProblem().getHValue(n2.getState());
            Integer n2G = n2.getCost();
            Integer n2F = n2G + n2H;
            if (!n1F.equals(n2F)) {
                return n1F - n2F;
            }
            // We return the node with the minor H
            return n1H <= n2H ? -1 : 1;
        };
    }
}
