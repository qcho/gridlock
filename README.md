# Gridlock

## Running the project
There's a script that handles running the GPS.
It supports the following parameters:
- level: Path to board
- strategy: Strategy to use (IDDFS, DFS, BFS, ASTAR, Greedy)

The following parameters are optional:
- hidestats: Hides statistics after running the GPS
- plot: Creates a .dot file showing what the engine did.
- hidesolution: Hides the solution

Example usage:
```bash
./run.sh \
    --level src/main/resources/boards/800.json \
    --strategy IDDFS \
    --hidestats
```
