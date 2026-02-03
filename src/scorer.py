from collections import Counter

def rule_based_score(sentences):
    freq = Counter(" ".join(sentences).lower().split())
    scores = {}
    for s in sentences:
        scores[s] = sum(freq[w] for w in s.lower().split())
    return scores
