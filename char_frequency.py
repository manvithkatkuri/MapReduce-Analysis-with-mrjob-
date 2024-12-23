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
