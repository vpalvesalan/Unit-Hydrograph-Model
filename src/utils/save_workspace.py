import pickle
import types

def save_workspace(filename):
    """
    Save the current global workspace to a file using pickle.

    This function copies the current global namespace and filters out:
      - Built-in variables (those whose names start with '__')
      - Imported modules
      - Callable objects (such as functions)
      - Objects that cannot be pickled

    The remaining variables are then serialized to the specified file using the
    pickle module. The saved file can later be loaded to restore the workspace
    in another session.

    Parameters:
    -----------
        filename (str): The path to the file where the workspace will be saved.

    Returns:
    --------
        None
    """
    # Copy the global namespace
    all_vars = globals().copy()

    # Filter out built-ins, modules, and callables.
    filtered_vars = {}
    for var_name, var_val in all_vars.items():
        if var_name.startswith('__'):
            continue
        if isinstance(var_val, types.ModuleType):
            continue
        if callable(var_val):
            continue
        try:
            # Test if the variable can be pickled
            pickle.dumps(var_val)
        except Exception:
            continue
        filtered_vars[var_name] = var_val

    with open(filename, 'wb') as f:
        pickle.dump(filtered_vars, f)

