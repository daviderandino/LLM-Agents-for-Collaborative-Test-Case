class StringProcessor:
    def __init__(self, text=""):
        self.text = text
    
    def set_text(self, text):
        self.text = text
        return self
    
    def reverse(self):
        return self.text[::-1]
    
    def is_palindrome(self):
        cleaned = "".join(c.lower() for c in self.text if c.isalnum())
        return cleaned == cleaned[::-1]
    
    def count_vowels(self):
        return sum(1 for c in self.text.lower() if c in "aeiou")
    
    def count_words(self):
        return len(self.text.split())
    
    def word_frequency(self):
        freq = {}
        for word in self.text.lower().split():
            word = "".join(c for c in word if c.isalnum())
            if word:
                freq[word] = freq.get(word, 0) + 1
        return freq
    
    def capitalize_words(self):
        return " ".join(word.capitalize() for word in self.text.split())
    
    def remove_duplicates(self):
        seen = set()
        result = []
        for c in self.text:
            if c not in seen:
                seen.add(c)
                result.append(c)
        return "".join(result)
    
    def find_longest_word(self):
        words = self.text.split()
        return max(words, key=len) if words else ""
    
    def truncate(self, max_len, suffix="..."):
        if len(self.text) <= max_len:
            return self.text
        return self.text[:max_len - len(suffix)] + suffix
