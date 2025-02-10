import pandas as pd

def glimpse(df: pd.DataFrame, return_df: bool = False) -> pd.DataFrame | None:

    """
    Provides a quick glimpse of a pandas DataFrame, displaying basic information 
    about its dimensions, column names, data types, and sample values. Optionally, 
    it can return the summary in a Pandas Data Frame.

    Parameters:
    -----------
    df : pd.DataFrame
        The pandas DataFrame to be glimpsed.

    return_df : bool, default False
        If set to True, the function will print out the number of rows, number of columns,
        and return a DataFrame containing the first few rows (transposed) along with their data types.
        If False, the function will print out the number of rows, number of columns, 
        and a preview of the first few values of each column along with their data type.

    Returns:
    --------
    pd.DataFrame or None
        If return_df is True, the function returns a DataFrame containing the first few rows 
        (transposed) of the original DataFrame along with the data types for each column.
        If return_df is False, the function prints the information to the console and returns None.
    
    Example:
    --------
    >>> glimpse(df)
    Rows: 100
    Columns: 5

    >>> glimpse(df, return_df=True)
    Rows: 100
    Columns: 5
       dtypes   0    1    2    3    4  
    column_name1  float64  ...  ...  ...  ...
    column_name2  object  ...  ...  ...  ...    
    """

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}", end = '\n' if return_df else '\n\n')

    if return_df:
        glimpse = (
            df.head()
            .T.assign(dtypes=df.dtypes)
            .loc[:, lambda x: sorted(x.columns, key=lambda col: 0 if col == "dtypes" else 1)]
        )
        return glimpse
    
    else:
        for col in df.columns:
            print(f"$ {col} <{df[col].dtype}> {df[col].head().values}")