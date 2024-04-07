import numpy as np
import statsmodels.api as sm
from sklearn.utils import resample
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import math

imputation = True # DNF data are replaced with the mean of the rest of the data
#imputation = False # DNF data removed
ignore_ms = True
audio = True
haptic = True
x = None
y = None
ms = None #1 = user was motion sick

if (audio and haptic):
    print("both")
    x = np.array([3, 2, 3, 3, 4, 2, 4, 1, 4, 5, 2, 4, 5, 3, 4, 4, 5, 4, 5, 4, 4, 4, 4, 4, 4, 2, 3, 2, 4, 5, 3, 5, 3, 5, 4, 4, 3, 4, 4, 4, 4, 4, 3, 5, 4, 4, 3, 4]).reshape(-1, 1)  # Independent variable (user score)
    y = np.array([-1, -1, 108.12, 163.98, 163.98, 260.29, 89.38, -1, 165.5, 471.55, 471.55, 108.12, 112.34, -1, 112.34, 165.5, 89.38, 260.29, 116.09, 116.09, 290.38, 290.38, 50.32, 50.32, -1, -1, 197.27, 212.74, 212.74, 197.56, 526.55, 53.23, 57.61, 58.98, 58.98, 197.27, 326.15, 53.23, 326.15, 57.61, 526.55, 197.56, 268.41, 268.41, 91.46, 91.46, 88.5, 88.5])  # Dependent variable (task completion time)
    ms = np.array([0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0])

elif (audio and not haptic):
    print("audio")
    x = np.array([3, 2, 3, 3, 4, 2, 4, 1, 4, 5, 2, 4, 5, 3, 4, 4, 5, 4, 5, 4, 4, 4, 4, 4]).reshape(-1, 1)  # Independent variable (user score)
    y = np.array([-1, -1, 108.12, 163.98, 163.98, 260.29, 89.38, -1, 165.5, 471.55, 471.55, 108.12, 112.34, -1, 112.34, 165.5, 89.38, 260.29, 116.09, 116.09, 290.38, 290.38, 50.32, 50.32])  # Dependent variable (task completion time)
    ms = np.array([0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0])

elif (haptic and not audio):
    print("haptic")
    x = np.array([4, 2, 3, 2, 4, 5, 3, 5, 3, 5, 4, 4, 3, 4, 4, 4, 4, 4, 3, 5, 4, 4, 3, 4]).reshape(-1, 1)  # Independent variable (user score)
    y = np.array([-1, -1, 197.27, 212.74, 212.74, 197.56, 526.55, 53.23, 57.61, 58.98, 58.98, 197.27, 326.15, 53.23, 326.15, 57.61, 526.55, 197.56, 268.41, 268.41, 91.46, 91.46, 88.5, 88.5])  # Dependent variable (task completion time)
    ms = np.array([0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0])

if imputation:
    if ignore_ms:
        mask = (y != -1) & (ms != 1)
        x_complete = x[mask]
        y_complete = np.where(y[mask] != -1, y[mask], np.mean(y[mask]))
    else:
        x_complete = x[y != -1]
        y_complete = np.where(y != -1, y, np.mean(y[y != -1]))
else:
    if ignore_ms:
        mask = (y != -1) & (ms != 1)
        x_complete = x[mask]
        y_complete = y[mask]
    else:
        x_complete = x[y != -1]
        y_complete = y[y != -1]

# Fit linear regression model
model = sm.OLS(y_complete, sm.add_constant(x_complete)).fit()

# Check the slope coefficient and p-value
slope_coefficient = model.params[1]
p_value = model.pvalues[1]

print(f"Slope Coefficient: {slope_coefficient}")
print(f"P-value: {p_value}")
print("lowest significance level: ", math.ceil((p_value*100)/5)*5)