from graphviz import Digraph
import random


class MarkovVisualizer:
    def __init__(self, markov_chain, max_nodes=10):
        """
        Initialize visualizer for Markov Chain

        Args:
            markov_chain: Trained MarkovChain instance
            max_nodes: Maximum number of nodes to display
        """
        self.chain = markov_chain
        self.max_nodes = max_nodes

    def create_visualization(self, start_sequence=None):
        """
        Create a visualization of the Markov chain

        Args:
            start_sequence: Optional starting sequence to visualize from

        Returns:
            Graphviz dot object
        """
        dot = Digraph(comment='Markov Chain Visualization')
        dot.attr(rankdir='LR')  # Left to right layout

        # Set node and edge styles for the specified theme
        dot.attr(bgcolor='transparent')
        dot.attr('node', shape='circle', style='filled', fillcolor='white', fontcolor='black')
        dot.attr('edge', fontsize='10', color='white', fontcolor='white')

        # If no start sequence provided, pick a random one
        if not start_sequence:
            start_sequence = random.choice(self.chain.start_sequences)

        # Keep track of nodes and edges we've added
        nodes = set([start_sequence])
        edges = set()

        # Build graph starting from start_sequence
        queue = [start_sequence]
        while queue and len(nodes) < self.max_nodes:
            current = queue.pop(0)

            # Get transitions for current sequence
            transitions = self.chain.transitions[current]
            if not transitions:
                continue

            # Convert counts to probabilities
            total = sum(transitions.values())
            probs = {char: count / total for char, count in transitions.items()}

            # Add edges for top transitions
            sorted_transitions = sorted(probs.items(), key=lambda x: x[1], reverse=True)
            for next_char, prob in sorted_transitions[:3]:  # Show top 3 transitions
                next_seq = current[1:] + next_char

                # Add nodes
                if next_seq not in nodes and len(nodes) < self.max_nodes:
                    nodes.add(next_seq)
                    dot.node(next_seq, next_seq)
                    queue.append(next_seq)

                # Add edge if both nodes exist
                if next_seq in nodes:
                    edge = (current, next_seq)
                    if edge not in edges:
                        edges.add(edge)
                        # Format probability to 2 decimal places
                        dot.edge(current, next_seq, f"{prob:.2f}")

        # Add start node
        dot.node(start_sequence, start_sequence)
        dot.render("markov_visualization", format="png", cleanup=True)
