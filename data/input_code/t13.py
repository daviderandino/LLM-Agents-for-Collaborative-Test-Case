from collections import Counter
def count_common(words):
  word_counts = Counter(words)
  top_four = word_counts.most_common(4)
  return (top_four)
