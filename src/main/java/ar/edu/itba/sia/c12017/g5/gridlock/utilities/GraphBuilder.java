package ar.edu.itba.sia.c12017.g5.gridlock.utilities;

import gps.GPSEngine;
import gps.GPSNode;
import gps.api.GPSState;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.StringJoiner;
import java.util.concurrent.atomic.AtomicInteger;

public class GraphBuilder {

  private List<GPSNode> graph = new ArrayList<>();
  private List<GPSNode> solutionNodes = new ArrayList<>();
  private GPSEngine engine;

  public GraphBuilder(GPSEngine engine) {
    this.engine = engine;
  }

  /**
   * Add a node to be graphed out.
   * @param node node
   */
  public void add(GPSNode node) {
    graph.add(node);
  }

  @Override
  public String toString() {
    StringJoiner sj = new StringJoiner(";\n    ", "{\n    ", "\n}\n");
    sj.add("graph ["
        + "fontname =\"Courier\", "
        + "fontsize=10, "
        + "overlap=scalexy, "
        + "splines=ortho, "
        + "nodesep=1, "
        + "ranksep=2, "
        + "ordering=\"out\""
        + "]");
    sj.add("node [shape=\"plaintext\", fontname = \"Courier\", fontsize=10]");
    sj.add("edge [fontname = \"Courier\", fontsize=10]");
    AtomicInteger nodesIndex = new AtomicInteger();
    AtomicInteger edgesIndex = new AtomicInteger();
    Map<GPSState,String> added = new HashMap<>();
    Map<Integer,List<String>> ranks = new HashMap<>();
    GPSNode solutionNode = engine.getSolutionNode();
    do {
      this.solutionNodes.add(solutionNode);
    } while ((solutionNode = solutionNode.getParent()) != null);
    graph.forEach(node -> {
      boolean inSolution = solutionNodes.contains(node);
      String currentId = added.computeIfAbsent(
          node.getState(),
          state -> {
            String id = String.format("n%09d", nodesIndex.incrementAndGet());
            ranks.computeIfAbsent(node.getCost(), integer -> new ArrayList<>()).add(id);
            sj.add(id + "["
                + (inSolution ? "shape=\"box\", fillcolor=orange, style=\"rounded,filled\", " : "")
                + "label=\"" + state.toString().replaceAll("(\\r|\\n|\\r\\n)+", "\\\\n")
                + "\"]");
            return id;
          }
      );
      if (node.getParent() != null) {
        String parentId = added.computeIfAbsent(
            node.getParent().getState(),
            state -> {
              String id = String.format("n%09d", nodesIndex.incrementAndGet());
              ranks.computeIfAbsent(node.getParent().getCost(),
                  integer -> new ArrayList<>()
              ).add(id);
              sj.add(id + "["
                  + (inSolution ? "shape=\"box\", fillcolor=orange, "
                  + "style=\"rounded,filled\", " : "")
                  + "label=\"" + state.toString().replaceAll("(\\r|\\n|\\r\\n)+", "\\\\n")
                  + "\"]");
              return id;
            }
        );
        sj.add(parentId + "->" + currentId + "["
            + "headlabel=\"  "
            + edgesIndex.incrementAndGet() + "#" + node.getGenerationRule().getName()
            + "  \"]");
      }

    });
    ranks.forEach((rank, nodes) -> sj.add("{rank = same; " + String.join("; ", nodes) + "}"));
    return "digraph graphname " + sj.toString();
  }

  /**
   * Dump dot file.
   */
  public void writeToFile() {
    try {
      try (BufferedWriter writer = Files.newBufferedWriter(
          Paths.get("/tmp/solution_" + engine.getClass().getSimpleName() + ".dot")
      )) {
        writer.write(this.toString());
      }
    } catch (IOException exception) {
      exception.printStackTrace();
    }
  }
}
