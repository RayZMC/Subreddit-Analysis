# Reddit Data Analysis

This repository explores Reddit comment datasets using statistical hypothesis testing,
data transformation, and distributed data processing with Apache Spark.

## Statistical Analysis

Analyzes comment activity in the `/r/canada` subreddit during 2012 and
2013 to investigate differences between weekday and weekend comment counts.

The analysis includes:

- **Student's t-test** to compare mean comment counts.
- **Normality tests** to assess data distributions.
- **Levene's test** to assess equality of variances.
- **Square-root transformation** to address skewness.
- **Weekly data aggregation** to reassess statistical assumptions.
- **Mann-Whitney U test** as a non-parametric alternative.
- **P-value calculations** to evaluate statistical significance.

## Reddit Average Scores (`reddit_averages.py`)

Uses PySpark to calculate the average comment score across subreddits
from the Reddit Comment Corpus.

The script demonstrates:

- JSON data ingestion using explicit DataFrame schemas.
- Data aggregation using Spark DataFrame operations.
- Calculation of average comment scores for each subreddit.
- Sorting and exporting results by subreddit name and average score.
- Writing processed results to CSV files.

## Reddit Relative Scores (`reddit_relative.py`)

Identifies the highest-scoring comments in each subreddit relative
to the subreddit's average comment score.

The script demonstrates:

- Data filtering and aggregation using PySpark DataFrames.
- Joining comment records with subreddit-level statistics.
- Calculating relative comment scores.
- Identifying authors with the highest relative comment scores.
- DataFrame caching to reduce redundant computations.
- Broadcast joins to optimize distributed data processing.
- Exporting analytical results to JSON.

## Technologies Used

- Python
- Pandas
- NumPy
- SciPy
- Apache Spark (PySpark)
- Jupyter Notebook

## Requirements

- Python 3.8+
- Java version compatible with your Apache Spark installation
- Apache Spark / PySpark

Install the required Python dependencies:

```bash
pip install numpy pandas scipy pyspark
```

## Usage

### Reddit Average Scores

```bash
spark-submit reddit_averages.py <input_directory> <output_directory>
```

### Reddit Relative Scores

```bash
spark-submit reddit_relative.py <input_directory> <output_directory>
```

The scripts require Reddit comment datasets in JSON format.
The statistical analysis uses daily subreddit comment counts,
while the PySpark exercises use individual comment records.
