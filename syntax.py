from collections import Counter


def words_check(prompt, response):
    """
    Example:
    prompt: "I went running"
    response: "We went running when we went to the track"

    Returns 3 / 9 = .33 because "went" was copied from the prompt and used twice, and "running" was copied from the prompt
    and used once. So, 3 of the 9 words in the response were copied.
    """
    word_counts = Counter(response.split())  # word -> # times word was typed

    s1 = set(prompt.split())
    s2 = set(response.split())
    words_in_both = s1.intersection(s2)

    ignored_words = set(
        [  # Don't punish user for copying one of these basic words
            "the",
            "of",
            "and",
            "to",
            "in",
            "a",
            "that",
            "for",
            "on",
            "with",
            "as",
            "at",
            "by",
            "from",
            "or",
        ]
    )

    copied_words = 0
    for word in words_in_both:
        if word not in ignored_words:
            copied_words += word_counts.get(word, 0)

    return float(copied_words) / len(response.split())


def compute_syntactic_similarity(prompt, response):
    syntax_algos = [words_check]

    scores = [algo(prompt, response) for algo in syntax_algos]

    return sum(scores) / len(scores)
