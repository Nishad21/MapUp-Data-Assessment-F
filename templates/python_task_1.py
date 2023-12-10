import pandas as pd


def generate_car_matrix(df) -> pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here

    # df = pd.read_csv("datasets/dataset-1.csv")

    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')

    car_matrix = car_matrix.fillna(0).astype(int)
    # car_matrix.values[[range(len(car_matrix))] * 2] = 0
    return car_matrix


df = pd.read_csv("/Users/nishad/Desktop/MapUp-Data-Assessment-F/datasets/dataset-1.csv")
result_matrix = generate_car_matrix(df)
print(result_matrix)


def get_type_count(df) -> dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]
    choices = ['low', 'medium', 'high']

    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')], labels=choices, right=False)

    type_count = df['car_type'].value_counts().to_dict()
    type_count = dict(sorted(type_count.items()))
    return type_count


df = pd.read_csv("/Users/nishad/Desktop/MapUp-Data-Assessment-F/datasets/dataset-1.csv")
result_dict = get_type_count(df)
print(result_dict)


def get_bus_indexes(df) -> list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    bus_mean = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    bus_indexes.sort()

    return bus_indexes


df = pd.read_csv("/Users/nishad/Desktop/MapUp-Data-Assessment-F/datasets/dataset-1.csv")
result_indices = get_bus_indexes(df)
print(result_indices)


def filter_routes(df) -> list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    route_avg_truck = df.groupby('route')['truck'].mean()
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    filtered_routes.sort()

    return filtered_routes


df = pd.read_csv("/Users/nishad/Desktop/MapUp-Data-Assessment-F/datasets/dataset-1.csv")
result_routes = filter_routes(df)
print(result_routes)


def multiply_matrix(matrix) -> pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    modified_matrix = matrix.copy()
    modified_matrix[modified_matrix > 20] *= 0.75
    modified_matrix[modified_matrix <= 20] *= 1.25

    modified_matrix = modified_matrix.round(1)
    return modified_matrix


modified_result_matrix = multiply_matrix(result_matrix)
print(modified_result_matrix)


def time_check(df) -> pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (
    `id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    completeness_series = df.groupby(['id', 'id_2']).apply(lambda group: check_pair_completeness(group)).reset_index(drop=True)

    return completeness_series


def check_pair_completeness(group):
    full_day_coverage = (group['end_timestamp'].max() - group['start_timestamp'].min()) >= pd.Timedelta(days=1)
    all_days_spanned = group['start_timestamp'].dt.dayofweek.nunique() == 7

    return full_day_coverage and all_days_spanned


df = pd.read_csv("/Users/nishad/Desktop/MapUp-Data-Assessment-F/datasets/dataset-2.csv")
completeness_series = time_check(df)
print(completeness_series)
