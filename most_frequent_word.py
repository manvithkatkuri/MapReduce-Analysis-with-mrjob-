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
