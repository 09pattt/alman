def sync_dictionaries(template: dict,
                      target: dict,
                      add_new_key: bool = True,
                      remove_current_key = True,
                      override_different_type: bool = True,
                      override_value: bool = False) -> dict:
    if add_new_key:
        for key, value in template.items():
            if key not in target:
                target[key] = value
            elif isinstance(value, dict) and isinstance(target.get(key), dict):
                sync_dictionaries(template=value,
                                  target=target[key],
                                  add_new_key=add_new_key,
                                  remove_current_key=remove_current_key,
                                  override_different_type=override_different_type,
                                  override_value=override_value)
            elif override_different_type and type(value) != type(target.get(key)):
                target[key] = value

    if override_value:
        for key, value in template.items():
            target[key] = value

    if remove_current_key:
        key_to_remove = []
        for key in target:
            if key not in template:
                key_to_remove.append(key)
        for key in key_to_remove:
            del target[key]

    return target