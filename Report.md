# **Implementing MapReduce with `mrjob`**
This document provides instructions for setting up and running a series of MapReduce tasks using Python's `mrjob` package. These tasks include counting word occurrences, finding the most frequent word, calculating character frequency, identifying common bigrams, and computing the average word length in a text file.

### Install `mrjob` Package
```bash
pip install mrjob
```
### Download a Sample Text File
Downloaded *Alice's Adventures in Wonderland* (text version) from [this link](https://www.gutenberg.org/ebooks/11).

Saved the downloaded file as `alice.txt`.

## **PART 1** 
### **Mandatory Task: Create the `word_count.py` File**
creating a new Python file named `word_count.py`. 
```python
from mrjob.job import MRJob

class WordCount(MRJob):
    
    def mapper(self, _, line):
        for word in line.split():
            yield word.lower(), 1

    def combiner(self, word, counts):
        # Locally aggregate word counts before sending to reducer
        yield word, sum(counts)

    def reducer(self, word, counts):
        # Final aggregation at the reducer level
        yield word, sum(counts)

if __name__ == '__main__':
    WordCount.run()
```

### Explanation of the Code
- **Mapper**: Reads each line of the text, splits it into words, and emits each word with a count of 1.
- **Combiner**: Optionally combines counts for each word locally to reduce data transferred to the reducer.
- **Reducer**: Aggregates the final count for each word across all lines.

### Run the Job Locally
In the terminal, navigate to the directory where `word_count.py` and `alice.txt` are located. Run the following command to execute the script with `alice.txt` as input:

```bash
python word_count.py alice.txt
```
This command will process the file and output the word count results to the terminal.

### Analyzing the Output
The program will display the word counts for each unique word in the text. 
Then redirected this output to a file for easier analysis, can be viewed in the uploaded zip file:

```bash
python word_count.py alice.txt > word_count_output.txt
```

### Sample Output - Top 10 Results 
Read the file, sort by the second column (count), and select the top 10

```bash
Get-Content word_count_output.txt | Sort-Object { [int]$_.Split()[1] } -Descending | Select-Object -First 10
```
```
"the"   1798
"and"   833
"to"    784
"a"     675
"of"    616
"she"   518
"said"  420
"in"    415
"it"    374
"was"   330
```
The table presents the frequency of the ten most commonly used words in a given text, indicating the number of occurrences for each word. The word "the" appears most frequently, with 1,798 occurrences, followed by "and" with 833 and "to" with 784, showcasing the prevalence of these common function words in the language used.


## **PART 2**
### **Task 1: Most Frequent Word**
This program identifies the most frequently occurring word in the dataset.

```python
from mrjob.job import MRJob
from mrjob.step import MRStep

class MostFrequentWord(MRJob):
    
    def mapper(self, _, line):
        for word in line.split():
            yield word.lower(), 1

    def combiner(self, word, counts):
        yield word, sum(counts)

    def reducer(self, word, counts):
        yield None, (sum(counts), word)

    def reducer_find_max(self, _, word_count_pairs):
        yield max(word_count_pairs)

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_find_max)
        ]

if __name__ == '__main__':
    MostFrequentWord.run()
```

### Explanation:
- **Mapper**: Splits each line into words, converts them to lowercase, and emits each word with a count of `1`.
- **Combiner**: Aggregates word counts locally, reducing the data size before sending it to the reducer.
- **Reducer**: Summarizes the total count of each word and emits a tuple of `(count, word)` for further processing.
- **Final Reducer (`reducer_find_max`)**: Finds the maximum count in the list of word-count pairs, returning the word with the highest frequency.

### Running the Program:
In the terminal:
```bash
python most_frequent_word.py alice.txt
```
This command will output the most frequently occurring word in the dataset, along with its count.

### Analyzing the Output
The program will display the most frequently occuring word in the text. 
Then redirected this output to a file for easier analysis, can be viewed in the uploaded zip file:

```bash
python most_frequent_word.py alice.txt > most_frequent_word.txt
```
### Sample Output:
```
1798	"the"
```
The most frequent word in Alice's Adventures in Wonderland is "the," appearing 1798 times. This result is typical for English-language texts, where "the" is one of the most common words due to its role as a definite article. Words like "the" do not convey specific meaning about the story's themes or characters but are essential for sentence structure.

---

### **Task 2: Character Frequency**
This program calculates the frequency of each alphabetic character in the text.

```python
from mrjob.job import MRJob
import re

class CharFrequency(MRJob):
    
    def mapper(self, _, line):
        for char in re.sub(r'[^a-zA-Z]', '', line):  # Remove non-alphabetic chars
            yield char.lower(), 1

    def combiner(self, char, counts):
        yield char, sum(counts)

    def reducer(self, char, counts):
        yield char, sum(counts)

if __name__ == '__main__':
    CharFrequency.run()
```

