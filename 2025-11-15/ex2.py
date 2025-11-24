def validate_schema(data: dict, schema: dict) -> dict:
    errors = []
    for key, expected_type in schema.items():
        if key not in data:
            errors.append(f"Missing key: {key}")
            continue
        value = data[key]
        if not isinstance(value, expected_type):
            errors.append(f"Incorrect type for key '{key}': expected {expected_type.__name__}, got {type(value).__name__}")
    return {"valid": len(errors) == 0, "errors": errors}

def validate_and_coerce_schema(data: dict, schema: dict[str, type]) -> dict:
    errors = []
    coerced_data = {}
    for key, expected_type in schema.items():
        if key not in data:
            errors.append(f"Missing key: {key}")
            continue
        value = data[key]
        if isinstance(value, expected_type):
            coerced_data[key] = value
            continue

        coerced_value = None
        try:
            if expected_type is bool and not isinstance(value, bool):
                if isinstance(value, str):
                    false_strings = {"false", "0", "no", "off", "disabled", "none", "", "null"}
                    true_strings = {"true", "1", "yes", "on", "enabled"}
                    coerced_value = True if value.strip().lower() in true_strings else False if value.strip().lower() in false_strings else None
            else:
                coerced_value = expected_type(value)
        except (ValueError, TypeError):
            errors.append(f"Cannot coerce key '{key}' to {expected_type.__name__}: invalid value {value}({type(value).__name__})")
            continue

        if expected_type is bool and coerced_value is None:
            errors.append(
                f"Cannot coerce key '{key}' to bool: unrecognized value {value!r} ({type(value).__name__})"
            )
            continue

        coerced_data[key] = coerced_value

    return {"valid": len(errors) == 0, "errors": errors, "data": coerced_data}
    