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
