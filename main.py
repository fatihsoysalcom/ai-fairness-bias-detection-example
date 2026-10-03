import collections

# --- Simple "AI" Model (simulating a biased decision process) ---
def make_hiring_decision(experience_years, project_score, candidate_type):
    """
    Simulates a hiring decision based on experience, project score,
    and a hidden bias related to candidate_type.
    """
    base_score = experience_years * 5 + project_score * 10

    # This line introduces an unintentional bias:
    # Candidates of 'Type Y' effectively need a higher base score to be considered 'Hired'.
    if candidate_type == 'Type Y':
        base_score -= 10 # A penalty applied to 'Type Y' candidates

    # Decision threshold
    if base_score >= 50:
        return 'Hired'
    else:
        return 'Rejected'

# --- Data Generation (Sample Candidates) ---
candidates = [
    {'id': 1, 'experience_years': 6, 'project_score': 5, 'candidate_type': 'Type X'}, # Score: 80. Decision: Hired
    {'id': 2, 'experience_years': 4, 'project_score': 3, 'candidate_type': 'Type Y'}, # Score: 50. Effective: 40. Decision: Rejected
    {'id': 3, 'experience_years': 5, 'project_score': 4, 'candidate_type': 'Type X'}, # Score: 65. Decision: Hired
    {'id': 4, 'experience_years': 3, 'project_score': 4, 'candidate_type': 'Type Y'}, # Score: 55. Effective: 45. Decision: Rejected
    {'id': 5, 'experience_years': 7, 'project_score': 2, 'candidate_type': 'Type Y'}, # Score: 55. Effective: 45. Decision: Rejected
    {'id': 6, 'experience_years': 5, 'project_score': 5, 'candidate_type': 'Type X'}, # Score: 75. Decision: Hired
    {'id': 7, 'experience_years': 6, 'project_score': 4, 'candidate_type': 'Type Y'}, # Score: 70. Effective: 60. Decision: Hired
    {'id': 8, 'experience_years': 2, 'project_score': 3, 'candidate_type': 'Type X'}, # Score: 40. Decision: Rejected
]

# --- Apply AI and Collect Results ---
results = []
for candidate in candidates:
    decision = make_hiring_decision(
        candidate['experience_years'],
        candidate['project_score'],
        candidate['candidate_type']
    )
    results.append({**candidate, 'decision': decision})

print("--- AI Hiring Decisions ---")
for r in results:
    print(f"Candidate {r['id']} ({r['candidate_type']}): Exp={r['experience_years']}, Proj={r['project_score']} -> {r['decision']}")
print("\n")

# --- AI Safety Audit (Ethical Safety: Fairness Check) ---
def conduct_fairness_audit(decisions, group_key='candidate_type', positive_outcome='Hired'):
    """
    Audits the fairness of decisions across different groups.
    Calculates the proportion of positive outcomes for each group.
    This is a basic form of ethical AI safety check.
    """
    group_outcomes = collections.defaultdict(lambda: {'total': 0, 'positive': 0})

    for decision_record in decisions:
        group = decision_record[group_key]
        group_outcomes[group]['total'] += 1
        if decision_record['decision'] == positive_outcome:
            group_outcomes[group]['positive'] += 1

    print("--- AI Safety Audit: Fairness Report ---")
    for group, data in sorted(group_outcomes.items()):
        total = data['total']
        positive = data['positive']
        if total > 0:
            rate = (positive / total) * 100
            print(f"Group '{group}': {positive}/{total} {positive_outcome} ({rate:.2f}%)")
        else:
            print(f"Group '{group}': No candidates.")

    # Simple comparison for bias detection
    groups_rates = {group: (data['positive'] / data['total']) for group, data in group_outcomes.items() if data['total'] > 0}
    if len(groups_rates) > 1:
        min_rate = min(groups_rates.values())
        max_rate = max(groups_rates.values())
        # Flag a warning if the difference in rates is substantial (e.g., more than 20% of the max rate)
        if max_rate > 0 and (max_rate - min_rate) / max_rate > 0.2:
            print("\nWARNING: Significant disparity in positive outcomes detected between groups.")
            print("This may indicate a fairness issue or bias in the AI model.")
        else:
            print("\nFairness check: No significant disparity detected (within 20% threshold).")
    else:
        print("\nFairness check: Only one group present, cannot assess inter-group fairness.")


conduct_fairness_audit(results, group_key='candidate_type', positive_outcome='Hired')
