import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logomaker

from logomaker.src.error_handling import LogomakerError
import pytest

def check_for_mistake(func, *args, **kw):
    """
    Run a function with the specified parameters and register whether
    success or failure was a mistake

    Parameters
    ----------
    func: (function or class constructor)
        An executable function to which *args and **kwargs are passed.

    Returns
    -------
    None
    """

    global global_fail_counter
    global global_success_counter

    # print test number
    test_num = global_fail_counter + global_success_counter
    print('Test # %d: ' % test_num, end='')
    #print('Test # %d: ' % test_num)

    # Run function
    obj = func(*args, **kw)
    # Increment appropriate counter
    if obj.mistake:
        global_fail_counter += 1
    else:
        global_success_counter += 1



# helper function to test parameters
def check_parameter(func, var_name, value, should_fail=True, **kwargs):
    """
    Tests if a function call with specific parameter
    value succeeds or fails as expected

    Parameters
    ----------
    func: (function)
        Executable to test. Can be function or class constructor.

    var_name: (str)
        Name of variable to test. If not specified, function is
        tested for success in the absence of any passed parameters.

    should_fail: (bool)
        True if function is expected to fail, False otherwise.

    **kwargs:
        Other keyword variables to pass onto func.

    Returns
    -------

    None.

    """
    kwargs[var_name] = value
    result = func(**kwargs)

# common success and fail lists
@pytest.fixture
def bool_fail_list():
    return [0,-1, 'True', 'x', 1]

@pytest.fixture
def bool_success_list():
    return [False, True]

# df inputs that successfully execute when entered into Logo.
@pytest.fixture
def good_crp_df():
    return logomaker.get_example_matrix('crp_energy_matrix', print_description=False)

@pytest.fixture
def good_prob_df():
    return logomaker.get_example_matrix('ss_probability_matrix', print_description=False)

@pytest.fixture
def random_df():
    return  pd.DataFrame(np.random.randint(0, 3, size=(10, 4)), columns=list('ACGT'))

# df inputs that fail when entered into Logo.
@pytest.fixture
def bad_df1():
    return 'x'

# parameterize Logo tests
@pytest.mark.parameterize("param,val,should_fail", [
    # test parameter df
    ('df', bool_fail_list, True),
    ('df', bad_df1, True )

])
def test_Logo_parameters(good_crp_df, param, val, should_fail):
    check_parameter(logomaker.Logo, 'df', val, should_fail)