package ar.edu.itba.sia.c12017.g5.gridlock.utilities;

import gps.GPSNode;
import gps.api.GPSState;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.StringJoiner;
import java.util.concurrent.atomic.AtomicInteger;

public class GraphBuilder {

    private List<GPSNode> graph = new ArrayList<>();

    public void add(GPSNode node) {
        graph.add(node);
    }

    @Override
    public String toString() {
        StringJoiner sj = new StringJoiner(";\n    ", "{\n    ", "}\n");
        sj.add("graph [fontname =\"Courier\", fontsize=10]");
        sj.add("node [shape=\"plaintext\", fontname = \"Courier\", fontsize=10]");
        sj.add("edge [fontname = \"Courier\", fontsize=10]");
        AtomicInteger nodesIndex = new AtomicInteger();
        AtomicInteger edgesIndex = new AtomicInteger();
        Map<GPSState,String> added = new HashMap<>();
        graph.forEach(node -> {
            String cId = added.computeIfAbsent(
                    node.getState(),
                    state -> {
                        String k = String.format("n%09d", nodesIndex.incrementAndGet());
                        sj.add(k + "[label=\"" + state.toString().replaceAll("(\\r|\\n|\\r\\n)+", "\\\\n") + "\"]");
                        return k;
                    }
            );
            if (node.getParent() != null) {
                String pId = added.computeIfAbsent(
                        node.getParent().getState(),
                        state -> {
                            String k = String.format("n%09d", nodesIndex.incrementAndGet());
                            sj.add(k + "[label=\"" + state.toString().replaceAll("(\\r|\\n|\\r\\n)+", "\\\\n") + "\"]");
                            return k;
                        }
                );
                sj.add(pId + "->" + cId + "[label=\" " + edgesIndex.incrementAndGet() + "#" + node.getGenerationRule().getName() + "\"]");

            }

        });
        return "digraph graphname " + sj.toString();
    }

    public void writeToFile(Path path) {
        try {
            try (BufferedWriter writer = Files.newBufferedWriter(path))
            {
                writer.write(this.toString());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
