def assert_models_equal(expected: dict, actual):
    for k, v in expected.items():
        actual_val = getattr(actual, k)
        assert(v == actual_val)
