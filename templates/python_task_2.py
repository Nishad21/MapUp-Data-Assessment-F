import pandas as pd


def calculate_distance_matrix(df) -> pd.DataFrame:
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    distance_matrix = pd.DataFrame(index=df.index, columns=df.index)
    for id_start in df.index:
        for id_end in df.index:
            if id_start == id_end:
                distance_matrix.loc[id_start, id_end] = 0
            elif pd.isna(distance_matrix.loc[id_start, id_end]):
                distance = calculate_cumulative_distance(df, id_start, id_end)
                distance_matrix.loc[id_start, id_end] = distance
                distance_matrix.loc[id_end, id_start] = distance
    return distance_matrix


def calculate_cumulative_distance(df, id_start, id_end):
    direct_distance = df.loc[id_start, id_end]
    if pd.notna(direct_distance):
        return direct_distance

    intermediates = df.columns[df.loc[id_start, :].notna() & df.loc[:, id_end].notna()]
    if len(intermediates) == 0:
        return float('inf')

    cumulative_distance = 0
    for intermediate in intermediates:
        distance_A_to_intermediate = calculate_cumulative_distance(df, id_start, intermediate)
        distance_intermediate_to_B = calculate_cumulative_distance(df, intermediate, id_end)
        cumulative_distance += distance_A_to_intermediate + distance_intermediate_to_B
    return cumulative_distance


df = pd.read_csv("/Users/nishad/Desktop/MapUp-Data-Assessment-F/datasets/dataset-3.csv")
result_matrix = calculate_distance_matrix(df)
print(result_matrix)


def unroll_distance_matrix(distance_matrix) -> pd.DataFrame:
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

    for id_start in distance_matrix.index:
        for id_end in distance_matrix.columns:
            if id_start != id_end:
                distance = distance_matrix.loc[id_start, id_end]
                unrolled_df = unrolled_df.append({'id_start': id_start, 'id_end': id_end, 'distance': distance},
                                                 ignore_index=True)
    return unrolled_df


result_matrix = calculate_distance_matrix(df)
unrolled_df = unroll_distance_matrix(result_matrix)
print(unrolled_df)


def find_ids_within_ten_percentage_threshold(unrolled_df, reference_id) -> pd.DataFrame:
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    reference_rows = unrolled_df[unrolled_df['id_start'] == reference_id]
    average_distance = reference_rows['distance'].mean()

    lower_threshold = average_distance * 0.9
    upper_threshold = average_distance * 1.1
    within_threshold_rows = reference_rows[(reference_rows['distance'] >= lower_threshold) &
                                           (reference_rows['distance'] <= upper_threshold)]

    sorted_ids_within_threshold = within_threshold_rows['id_start'].unique()
    sorted_ids_within_threshold.sort()

    return sorted_ids_within_threshold


df = pd.read_csv("/Users/nishad/Desktop/MapUp-Data-Assessment-F/datasets/dataset-3.csv")
result_matrix = calculate_distance_matrix(df)
unrolled_df = unroll_distance_matrix(result_matrix)
reference_value = 1
result = find_ids_within_ten_percentage_threshold(unrolled_df, reference_value)
print(result)

def calculate_toll_rate(df) -> pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here

    return df


def calculate_time_based_toll_rates(df) -> pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

    return df
