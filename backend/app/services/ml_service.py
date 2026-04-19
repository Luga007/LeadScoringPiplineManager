import numpy as np


def calculate_conversion_probability(lead):
    """
    Simple scoring logic (replace later with ML model)
    """

    score = 0

    # Budget factor
    if lead.budget:
        if lead.budget > 10000:
            score += 0.4
        elif lead.budget > 5000:
            score += 0.25
        else:
            score += 0.1

    # Industry weight
    high_value_industries = ["IT", "Finance", "SaaS"]
    if lead.industry in high_value_industries:
        score += 0.3
    else:
        score += 0.1

    # Random noise (simulate ML)
    score += np.random.uniform(0.05, 0.2)

    return round(min(score, 1.0), 2)