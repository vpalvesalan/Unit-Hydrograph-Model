import pandas as pd

def glimpse(df: pd.DataFrame, return_df: bool = False) -> pd.DataFrame | None:
    """
    Provides a quick glimpse of a pandas DataFrame, similar to pd.DataFrame.info().
    Displays the number of rows, columns, and the data types of each column, 
    along with the count of Null entries per column and the first 5 values of each column.

    Parameters:
    -----------
    df : pd.DataFrame
        The pandas DataFrame to be inspected.

    return_df : bool, default False
        If set to True, the function will return a DataFrame containing the first few rows (transposed)
        along with their data types. If False, the function will print out the glimpse to the console.

    Returns:
    --------
    pd.DataFrame or None
        If return_df is True, the function returns a DataFrame containing the first few rows 
        (transposed) of the original DataFrame along with the data types for each column.
        If return_df is False, the function prints the information to the console and returns None.
    """
    # Print the number of rows and columns
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    if return_df:
        # Optionally return the transposed preview with data types
        glimpse_df = (
            df.head()
            .T.assign(dtypes=df.dtypes)
            .loc[:, lambda x: sorted(x.columns, key=lambda col: 0 if col == "dtypes" else 1)]
        )
        return glimpse_df
    else:
        # Print details for each column
        col_info = ['                              Null Count   Dtype         First Values',
                    '                              ----------   ------        ------------']
        for col in df.columns:
            col_edited = col
            null_count = df[col].isnull().sum()
            dtype = df[col].dtype
            first_values = df[col].head().values
            if len(col)>29:
                col_edited = col_edited[:27] + '...'

            # Convert first values to strings for better formatting
            first_values_str = ', '.join(map(str, first_values))
            col_info.append(f"{col_edited:<29} {null_count:<11}  {str(dtype):<13} [{first_values_str}]")
        
        # Print each column's info
        for col in col_info:
            print(col)
        return None