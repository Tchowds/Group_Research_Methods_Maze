import os
import math
import matplotlib as plt
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

audio_co_presence = [3, 2, 3, 3, 4, 2, 4, 1, 4, 5, 2, 4, 5, 3, 4, 4, 5, 4, 5, 4, 4, 4, 4, 4]
haptic_co_presence = [4, 2, 3, 2, 4, 5, 3, 5, 3, 5, 4, 4, 3, 4, 4, 4, 4, 4, 3, 5, 4, 4, 3, 4]

easiness_audio = [3, 1, 4, 5, 3, 2, 4, 3, 3, 3, 2, 3, 5, 2, 4, 4, 5, 2, 5, 3, 3, 3, 5, 5]
easiness_haptic = [4, 4, 2, 4, 2, 5, 2, 5, 1, 4, 4, 3, 2, 5, 3, 3, 2, 4, 3, 2, 5, 4, 4, 4]

confidence_audio = [2, 2, 2, 4, 3, 2, 4, 4, 4, 3, 2, 4, 5, 3, 5, 4, 5, 4, 5, 5, 3, 4, 5, 5]
confidence_haptic = [4, 4, 2, 4, 4, 5, 3, 5, 2, 3, 4, 2, 2, 4, 2, 3, 2, 5, 2, 3, 4, 4, 5, 3]

helpful_audio = [2, 4, 4, 5, 5, 2, 5, 5, 2, 2, 3, 4, 5, 3, 5, 4, 5, 3, 5, 3, 4, 5, 5, 5]
helpful_haptic = [4, 4, 4, 3, 4, 5, 2, 5, 2, 4, 1, 5, 2, 5, 3, 4, 2, 5, 4, 3, 4, 5, 4, 4]

comfort_audio = [4, 2, 3, 5, 3, 5, 4, 5, 3, 5, 3, 2, 5, 3, 4, 2, 5, 5, 4, 5, 3, 5, 4, 4]
comfort_haptic = [5, 2, 3, 4, 2, 4, 3, 5, 2, 5, 4, 2, 3, 4, 5, 3, 3, 5, 5, 3, 4, 5, 4, 3]


def wilcoxon_test(data1, data2):

    # Perform Wilcoxon Signed-Rank Test
    statistic, p_value = stats.wilcoxon(data1, data2)

    # Output results
    print("Wilcoxon Signed-Rank Test:")
    print(f"Statistic: {statistic}")
    print(f"P-value: {p_value}")

    # Interpret the results
    alpha = 0.10
    if p_value < alpha:
        print("Reject the null hypothesis: There is a significant difference between the two sets of data.")
    else:
        print("Fail to reject the null hypothesis: There is no significant difference between the two sets of data.")

def monte_carlo(data1, data2):

    diff = data1 - data2

    # Calculate the observed test statistic (sum of positive differences)
    observed_statistic = sum(diff[diff > 0])

    # Number of permutations
    n_permutations = 10000

    # Initialize an array to store permuted test statistics
    permuted_statistics = []

    # Perform permutations
    for _ in range(n_permutations):
        permuted_diff = np.random.permutation(diff)
        permuted_statistic = sum(permuted_diff[permuted_diff > 0])
        permuted_statistics.append(permuted_statistic)

    # Calculate the p-value
    p_value = (sum(permuted_statistic >= observed_statistic for permuted_statistic in permuted_statistics) + 1) / (n_permutations + 1)

    # Output results
    print("Monte Carlo Permutation Test:")
    print(f"Observed Statistic: {observed_statistic}")
    print(f"P-value: {p_value}")

    # Interpret the results
    alpha = 0.10
    if p_value < alpha:
        print("Reject the null hypothesis: There is a significant difference between the two sets of data.")
    else:
        print("Fail to reject the null hypothesis: There is no significant difference between the two sets of data.")


print("co-presence")
wilcoxon_test(audio_co_presence, haptic_co_presence)
monte_carlo(np.array(audio_co_presence), np.array(haptic_co_presence))

print("easiness")
wilcoxon_test(easiness_audio, easiness_haptic)
monte_carlo(np.array(easiness_audio), np.array(easiness_haptic))

print("confidence")
wilcoxon_test(confidence_audio, confidence_haptic)
monte_carlo(np.array(confidence_audio), np.array(confidence_haptic))

print("comfort")
wilcoxon_test(comfort_audio, comfort_haptic)
monte_carlo(np.array(comfort_audio), np.array(comfort_haptic))




