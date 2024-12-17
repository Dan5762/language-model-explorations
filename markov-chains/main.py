import os
import random
from collections import defaultdict

import requests
import numpy as np

from visualise import MarkovVisualizer


class MarkovChain:
    def __init__(self, order=3):
        """
        Initialize the Markov Chain with specified order (context length)

        Args:
            order (int): Number of characters to use as context
        """
        self.order = order
        self.transitions = defaultdict(lambda: defaultdict(int))
        self.start_sequences = []

    def train(self, text):
        """
        Train the model on input text

        Args:
            text (str): Training text
        """
        # Add padding to handle beginning and end of sequences
        padded_text = '^' * self.order + text + '$' * self.order

        # Record valid start sequences
        for i in range(len(text) - self.order + 1):
            self.start_sequences.append(text[i:i + self.order])

        # Build transition probabilities
        for i in range(len(padded_text) - self.order):
            context = padded_text[i:i + self.order]
            next_char = padded_text[i + self.order]
            self.transitions[context][next_char] += 1

    def generate(self, length=100, temperature=1.0):
        """
        Generate text using the trained model

        Args:
            length (int): Length of text to generate
            temperature (float): Temperature parameter to control randomness

        Returns:
            str: Generated text
        """
        if not self.transitions:
            return "Model not trained yet!"

        # Start with a random starting sequence
        current = random.choice(self.start_sequences)
        result = [current]

        for _ in range(length):
            # Get possible next characters and their counts
            possibilities = self.transitions[current]
            if not possibilities:
                break

            # Convert counts to probabilities and apply temperature scaling
            chars, counts = zip(*possibilities.items())
            counts = np.array(counts, dtype=np.float64)

            if temperature != 0:
                counts = counts ** (1.0 / temperature)
                probabilities = counts / counts.sum()
            else:
                counts = counts == counts.max()
                probabilities = counts / counts.sum()

            # Make a weighted choice based on the scaled probabilities
            next_char = np.random.choice(chars, p=probabilities)
            result.append(next_char)
            current = current[1:] + next_char

        return ''.join(result)


def get_text():
    """
    Download The Picture of Dorian Gray from Project Gutenberg

    Returns:
        str: Cleaned text of the book
    """
    if os.path.exists("text.txt"):
        with open("text.txt", "r") as file:
            return file.read()
    else:
        url = "https://www.gutenberg.org/cache/epub/174/pg174.txt"
        response = requests.get(url)
        text = response.text

        start_of_text = text.find("*** START OF THE PROJECT GUTENBERG EBOOK THE PICTURE OF DORIAN GRAY ***")
        end_of_text = text.find("*** END OF THE PROJECT GUTENBERG EBOOK THE PICTURE OF DORIAN GRAY ***")
        text = text[start_of_text:end_of_text]

        cleaned = '\n'.join(
            line.strip() for line in text.split('\n')
            if line.strip() and not line.strip().isdigit()
        )

        with open("text.txt", "w") as file:
            file.write(cleaned)

        return cleaned


if __name__ == "__main__":
    # Get and prepare training data
    book_text = get_text()

    # # Create and train model
    model = MarkovChain(order=8)
    model.train(book_text)

    # # Generate some text
    print("Generated text:")
    print(model.generate(length=200, temperature=0.5))

    # # Visualize the model
    visualiser = MarkovVisualizer(model, max_nodes=50)
    graph = visualiser.create_visualization()
