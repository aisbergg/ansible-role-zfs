#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule


def convert_values_and_remove_unchanged(new_properties, current_properties):
    result = {}
    for name, value in new_properties.items():
        # convert bool types
        if isinstance(value, bool):
            value = "on" if value else "off"
        else:
            value = str(value)

        current_value = current_properties.get(name, None)
        if current_value != value:
            result[name] = value

    return result


def prepare_zpool_properties(new_properties, current_properties):
    new_properties = convert_values_and_remove_unchanged(new_properties, current_properties)

    result = {}

    changeable_properties = [
        "altroot",
        "ashift",
        "autoexpand",
        "autoreplace",
        "autotrim",
        "bootfs",
        "cachefile",
        "comment",
        "dedupditto",
        "delegation",
        "failmode",
        "listsnapshots",
        "multihost",
        "readonly",
        "version",
    ]

    known_features = [
        "allocation_classes",
        "async_destroy",
        "bookmarks",
        "bookmark_v2",
        "device_removal",
        "edonr",
        "embedded_data",
        "empty_bpobj",
        "enabled_txg",
        "extensible_dataset",
        "filesystem_limits",
        "hole_birth",
        "large_dnode",
        "lz4_compress",
        "obsolete_counts",
        "project_quota",
        "resilver_defer",
        "sha512",
        "skein",
        "spacemap_histogram",
        "spacemap_v2",
        "userobj_accounting",
        "zpool_checkpoint",
    ]

    read_only_properties = [
        "allocated",
        "capacity",
        "checkpoint",
        "dedupratio",
        "expandsize",
        "fragmentation",
        "free",
        "freeing",
        "guid",
        "health",
        "leaked",
        "load_guid",
        "size",
    ]

    for name, value in new_properties.items():
        # property is changeable
        if name in changeable_properties:
            result[name] = value

        # property is a feature
        elif name.startswith("feature@"):
            if name in known_features:
                raise ValueError("Unknown feature '{}'".format(name))
            if current_properties:
                if current_properties[name] in ["active", "enabled"] and value != "disabled":
                    continue
                elif current_properties[name] == "disabled" and value == "disabled":
                    continue

            result[name] = value

        # property is read-only
        elif name in read_only_properties or name.startswith("unsupported@"):
            raise ValueError("Property '{}' is read-only".format(name))

        # property is unknwon
        else:
            raise ValueError("Unknown zpool property '{}'".format(name))

    return result


def prepare_dataset_properties(new_properties, current_properties, creation_type):
    new_properties = convert_values_and_remove_unchanged(new_properties, current_properties)

    dataset_type = current_properties.get("type", creation_type)
    result = {}

    read_only_properties = [
        "available",
        "compressratio",
        "createtxg",
        "creation",
        "clones",
        "defer_destroy",
        "encryptionroot",
        "filesystem_count",
        "keystatus",
        "guid",
        "logicalreferenced",
        "logicalused",
        "mounted",
        "objsetid",
        "origin",
        "receive_resume_token",
        "referenced",
        "refcompressratio",
        "snapshot_count",
        "type",
        "usedbychildren",
        "usedbydataset",
        "usedbyrefreservation",
        "usedbysnapshots",
        "userused",
        "userobjused",
        "userrefs",
        "groupused",
        "groupobjused",
        "projectused",
        "projectobjused",
        "written",
    ]

    # general dataset properties
    changeable_properties = [
        "checksum",
        "compression",
        "context",
        "copies",
        "dedup",
        "defcontext",
        "fscontext",
        "keylocation",
        "logbias",
        "mlslabel",
        "primarycache",
        "readonly",
        "redundant_metadata",
        "refreservation",
        "reservation",
        "rootcontext",
        "secondarycache",
        "snapdev",
        "snapshot_limit",
        "sync",
        "volmode",
    ]

    unchangeable_properties = {}

    if dataset_type == "filesystem":
        # add filesystem specific properties
        changeable_properties.extend([
            "aclinherit",
            "acltype",
            "atime",
            "canmount",
            "devices",
            "dnodesize",
            "exec",
            "filesystem_limit",
            "mountpoint",
            "nbmand",
            "overlay",
            "quota",
            "recordsize",
            "refquota",
            "relatime",
            "setuid",
            "sharenfs",
            "sharesmb",
            "snapdir",
            "special_small_blocks",
            "version",
            "vscan",
            "xattr",
            "zoned",
        ])

        unchangeable_properties = {
            "casesensitivity": None,
            "encryption": None,
            "keyformat": None,
            "normalization": None,
            "pbkdf2iters": None,
            "utf8only": None,
        }

    elif dataset_type == "volume":
        unchangeable_properties = {
            "encryption": None,
            "keyformat": None,
            "pbkdf2iters": None,
            "volblocksize": None,
            "volsize": "Changing 'volsize' can lead to data corruption. "\
                    "You have to do it manually if you really want to do it.",
        }

    elif dataset_type == "snapshot":
        # add snapshot specific properties
        changeable_properties.extend([
            "acltype",
            "devices",
            "exec",
            "nbmand",
            "setuid",
            "version",
            "xattr",
        ])

        unchangeable_properties = {
            "casesensitivity": None,
            "encryption": None,
            "keyformat": None,
            "normalization": None,
            "pbkdf2iters": None,
            "utf8only": None,
        }

    for name, value in new_properties.items():
        # property is changeable
        if name in changeable_properties:
            result[name] = value

        # property is unchangeable
        elif name in unchangeable_properties:
            # dataset exists -> check if property would change
            if current_properties:
                if value != current_properties[name]:
                    msg = unchangeable_properties[name]
                    if msg:
                        raise ValueError(msg)
                    else:
                        raise ValueError("The value of {} property '{}' cannot be changed after creation.".format(
                            dataset_type, name))

            # dataset does not exist yet -> ok to add
            else:
                result[name] = value

        # property is read-only
        elif name in read_only_properties:
            raise ValueError("{} property '{}' is read-only".format(dataset_type, name))

        # property is unkown
        else:
            raise ValueError("Unknown {} property '{}'".format(dataset_type, name))

    return result


def main():
    module_args = dict(new_properties=dict(type="dict", required=True),
                       current_properties=dict(type="dict", default={}),
                       type=dict(type="str", default="filesystem", choices=["filesystem", "volume", "zpool"]))
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    new_properties = module.params["new_properties"]
    current_properties = module.params["current_properties"]
    type_ = module.params["type"]

    result = {}

    try:
        if type_ in ["filesystem", "volume"]:
            result["properties"] = prepare_dataset_properties(new_properties, current_properties, type_)
        else:
            result["properties"] = prepare_zpool_properties(new_properties, current_properties)
    except ValueError as ve:
        module.fail_json(msg=str(ve))

    result["changed"] = (len(result["properties"]) > 0)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
