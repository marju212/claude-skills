# Data Transformation with Pandas

## Category
Data Processing

## Description
Using Python's Pandas library to transform, clean, and manipulate tabular data. This skill covers common data transformation operations like filtering, grouping, aggregating, and reshaping data.

## Use Cases
- Cleaning and preparing data for analysis
- Converting data between different formats
- Aggregating data for reports
- Merging data from multiple sources
- Feature engineering for machine learning

## Prerequisites
- Python basics
- Understanding of tabular data structures (rows, columns)
- Familiarity with NumPy arrays (helpful but not required)
- Basic statistics knowledge

## Implementation

### Basic Example

```python
import pandas as pd
import numpy as np

# Create a sample DataFrame
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'age': [25, 30, 35, 28, 32],
    'city': ['New York', 'London', 'Paris', 'New York', 'London'],
    'salary': [70000, 80000, 90000, 75000, 85000]
}
df = pd.DataFrame(data)

# Filter rows
young_employees = df[df['age'] < 30]
print("Employees under 30:")
print(young_employees)

# Select specific columns
names_and_salaries = df[['name', 'salary']]

# Add a new column
df['salary_after_bonus'] = df['salary'] * 1.1

# Sort data
df_sorted = df.sort_values('salary', ascending=False)

# Group by and aggregate
avg_salary_by_city = df.groupby('city')['salary'].mean()
print("\nAverage salary by city:")
print(avg_salary_by_city)
```

### Advanced Example

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create a more complex dataset
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
n_records = len(dates)

sales_data = pd.DataFrame({
    'date': dates,
    'product': np.random.choice(['Widget A', 'Widget B', 'Widget C'], n_records),
    'region': np.random.choice(['North', 'South', 'East', 'West'], n_records),
    'quantity': np.random.randint(1, 100, n_records),
    'unit_price': np.random.uniform(10, 50, n_records),
    'customer_type': np.random.choice(['New', 'Returning'], n_records)
})

# Calculate revenue
sales_data['revenue'] = sales_data['quantity'] * sales_data['unit_price']

# Extract date components
sales_data['year'] = sales_data['date'].dt.year
sales_data['month'] = sales_data['date'].dt.month
sales_data['quarter'] = sales_data['date'].dt.quarter
sales_data['day_of_week'] = sales_data['date'].dt.day_name()

# Complex aggregations
monthly_summary = sales_data.groupby(['year', 'month', 'product']).agg({
    'revenue': ['sum', 'mean', 'count'],
    'quantity': 'sum'
}).round(2)

# Rename columns with multi-level index
monthly_summary.columns = ['_'.join(col).strip() for col in monthly_summary.columns.values]
monthly_summary = monthly_summary.reset_index()

# Pivot table for analysis
product_region_pivot = pd.pivot_table(
    sales_data,
    values='revenue',
    index='product',
    columns='region',
    aggfunc='sum',
    fill_value=0
)

# Calculate percentage of total
product_region_pivot['Total'] = product_region_pivot.sum(axis=1)
for col in ['North', 'South', 'East', 'West']:
    product_region_pivot[f'{col}_pct'] = (
        product_region_pivot[col] / product_region_pivot['Total'] * 100
    ).round(2)

# Window functions for running totals
sales_data = sales_data.sort_values('date')
sales_data['cumulative_revenue'] = sales_data.groupby('product')['revenue'].cumsum()

# Calculate rolling average
sales_data['revenue_7day_avg'] = (
    sales_data.groupby('product')['revenue']
    .rolling(window=7, min_periods=1)
    .mean()
    .reset_index(0, drop=True)
)

# Filtering with multiple conditions
high_value_sales = sales_data[
    (sales_data['revenue'] > 1000) &
    (sales_data['customer_type'] == 'New') &
    (sales_data['region'].isin(['North', 'East']))
]

# Join/merge data
product_info = pd.DataFrame({
    'product': ['Widget A', 'Widget B', 'Widget C'],
    'category': ['Electronics', 'Home', 'Electronics'],
    'weight_kg': [0.5, 1.2, 0.8]
})

enriched_data = sales_data.merge(product_info, on='product', how='left')

# Handle missing data
enriched_data['weight_kg'].fillna(enriched_data['weight_kg'].mean(), inplace=True)

# Create bins for categorical analysis
enriched_data['revenue_category'] = pd.cut(
    enriched_data['revenue'],
    bins=[0, 500, 1000, 2000, float('inf')],
    labels=['Low', 'Medium', 'High', 'Very High']
)

# Export results
monthly_summary.to_csv('monthly_summary.csv', index=False)
product_region_pivot.to_excel('product_region_analysis.xlsx')
```

## Best Practices
- **Use vectorized operations**: Avoid loops; use pandas/numpy operations for better performance
- **Chain operations carefully**: Break complex chains into steps for readability
- **Be mindful of memory**: Use appropriate data types (e.g., category for repeated strings)
- **Handle missing data explicitly**: Don't ignore NaN values; decide how to handle them
- **Use meaningful column names**: Make your dataframes self-documenting
- **Leverage built-in methods**: Pandas has many optimized methods; use them instead of manual implementations
- **Set proper index**: Use meaningful indices to make data access easier
- **Document transformations**: Comment complex transformations or create a data pipeline

## Common Pitfalls
- **Modifying copies instead of originals**: Use `inplace=True` or reassign the result
- **Chained assignment warnings**: Use `.loc[]` for setting values to avoid unexpected behavior
- **Not resetting index**: After groupby operations, remember to reset index if needed
- **Memory issues with large datasets**: Consider chunking or using Dask for very large data
- **Assuming data types**: Always check and convert data types as needed
- **Not handling time zones**: Be explicit about time zones when working with datetime data
- **Ignoring categorical data**: Use categorical type for columns with repeated values

## Related Skills
- [Data Visualization](./data-visualization.md)
- [SQL Queries](./database-queries.md)
- [Data Cleaning](./data-cleaning.md)

## Resources
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Python for Data Analysis by Wes McKinney](https://wesmckinney.com/book/)
- [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
- [Modern Pandas Tutorial](https://tomaugspurger.github.io/modern-1-intro.html)
