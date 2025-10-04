import math

from constants import ignored_words


def curve_syntax_score(score: float) -> float:
    inverse_score = 1 - score
    return 1 - math.sqrt(inverse_score)


def compute_syntactic_similarity(prompt, response):
    syntax_algos = [words_check, levenshtein_distance_score]

    prompt = cleanup_sentence(prompt)
    response = cleanup_sentence(response)

    scores = [algo(prompt, response) for algo in syntax_algos]

    raw_score = sum(scores) / len(scores)
    return curve_syntax_score(raw_score)


def longest_common_substring_score(s1, s2) -> float:
    score = float(longest_common_substring(s1, s2)) / min(len(s1), len(s2))
    return score


def levenshtein_distance_score(s1, s2) -> float:
    """
    Higher levenshtein distance is a lower similarity.
    """
    score = 1 - float(levenshtein_distance(s1, s2)) / max(len(s1), len(s2))
    return score


def words_check(prompt, response):
    """
    Example:
    prompt: "I went running"
    response: "We went running when we went to the track"

    Returns 3 / 9 = .33 because "went" was copied from the prompt and used twice, and "running" was copied from the prompt
    and used once. So, 3 of the 9 words in the response were copied.
    """

    prompt_words = set(prompt.split())

    copied_words = 0
    total_words = 0
    for word in response.split():
        if word in ignored_words:
            continue
        total_words += 1
        if word in prompt_words:
            copied_words += 1

    score = float(copied_words) / float(total_words)
    return score


def longest_common_substring(s1: str, s2: str) -> int:
    m = len(s1)
    n = len(s2)

    # Create a 1D array to store the previous row's results
    prev = [0] * (n + 1)

    res = 0
    for i in range(1, m + 1):
        # Create a temporary array to store the current row
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[j] = prev[j - 1] + 1
                res = max(res, curr[j])
            else:
                curr[j] = 0

        # Move the current row's data to the previous row
        prev = curr

    return res


def levenshtein_distance(s1: str, s2: str) -> int:
    # Create a matrix to store distances
    rows = len(s1) + 1
    cols = len(s2) + 1
    distance_matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    # Initialize the first row and column
    for i in range(1, rows):
        distance_matrix[i][0] = i
    for j in range(1, cols):
        distance_matrix[0][j] = j

    # Fill the rest of the matrix
    for col in range(1, cols):
        for row in range(1, rows):
            cost = 0 if s1[row - 1] == s2[col - 1] else 1
            distance_matrix[row][col] = min(
                distance_matrix[row - 1][col] + 1,  # Deletion
                distance_matrix[row][col - 1] + 1,  # Insertion
                distance_matrix[row - 1][col - 1] + cost,  # Substitution
            )

    return distance_matrix[rows - 1][cols - 1]


def cleanup_sentence(s: str) -> str:
    # remove punctuation
    s = s.replace(".", "")
    s = s.replace("!", "")
    s = s.replace("?", "")

    # make lower case
    s = s.lower()
    return s
