from dataclasses import dataclass
from math import hypot
from pathlib import Path
from typing import Dict, List, Tuple

import yaml


@dataclass(frozen=True)
class GraphNode:
    node_id: str
    x: float
    y: float
    yaw: float = 0.0


class NavigationGraph:
    def __init__(self, config_file: str):
        self.config_file = Path(config_file)
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: Dict[str, List[Tuple[str, float]]] = {}
        self.load()

    def load(self) -> None:
        with self.config_file.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file) or {}

        self.nodes.clear()
        self.edges.clear()

        for node_id, data in config.get("nodes", {}).items():
            self.nodes[node_id] = GraphNode(
                node_id=node_id,
                x=float(data["x"]),
                y=float(data["y"]),
                yaw=float(data.get("yaw", 0.0)),
            )
            self.edges[node_id] = []

        for edge in config.get("edges", []):
            if isinstance(edge, dict):
                source = edge["from"]
                target = edge["to"]
                cost = edge.get("cost")
                bidirectional = edge.get("bidirectional", True)
            else:
                source, target = edge[0], edge[1]
                cost = edge[2] if len(edge) > 2 else None
                bidirectional = True

            if source not in self.nodes or target not in self.nodes:
                raise ValueError(
                    f"Graph edge references unknown node: {source} -> {target}"
                )

            if cost is None:
                cost = self.distance(source, target)

            cost = float(cost)
            self.edges[source].append((target, cost))

            if bidirectional:
                self.edges[target].append((source, cost))

    def distance(self, source: str, target: str) -> float:
        a = self.nodes[source]
        b = self.nodes[target]
        return hypot(b.x - a.x, b.y - a.y)

    def neighbors(self, node_id: str):
        return self.edges.get(node_id, [])

    def shortest_path(self, start: str, goal: str):
        import heapq

        if start not in self.nodes:
            raise KeyError(f"Unknown start node: {start}")
        if goal not in self.nodes:
            raise KeyError(f"Unknown goal node: {goal}")

        distances = {node_id: float("inf") for node_id in self.nodes}
        previous = {node_id: None for node_id in self.nodes}

        distances[start] = 0.0
        queue = [(0.0, start)]

        while queue:
            current_cost, current = heapq.heappop(queue)

            if current_cost > distances[current]:
                continue

            if current == goal:
                break

            for neighbor, edge_cost in self.neighbors(current):
                new_cost = current_cost + edge_cost

                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    previous[neighbor] = current
                    heapq.heappush(queue, (new_cost, neighbor))

        if distances[goal] == float("inf"):
            return [], float("inf")

        path = []
        current = goal

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()
        return path, distances[goal]
