import os
import time
import pandas as pd
import numpy as np

class ProbabilityMatrix:
    def __init__(self):
        self.word_count = {}
        self.word_occur = {}
        self.unique_words = []

    def calculate_probability_matrix(self, words):
        for word in words:
            self.word_count[word] = self.word_count.get(word, 0) + 1
            self.unique_words.append(word)

        for i in range(len(words) - 1):
            pair = words[i] + ' => ' + words[i+1]
            self.word_occur[pair] = self.word_occur.get(pair, 0) + 1

        matrix = [[0 for k in range(len(self.unique_words))] for k in range(len(self.unique_words))]

        for pair, count in self.word_occur.items():
            word1, word2 = pair.split(' => ')
            index1 = self.unique_words.index(word1)
            index2 = self.unique_words.index(word2)
            matrix[index2][index1] = count

        table = pd.DataFrame(matrix, columns=self.unique_words, index=self.unique_words)
        self.prob_matrix = table.div(table.sum(axis=0), axis=1)

    def save_probability_table(self, directory, file_name):
        file_path = os.path.join(directory, f'{file_name}.csv')
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.prob_matrix.to_csv(file_path, index=True)
        print("Table saved successfully.")

class WordProbabilities:
    def __init__(self, prob_matrix, unique_words):
        self.prob_matrix = prob_matrix
        self.unique_words = unique_words

    def find_probabilities(self, find_word):
        if find_word not in self.unique_words:
            print(f"'{find_word}' is not in unique_words")
        else:
            current_index = self.unique_words.index(find_word)
            probabilities = dict(self.prob_matrix.iloc[:, current_index])
            next_words = pd.Series(probabilities, index=self.unique_words).sort_values(ascending=False)

            print(f"The most probable next words after '{find_word}' are:->")
            for word, prob in list(next_words.items())[:5]:
                print(f"--->> {word}: {np.exp(prob):.3f}")

# Main processing
start_time = time.time()
directory = 'Drectory PATH'
input_file = 'File PATH'
find_word = 'beautiful' 
file_name = input("Enter File Name As You Want To Save:--> ")

with open(input_file, 'r', encoding='UTF-8') as f:
    text = f.read().lower()
    words = text.split()

prob_matrix = ProbabilityMatrix()
prob_matrix.calculate_probability_matrix(words)
prob_matrix.save_probability_table(directory, file_name)

word_probabilities = WordProbabilities(prob_matrix.prob_matrix, prob_matrix.unique_words)
word_probabilities.find_probabilities(find_word)

end_time = time.time()
time_diff = end_time - start_time

minutes, seconds, milliseconds = int(time_diff // 60), int(time_diff % 60), int((time_diff * 1000) % 1000)
