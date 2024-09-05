import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


class SocialMediaGraph:
    def __init__(self):
        self.graph = nx.Graph()
        self.pos = None

    def add_node(self, node_id, is_user, comments=0, views=0):
        self.graph.add_node(node_id, is_user=is_user, comments=comments, views=views)

    def add_edge(self, source, destination, edge_type):
        self.graph.add_edge(source, destination, type=edge_type)

    def draw(self, criterion='comments'):
        if criterion not in ['comments', 'views']:
            raise ValueError("Invalid criterion. Choose 'comments' or 'views'.")

        # Compute layout once
        if self.pos is None:
            self.pos = nx.spring_layout(self.graph, seed=42)  # Using a fixed seed for reproducibility

        node_colors = [self.get_node_color(node, criterion) for node in self.graph.nodes]

        fig, ax = plt.subplots(figsize=(12, 8))
        nx.draw(self.graph, pos=self.pos, with_labels=True, node_color=node_colors,
                node_size=300, font_size=8, font_color='black',
                edge_color='gray', linewidths=0.5, width=0.5, alpha=0.7, ax=ax)

        # Draw edge labels
        labels = nx.get_edge_attributes(self.graph, 'type')
        nx.draw_networkx_edge_labels(self.graph, pos=self.pos, edge_labels=labels, ax=ax)

        # Add color legend
        self.add_color_legend(criterion, ax, fig)

        plt.title(f"Social Media Graph - Highlight by {criterion.capitalize()}")
        plt.show()

    def get_node_color(self, node, criterion):
        values = np.array(list(nx.get_node_attributes(self.graph, criterion).values()))
        min_value = min(values, default=0)
        max_value = max(values, default=1)  # Avoid division by zero
        value = self.graph.nodes[node].get(criterion, 0)
        norm = mcolors.Normalize(vmin=min_value, vmax=max_value)
        cmap = plt.get_cmap('Reds')
        return cmap(norm(value))

    def add_color_legend(self, criterion, ax, fig):
        values = np.array(list(nx.get_node_attributes(self.graph, criterion).values()))
        min_value = min(values, default=0)
        max_value = max(values, default=1)
        cmap = plt.get_cmap('Reds')
        norm = mcolors.Normalize(vmin=min_value, vmax=max_value)

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])

        cbar = fig.colorbar(sm, ax=ax)
        cbar.set_label(f'{criterion.capitalize()}')
        cbar.ax.tick_params(labelsize=8)


def main():
    # Create the social media graph
    sm_graph = SocialMediaGraph()

    # Add nodes and edges
    sm_graph.add_node("User1", True)
    sm_graph.add_node("User2", True)
    sm_graph.add_node("User3", True)
    sm_graph.add_node("User4", True)
    sm_graph.add_node("User5", True)
    sm_graph.add_node("Post1", False, comments=20, views=100)
    sm_graph.add_node("Post2", False, comments=50, views=200)
    sm_graph.add_node("Post3", False, comments=10, views=50)
    sm_graph.add_node("Post4", False, comments=100, views=500)
    sm_graph.add_node("Post5", False, comments=500, views=1000)
    sm_graph.add_node("Post6", False, comments=100, views=500)
    sm_graph.add_node("Post7", False, comments=5, views=20)
    sm_graph.add_node("Post8", False, comments=1000, views=2000)
    sm_graph.add_node("Post9", False, comments=10, views=80)
    sm_graph.add_node("Post10", False, comments=30, views=120)

    sm_graph.add_edge("User1", "Post1", "author")
    sm_graph.add_edge("User1", "Post2", "author")
    sm_graph.add_edge("User2", "Post3", "author")
    sm_graph.add_edge("User2", "Post4", "author")
    sm_graph.add_edge("User3", "Post5", "author")
    sm_graph.add_edge("User3", "Post6", "author")
    sm_graph.add_edge("User4", "Post7", "author")
    sm_graph.add_edge("User4", "Post8", "author")
    sm_graph.add_edge("User5", "Post9", "author")
    sm_graph.add_edge("User5", "Post10", "author")

    sm_graph.add_edge("User1", "Post4", "viewing")
    sm_graph.add_edge("User1", "Post5", "viewing")
    sm_graph.add_edge("User1", "Post9", "viewing")
    sm_graph.add_edge("User2", "Post2", "viewing")
    sm_graph.add_edge("User2", "Post5", "viewing")
    sm_graph.add_edge("User2", "Post8", "viewing")
    sm_graph.add_edge("User3", "Post2", "viewing")
    sm_graph.add_edge("User3", "Post7", "viewing")
    sm_graph.add_edge("User3", "Post8", "viewing")
    sm_graph.add_edge("User4", "Post2", "viewing")
    sm_graph.add_edge("User4", "Post4", "viewing")
    sm_graph.add_edge("User4", "Post10", "viewing")
    sm_graph.add_edge("User5", "Post1", "viewing")
    sm_graph.add_edge("User5", "Post3", "viewing")
    sm_graph.add_edge("User5", "Post6", "viewing")

    # Draw the graph highlighting by comments
    sm_graph.draw(criterion='comments')

    # Draw the graph highlighting by views
    sm_graph.draw(criterion='views')


if __name__ == "__main__":
    main()
