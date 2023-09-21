import nltk
from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
import matplotlib.pyplot as plt
from collections import defaultdict

# Download the required NLTK resources
nltk.download('gutenberg')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# Read the Moby Dick file
moby_dick = gutenberg.raw('melville-moby_dick.txt')

# Tokenization
tokens = word_tokenize(moby_dick)

# Stopwords filtering
stop_words = set(stopwords.words('english'))
filtered_tokens = [token for token in tokens if token.lower() not in stop_words]

# Parts-of-Speech (POS) tagging
pos_tags = pos_tag(filtered_tokens)

# POS frequency
pos_counts = FreqDist(tag for (word, tag) in pos_tags)
top_pos = pos_counts.most_common(5)
print("Top 5 POS and their counts:")
for pos, count in top_pos:
    print(pos, ":", count)

# Lemmatization
lemmatizer = WordNetLemmatizer()
lemmatized_tokens = []

# Function to map NLTK POS tags to WordNet POS tags
def get_wordnet_pos(nltk_pos):
    if nltk_pos.startswith('J'):
        return 'a'  # Adjective
    elif nltk_pos.startswith('V'):
        return 'v'  # Verb
    elif nltk_pos.startswith('N'):
        return 'n'  # Noun
    elif nltk_pos.startswith('R'):
        return 'r'  # Adverb
    else:
        return 'n'  # Default to noun

# Lemmatize the top 20 tokens
for token, pos in pos_tags[:20]:
    wn_pos = get_wordnet_pos(pos)
    lemmatized_token = lemmatizer.lemmatize(token, pos=wn_pos)
    lemmatized_tokens.append(lemmatized_token)

# Plotting frequency distribution
pos_freq = defaultdict(int)
for word, pos in pos_tags:
    pos_freq[pos] += 1

# Sort the POS frequencies by count
sorted_pos_freq = sorted(pos_freq.items(), key=lambda x: x[1], reverse=True)

# Extract POS labels and counts for plotting
pos_labels, pos_counts = zip(*sorted_pos_freq)

# Plot the frequency distribution
plt.figure(figsize=(10, 6))
plt.bar(pos_labels, pos_counts)
plt.xlabel('Part of Speech')
plt.ylabel('Frequency')
plt.title('POS Frequency Distribution')
plt.xticks(rotation=45)
plt.show()