# Reddit Comment Analysis - Statistical Tests

This script analyzes comment data from the Reddit `/r/canada` subreddit to compare the number of comments posted during weekdays and weekends in the years 2012 and 2013. It applies various statistical tests to the data to determine whether the number of comments differs significantly between weekdays and weekends.

The script performs:
1. **Student's T-test** to compare the means of comment counts between weekdays and weekends.
2. **Normality tests** to check if the data follows a normal distribution.
3. **Levene's test** to check if the variances between the two datasets are equal.
4. **Data Transformation** (via square root transformation) to improve the data distribution before performing statistical tests.
5. **Weekly grouping** to check for patterns based on the year and week of the data.
6. **Mann-Whitney U-test** as a non-parametric alternative for testing differences between two independent samples.

---

## Requirements

- **Python 3.8+**
- **Dependencies**:
    - `numpy`
    - `pandas`
    - `scipy`
    - `datetime`

You can install the required dependencies using:

```bash
pip install numpy pandas scipy
