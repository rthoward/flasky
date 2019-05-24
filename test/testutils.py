from flasky.validator import ValidationError


def assert_models_equal(expected: dict, actual):
    for k, v in expected.items():
        actual_val = getattr(actual, k)
        assert v == actual_val


def assert_validation_errors(error_fields, fn):
    try:
        fn()
    except ValidationError as e:
        for field in error_fields:
            assert field in e.errors
