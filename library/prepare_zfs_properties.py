#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule


def get_changed_properties(current, new, unchangeable=None):
    """Get the changed properties.

    :param current: Current properties
    :type current: dict
    :param new: New properties to be set
    :type new: dict
    :param unchangeable: Set of unchangeable properties, defaults to None
    :type unchangeable: set, optional
    :raises ValueError: If the value of an unchangeable property is tried to be changed
    :return: Changed properties
    :rtype: dict
    """
    unchangeable = unchangeable or set()
    changed_properties = {}
    for name, new_value in new.items():
        # convert bool types
        if isinstance(new_value, bool):
            new_value = "on" if new_value else "off"
        else:
            new_value = str(new_value)

        # check if new value differs from current one and if the value is changeable
        current_value = current.get(name, None)
        if current_value is None:
            # the dataset does not yet exist -> add new value
            changed_properties[name] = new_value

        elif new_value != current_value:
            if name in unchangeable:
                dataset_type = current["type"]
                raise ValueError(
                    "The value of {} property '{}' cannot be changed after creation."
                    .format(dataset_type, name))
            if name.startswith("feature@"):
                if (current_value in ["active", "enabled"]
                        and new_value == "disabled"):
                    changed_properties[name] = new_value
            else:
                changed_properties[name] = new_value

    return changed_properties


def main():
    # arguments definition
    module_args = dict(
        new_properties=dict(type="dict", required=True),
        current_properties=dict(type="dict", default={}),
        type=dict(type="str",
                  default="filesystem",
                  choices=["filesystem", "volume", "zpool"]),
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # parse arguments
    new_properties = module.params["new_properties"]
    current_properties = module.params["current_properties"]
    type_ = module.params["type"]

    result = {}

    try:
        if type_ in ["filesystem", "volume"]:
            dataset_type = current_properties.get("type", type_)
            unchangeable_properties = {
                "filesystem": {
                    "casesensitivity",
                    "encryption",
                    "keyformat",
                    "normalization",
                    "pbkdf2iters",
                    "utf8only",
                },
                "volume": {
                    "encryption",
                    "keyformat",
                    "pbkdf2iters",
                    "volblocksize",
                    "volsize",
                },
                "snapshot": {
                    "casesensitivity",
                    "encryption",
                    "keyformat",
                    "normalization",
                    "pbkdf2iters",
                    "utf8only",
                }
            }.get(dataset_type)
            result["properties"] = get_changed_properties(
                current_properties, new_properties, unchangeable_properties)
        else:
            result["properties"] = get_changed_properties(
                current_properties, new_properties)
    except ValueError as err:
        module.fail_json(msg=str(err))

    result["changed"] = (len(result["properties"]) > 0)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
