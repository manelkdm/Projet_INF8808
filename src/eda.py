import pandas as pd

# load the data
df = pd.read_csv("nuforc_reports.csv")

# count the frequency of uniques of column "shape"

shape_counts = df["shape"].value_counts()

# sort the shape_counts in descending order

shape_counts = shape_counts.sort_values(ascending=False)

# convert the numbesr to percentage

shape_counts = shape_counts / shape_counts.sum()

# print(shape_counts)

# For every top N shape, calculate the total percentage of them
# N is a variable

for n in range(1, 11):
    top_n_shapes = shape_counts.head(n)
    print(top_n_shapes.sum())
