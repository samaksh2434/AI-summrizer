import re
from collections import Counter

# -------------------------
# Utilities
# -------------------------

def split_sentences(text):
    text = text.replace("\n", " ")
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 0]


def extract_keywords(text, top_n=12):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    stopwords = {
        "that", "this", "with", "from", "were", "been", "have",
        "their", "which", "would", "there", "about", "could",
        "these", "those", "into", "while", "where"
    }
    words = [w for w in words if w not in stopwords]
    return set([w for w, _ in Counter(words).most_common(top_n)])


def decide_summary_limits(word_count, user_length):
    if user_length == "short":
        return 1, max(30, word_count // 8)
    if user_length == "long":
        return 4, max(80, word_count // 3)
    return 2, max(50, word_count // 5)


# -------------------------
# Idea-centric logic
# -------------------------

def extract_facts(sentences, keywords):
    facts = []
    for s in sentences:
        score = sum(1 for w in s.lower().split() if w in keywords)
        if score >= 2:
            facts.append(s)
    return facts


def cluster_facts(facts):
    clusters = []
    for fact in facts:
        placed = False
        fact_words = set(fact.lower().split())

        for cluster in clusters:
            base_words = set(cluster[0].lower().split())
            if len(fact_words & base_words) >= 2:
                cluster.append(fact)
                placed = True
                break

        if not placed:
            clusters.append([fact])

    return clusters


def compress_cluster(cluster):
    base = cluster[0]
    words = base.split()
    return " ".join(words[:18])


def build_summary(clusters, max_units):
    units = [compress_cluster(c) for c in clusters[:max_units]]

    if not units:
        return ""

    if len(units) == 1:
        return units[0] + "."

    summary = units[0]
    for u in units[1:]:
        summary += ", and " + u[0].lower() + u[1:]
    return summary + "."


# -------------------------
# Main API
# -------------------------

def summarize(text, user_length="medium"):
    if not text or len(text.split()) < 20:
        return text

    sentences = split_sentences(text)
    keywords = extract_keywords(text)

    max_units, max_words = decide_summary_limits(len(text.split()), user_length)

    facts = extract_facts(sentences, keywords)
    clusters = cluster_facts(facts)

    summary = build_summary(clusters, max_units)

    return " ".join(summary.split()[:max_words])
