import pandas as pd
import numpy as np


def calculate_transition_matrix(df, states):
    """Calculate raw empirical transition frequencies."""
    transition_counts = pd.DataFrame(0, index=states, columns=states)

    for _, group in df.groupby('session_idx'):
        events = group['event_type'].tolist()
        for i in range(len(events) - 1):
            curr_state, next_state = events[i], events[i + 1]
            if curr_state in states and next_state in states:
                transition_counts.loc[curr_state, next_state] += 1

    return transition_counts


def apply_laplace_smoothing(transition_counts, states, alpha=1.0):
    """Apply additive Laplace smoothing to handle zero-frequency transitions."""
    n_states = len(states)
    smoothed_matrix = pd.DataFrame(0.0, index=states, columns=states)

    for curr_state in states:
        total_transitions = transition_counts.loc[curr_state].sum()
        for next_state in states:
            n_ij = transition_counts.loc[curr_state, next_state]
            p_ij = (n_ij + alpha) / (total_transitions + alpha * n_states)
            smoothed_matrix.loc[curr_state, next_state] = p_ij

    return smoothed_matrix


if __name__ == "__main__":
    df = pd.read_csv('cleaned_mvp_sessions.csv')

    funnel_states = ['main_page', 'product_page', 'cart', 'checkout', 'payment']

    raw_matrix = calculate_transition_matrix(df, funnel_states)
    print("Raw Transition Frequencies (n_ij):\n", raw_matrix, "\n")

    smoothed_matrix = apply_laplace_smoothing(raw_matrix, funnel_states, alpha=1.0)
    print("Laplace Smoothed Probabilities (alpha=1.0):\n", smoothed_matrix.round(4))