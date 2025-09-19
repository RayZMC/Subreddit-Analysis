import sys
import numpy as np
import pandas as pd
from scipy import stats
from datetime import date


OUTPUT_TEMPLATE = (
    "Initial T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann-Whitney U-test p-value: {utest_p:.3g}"
)


def main():
    reddit_counts = sys.argv[1]

    counts = pd.read_json(sys.argv[1], lines=True)
    
    # Filter the data to look only at values (1) in 2012 and 2013, and (2) in the /r/canada subreddit.
    counts = counts[(counts['subreddit'] == 'canada') & (counts['date'].dt.year.isin([2012, 2013]))]
    
    # Separate weekdays (0 to 4) and weekends (5 and 6)
    weekdays = counts[counts['date'].dt.weekday < 5].copy()
    weekends = counts[counts['date'].dt.weekday >= 5].copy()
    
    # -- Student's T-Test --
    # Using scipy.stats to do a T-test on the data to get a p-value
    p_value = stats.ttest_ind(weekdays['comment_count'], weekends['comment_count']).pvalue
    
    #print("T-test p-value:", p_value)
    # Trying stats.normaltest to see if the data is normally-distributed, and stats.levene to see if the two data sets have equal variances.
    weekdays_normality = stats.normaltest(weekdays['comment_count']).pvalue
    weekends_normality = stats.normaltest(weekends['comment_count']).pvalue
    initial_levene_p = stats.levene(weekdays['comment_count'], weekends['comment_count']).pvalue
    
    
    # -- Fix 1: Transforming the data since it was skewed -- 
    transformed_weekdays = np.sqrt(weekdays['comment_count'])
    transformed_weekends = np.sqrt(weekends['comment_count'])
    transformed_weekday_normality_p = stats.normaltest(transformed_weekdays).pvalue
    transformed_weekend_normality_p = stats.normaltest(transformed_weekends).pvalue
    transformed_levene = stats.levene(transformed_weekdays, transformed_weekends).pvalue
    
    
    # -- Fix 2: the Central Limit Theorem might save us --
    # Extract year and week number using isocalendar
    weekdays.loc[:, 'year'] = weekdays['date'].apply(lambda x: x.isocalendar()[0])
    weekdays.loc[:, 'week_number'] = weekdays['date'].apply(lambda x: x.isocalendar()[1])
    weekends.loc[:, 'year'] = weekends['date'].apply(lambda x: x.isocalendar()[0])
    weekends.loc[:, 'week_number'] = weekends['date'].apply(lambda x: x.isocalendar()[1])

    # Group by year and week number and calculate the mean
    weekdays_grouped = weekdays.groupby(['year', 'week_number'])['comment_count'].mean()
    weekends_grouped = weekends.groupby(['year', 'week_number'])['comment_count'].mean()

    # Check for normality and equal variance
    weekly_weekday_normality_p = stats.normaltest(weekdays_grouped).pvalue
    weekly_weekend_normality_p = stats.normaltest(weekends_grouped).pvalue
    weekly_levene_p = stats.levene(weekdays_grouped, weekends_grouped).pvalue

    # Applying T-test
    weekly_ttest_p = stats.ttest_ind(weekdays_grouped, weekends_grouped).pvalue
    
    
    # -- Fix 3 Mann-Whitney U-test --
    utest = stats.mannwhitneyu(weekdays['comment_count'], weekends['comment_count'], alternative='two-sided').pvalue
    
    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=p_value,
        initial_weekday_normality_p=weekdays_normality,
        initial_weekend_normality_p=weekends_normality,
        initial_levene_p=initial_levene_p,
        transformed_weekday_normality_p=transformed_weekday_normality_p,
        transformed_weekend_normality_p=transformed_weekend_normality_p,
        transformed_levene_p=transformed_levene,
        weekly_weekday_normality_p=weekly_weekday_normality_p,
        weekly_weekend_normality_p=weekly_weekend_normality_p,
        weekly_levene_p=weekly_levene_p,
        weekly_ttest_p=weekly_ttest_p,
        utest_p=utest,
    ))


if __name__ == '__main__':
    main()
