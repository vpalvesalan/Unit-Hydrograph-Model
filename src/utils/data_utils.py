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
        #Find length of each printing column
        dtypes = df.dtypes.astype(str).tolist()
        dtypes_len = max(len(dtype) for dtype in dtypes) + 1

        columns = df.columns.astype(str).tolist()
        columns_len = max(len(col) for col in columns) + 1
        if columns_len > 29:
            columns_len = 29

        # Print details for each column
        col_info = [' '*columns_len + ' Null Count  Dtype' + ' '*(dtypes_len-4) + 'First Values',
                    ' '*columns_len + ' ----------  -----' + ' '*(dtypes_len-4) + '-------------']
        for col in df.columns:
            col_edited = col
            null_count = df[col].isnull().sum()
            dtype = df[col].dtype
            first_values = df[col].head().values
            if len(col)>29:
                col_edited = col_edited[:27] + '...'

            # Convert first values to strings for better formatting
            first_values_str = ', '.join(map(str, first_values))
            col_info.append(f"{col_edited:<{columns_len}} {null_count:<10}  {str(dtype):<{dtypes_len}} [{first_values_str}]")
        
        # Print each column's info
        for col in col_info:
            print(col)
        return None