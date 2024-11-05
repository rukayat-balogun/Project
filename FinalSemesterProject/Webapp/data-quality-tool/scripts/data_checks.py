import pandas as pd

def check_missing_values(df):
    """Returns the count of missing values per column."""
    return df.isnull().sum()


def check_data_types(df, expected_types):
    """Checks if columns have the expected data types."""
    mismatches = {}
    for column, expected_type in expected_types.items():
        if df[column].dtype != expected_type:
            mismatches[column] = df[column].dtype
    return mismatches


from scipy import stats

def check_outliers(df, column):
    """Identifies outliers in a specified column using z-scores."""
    z_scores = stats.zscore(df[column])
    outliers = df[(abs(z_scores) > 3)]
    return outliers


def check_duplicates(df):
    """Returns the number of duplicate rows."""
    return df.duplicated().sum()


def check_range(df, column, min_val, max_val):
    """Checks if values in a column fall within a specified range."""
    out_of_range = df[(df[column] < min_val) | (df[column] > max_val)]
    return out_of_range


def generate_quality_report(df):
    """Runs all quality checks and compiles results into a report."""
    report = {
        'missing_values': check_missing_values(df),
        'data_type_mismatches': check_data_types(df, {'age': 'int64', 'salary': 'float64'}),
        'outliers_age': check_outliers(df, 'age'),
        'duplicate_count': check_duplicates(df)
    }
    return report


def save_report(report, filename='data_quality_report.csv'):
    report_df = pd.DataFrame.from_dict(report, orient='index')
    report_df.to_csv(filename)