### Explanation:
- **Mapper**: Uses a regular expression to remove non-alphabetic characters from each line, then emits each alphabetic character with a count of `1`.
- **Combiner**: Summarizes character counts locally, reducing data transfer to the reducer.
- **Reducer**: Finalizes the count for each character across all lines and emits the total frequency of each character.

### Running the Program:
In the terminal:
```bash
python char_frequency.py alice.txt
```
This command will output the frequency of each character in the text.

### Analyzing the Output
The program will display the frequency of each character in the text. 
Then redirected this output to a file for easier analysis, can be viewed in the uploaded zip file:

```bash
python char_frequency.py alice.txt > char_frequency.txt
```
### Sample Output - Top 10 Results 
Read the file, sort by the second column (count), and select the top 10

```bash
Get-Content char_frequency.txt | Sort-Object { [int]$_.Split()[1] } -Descending | Select-Object -First 10
```
```
"e"     15479
"t"     12223
"a"     9837
"o"     9519
"i"     8640
"n"     8070
"h"     7922
"s"     7270
"r"     6656
"d"     5478
```
The most frequent letter in the text is "e," appearing 15,479 times, followed closely by "t" and "a." This frequency pattern is consistent with common letter distributions in English, where vowels like "e" and "a" are generally prevalent. High frequencies of "t," "h," and "n" indicate the text's reliance on commonly used words, such as articles and pronouns, essential for sentence construction.

---

### **Task 3: Bigram Count**
This program calculates the frequency of each bigram (two consecutive words) in the text.

```python
from mrjob.job import MRJob

class BigramCount(MRJob):
    
    def mapper(self, _, line):
        words = line.split()
        for i in range(len(words) - 1):  # Changed to "- 1" to generate bigrams
            bigram = f"{words[i]} {words[i+1]}"
            yield bigram.lower(), 1

    def combiner(self, bigram, counts):
        yield bigram, sum(counts)

    def reducer(self, bigram, counts):
        yield bigram, sum(counts)

if __name__ == '__main__':
    BigramCount.run()
```

### Explanation:
- **Mapper**: Splits each line into words and generates bigrams (pairs of consecutive words). Emits each bigram in lowercase with a count of `1`.
- **Combiner**: Summarizes counts for each bigram locally.
- **Reducer**: Aggregates the final count for each bigram across all lines and emits each bigram with its total count.

### Running the Program:
In the terminal:
```bash
python bigram_count.py alice.txt
```
This command will output the frequency of each bigram in the text, showing which two-word combinations are most common.

### Analyzing the Output
The program will display the frequency of each bigram in the text. 
Then redirected this output to a file for easier analysis, can be viewed in the uploaded zip file:

```bash
python bigram_count.py alice.txt > bigram_count.txt
```
### Sample Output
```
"queen in"      2
"queen merely"  1
"queen put"     1
"queen of"      4
"queen never"   1
"queen had"     3
"quadrille, that"   1
```
The program calculates the frequency of each bigram (pair of consecutive words) in the text, allowing identification of common word pairings. In this sample, "queen of" appears most frequently, suggesting it's a recurring phrase, while other bigrams with "queen" appear less often, indicating varied contexts or actions associated with the term.

---

### **Task 4: Average Word Length**
This program calculates the average word length in the text.

```python
from mrjob.job import MRJob

class AverageWordLength(MRJob):
    
    def mapper(self, _, line):
        words = line.split()
        yield "average_word_length", (sum(len(word) for word in words), len(words))

    def combiner(self, key, values):
        total_length, total_count = 0, 0
        for length, count in values:
            total_length += length
            total_count += count
        yield key, (total_length, total_count)

    def reducer(self, key, values):
        total_length, total_count = 0, 0
        for length, count in values:
            total_length += length
            total_count += count
        yield key, total_length / total_count if total_count else 0

if __name__ == '__main__':
    AverageWordLength.run()
```

### Explanation:
- **Mapper**: For each line, calculates the total character length of all words and the count of words, emitting a tuple of `(total_length, word_count)` with the key `"average_word_length"`.
- **Combiner**: Aggregates total character length and word count locally, reducing data transfer to the reducer.
- **Reducer**: Finalizes the total length and word count across all lines and calculates the average word length by dividing the total character length by the total word count.

### Running the Program:
In the terminal:
```bash
python average_word_length.py alice.txt
```
This command will output the average word length in the text.

### Analyzing the Output
The program will display the average word length in the text. 
Then redirected this output to a file for easier analysis, can be viewed in the uploaded zip file:

```bash
python average_word_length.py alice.txt > average_word_length.txt
```
### Sample Output
```
"average_word_length"	4.483797862264916
```
This program calculates the average word length in the text, providing insight into the general complexity and vocabulary used in the content. In the sample output, an average word length of approximately 4.48 characters suggests moderately sized words, making it accessible for readers.