from mrjob.job import MRJob

class BigramCount(MRJob):
    
    def mapper(self, _, line):
        words = line.split()
        for i in range(len(words) - 2):
            bigram = f"{words[i]} {words[i+1]}"
            yield bigram.lower(), 1

    def combiner(self, bigram, counts):
        yield bigram, sum(counts)

    def reducer(self, bigram, counts):
        yield bigram, sum(counts)

if __name__ == '__main__':
    BigramCount.run()
