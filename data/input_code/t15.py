import re
def split_lowerstring(text):
 return (re.findall('[a-z][^a-z]*', text))