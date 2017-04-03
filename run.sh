#!/bin/sh

#Strategies:
#   - IDDFS: Iterative deepening DFS.
#   - FIDDFS: Same as IDDFS but optimized to restart each iteration with frontier.
#   - ASTAR: A-Star algorithm
#   - GREEDY: Greedy algorithm
#   - BFS: Breadth first search
#   - DFS: Deapth first search
strategy="ASTAR"

# Level: Path to level
level="src/main/resources/boards/800.json"

# Plot: Generate plot file? (Generates A LOT of overhead)
plot="false"

# Show statistics? true/false
showstats="true"

# Show solution? true/false
showsolution="true"

# DO NOT MODIFY FROM HERE DOWN
while [[ $# -gt 1 ]]
do
    key="$1"
    case $key in
        --level)
            level="$2"
            shift
            ;;
        --strategy)
            lowerstrat="$(echo $2 | tr '[A-Z]' '[a-z]')"
            shift
            case $lowerstrat in
                iddfs|dfs|bfs|greedy|astar) strategy="$lowerstrat";;
                *) echo "Invalid strategy"; exit ;;
            esac
            ;;
        --hidestats)
            showstats="false"
            ;;
        --plot)
            plot="true"
            ;;
        --hidesolution)
            showsolution="false"
            ;;
        *)
            echo "Unknown option $1"
            ;;
    esac
done

./gradlew -q run -PappArgs="['strategy=$strategy','level=$level','showstats=$showstats','showsolution=$showsolution','plot=$plot']"
