# [Attention Is All You Need](https://arxiv.org/pdf/1706.03762)

## Sections

- Abstract
- Introduction
- Background
- Model Architecture
    - Encoder and Decoder Stacks
        - Encoder
        - Decoder
    - Attention
        - Scaled Dot-Product Attention
        - Multi-Head Attention
        - Applications of Attention in Our Model
    - Position-wise Feed-Forward Networks
    - Embeddings and Softmax
    - Positional Encoding
- Why Self-Attention
- Training
    - Training Data and Batching
    - Hardware and Schedule
    - Optimizer
    - Regularization
- Results
    - Machine Translation
    - Model Variations
    - English Constituency Parsing
- Conclusion

## Abstract

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 Englishto-German translation task, improving over the existing best results, including ensembles, by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both withlarge and limited training data.

## Glossary

- BLEU: Bilingual Evaluation Understudy, a metric for evaluating the quality of text which has been machine-translated from one natural language to another.

