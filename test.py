import matplotlib.pyplot as plt
import networkx as nx

# Define the steps and their connections
steps = [
    "Start",
    "Analyze Current State",
    "Define Ideal Final Result (IFR)",
    "Identify Contradictions",
    "Apply Inventive Principles",
    "Resource Analysis",
    "Develop Solution Concept",
    "Implement and Test",
    "End"
]

# Create a directed graph
G = nx.DiGraph()
for i in range(len(steps) - 1):
    G.add_edge(steps[i], steps[i + 1])

# Define positions for a hierarchical layout
pos = nx.spring_layout(G, seed=42)

# Draw the graph
plt.figure(figsize=(12, 8))
nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=3000, edgecolors="black")
nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20, edge_color="gray")
nx.draw_networkx_labels(G, pos, font_size=10, font_color="black", font_weight="bold")

# Add title
plt.title("ARIZ Flowchart for Schedule Application Development", fontsize=14, fontweight="bold")
plt.axis("off")
plt.show()
