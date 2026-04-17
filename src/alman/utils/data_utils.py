def sync_dictionaries(template: dict, target: dict, add_new_key: bool = True, remove_current_key = True, override_value_to_dict: bool = True, override_value: bool = False) -> dict:
    if add_new_key:
        for key, value in template.items():
            if key not in target:
                target[key] = value
            elif override_value:
                target[key] = value
            elif isinstance(value, dict) and not isinstance(target.get(key), dict):
                if override_value_to_dict:
                    target[key] = value
            elif isinstance(value, dict) and isinstance(target.get(key), dict):
                sync_dictionaries(template=value, target=target[key], add_new_key=add_new_key, remove_current_key=remove_current_key)

    if remove_current_key:
        key_to_remove = []
        for key in target:
            if key not in template:
                key_to_remove.append(key)
        for key in key_to_remove:
            del target[key]

    return target