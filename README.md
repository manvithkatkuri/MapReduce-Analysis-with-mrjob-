# MapReduce Analysis with `mrjob`

This project demonstrates the implementation of various text-processing tasks using the MapReduce programming model with Python's `mrjob` library. The tasks include word count, identifying the most frequent word, character frequency analysis, bigram frequency analysis, and average word length calculation. By leveraging MapReduce, the project efficiently processes large text datasets, showcasing the scalability and utility of distributed computing techniques.

## Project Description

The goal of this project is to provide practical examples of using the MapReduce model to analyze text data. Each task involves breaking down a computational problem into smaller, parallelizable components and solving it using the `mrjob` framework. The text used for the analysis is *Alice's Adventures in Wonderland*, a public domain text obtained from Project Gutenberg.

### Key Features:

1. **Word Count**: Count the frequency of each word in the text, providing insights into word usage patterns.
2. **Most Frequent Word**: Identify the word that occurs most frequently in the text.
3. **Character Frequency**: Analyze the frequency of each alphabetic character, revealing the distribution of letters.
4. **Bigram Count**: Count the frequency of two consecutive words (bigrams) to explore common word pairings.
5. **Average Word Length**: Calculate the average length of words, indicating the complexity of the vocabulary used in the text.

### Implementation:

Each task is implemented as a standalone Python script using `mrjob`, a framework for writing MapReduce programs in Python. The scripts include:
- **Mapper**: Processes input data line by line, emitting key-value pairs for further processing.
- **Combiner**: Optionally aggregates intermediate results locally to reduce data transfer.
- **Reducer**: Consolidates results from all mappers and combiners to produce the final output.

The project is structured to allow easy execution and customization of each task, making it a practical tool for learning and applying MapReduce concepts.

### Benefits:

- **Scalability**: By using the MapReduce model, the tasks can handle large datasets efficiently.
- **Modularity**: Each script is designed for a specific task, allowing users to focus on individual analyses.
- **Educational Value**: The project serves as a comprehensive example of text data processing using MapReduce, ideal for students and professionals learning distributed computing.

---


