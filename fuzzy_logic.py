import numpy as np

# Fuzzy set centroids
CENTROIDS = {
    'low': 0.15,
    'medium': 0.20,
    'high': 0.35
}


def fuzzify(x, c_prev, c_curr, c_next):
    """Calculate membership degree using a triangular membership function."""
    left = (x - c_prev) / (c_curr - c_prev) if c_curr != c_prev else 0
    right = (c_next - x) / (c_next - c_curr) if c_next != c_curr else 0
    return max(0, min(left, right))


def evaluate_transitions(transitions):
    """Map probabilities to fuzzy membership degrees."""
    results = {}
    for route, p_val in transitions.items():
        mu_low = fuzzify(p_val, 0.0, CENTROIDS['low'], CENTROIDS['medium'])
        mu_med = fuzzify(p_val, CENTROIDS['low'], CENTROIDS['medium'], CENTROIDS['high'])
        mu_high = fuzzify(p_val, CENTROIDS['medium'], CENTROIDS['high'], 1.0)

        results[route] = {
            'p': p_val,
            'low': round(mu_low, 4),
            'medium': round(mu_med, 4),
            'high': round(mu_high, 4)
        }
    return results


if __name__ == "__main__":
    # Extracted from smoothed Markov transition matrix
    target_transitions = {
        'main_page -> product_page': 0.3333,
        'cart -> checkout': 0.2000,
        'main_page -> checkout': 0.1667
    }

    membership_degrees = evaluate_transitions(target_transitions)

    print("Fuzzy Inference System Output:\n")
    for route, degrees in membership_degrees.items():
        print(f"[{route}] p={degrees['p']}")
        print(f"  μ(Low): {degrees['low']} | μ(Medium): {degrees['medium']} | μ(High): {degrees['high']}\n")