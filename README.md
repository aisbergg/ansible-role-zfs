# Ansible Role: `aisbergg.zfs`

This Ansible role installs the ZFS filesystem module, creates or imports zpools and manages ZFS datasets on Debian and CentOS systems.

## Requirements

- System needs to be managed with Systemd

## Role Variables

**Bold** variables are required.

| Variable | Default | Comments |
|----------|---------|----------|
| `zfs_redhat_style` | `kmod` | Style of ZFS module installation. Can be either kmod or dkms.  Applies only to RedHat systems. See [official documentation](https://openzfs.github.io/openzfs-docs/Getting%20Started/RHEL-based%20distro/index.html#rhel-based-distro) for information on DKMS and kmod version of openZFS. |
| `zfs_redhat_repo_dkms_url` | `http://download.zfsonlinux.org/`<br>`epel/{{ ansible_distribution_version }}/$basearch/` | Repository URL used for DKMS installation of ZFS. Applies only to RedHat systems. |
| `zfs_redhat_repo_kmod_url` | `http://download.zfsonlinux.org/`<br>`epel/{{ ansible_distribution_version }}/kmod/$basearch/` | Repository URL used for kmod installation of ZFS. Applies only to RedHat systems. |
| `zfs_debian_repo` | `{{ ansible_distribution_release }}-backports` | Repository used for installation. Applies only to Debian systems. |
| `zfs_service_import_cache_enabled` | `true` | Enable service to import ZFS pools by cache file. |
| `zfs_service_import_scan_enabled` | `false` | Enable service to import ZFS pools by device scanning. |
| `zfs_service_mount_enabled` | `false` if zfs_use_zfs_mount_generator else `true` }}"` | Enable service to mount ZFS filesystems using the ZFS built-in mounting mechanism. |
| `zfs_service_share_enabled` | `false` | Enable ZFS file system shares service. |
| `zfs_service_volume_wait_enabled` | `true` | Enable service to wait for ZFS Volume links in `/dev`. |
| `zfs_service_zed_enabled` | `true` | Enable ZFS Event Daemon (ZED) service. |
| `zfs_use_zfs_mount_generator` | `true` | Enable Systemd Mount Generator, to automatically mount volumes on boot with Systemd. |
| `zfs_kernel_module_parameters` | `{}` | Dictionary (key-value pairs) of ZFS kernel module parameters. See [official documentation](https://openzfs.github.io/openzfs-docs/Performance%20and%20Tuning/Module%20Parameters.html?highlight=zfs_arc_max) for available parameters. |
| `zfs_scrub_schedule` | `monthly` | Time schedule for zpool scrubs. Valid options can be looked up [here](https://www.freedesktop.org/software/systemd/man/systemd.time.html#Calendar%20Events). |
| `zfs_config_none_ioscheduler` | `[]` | Set IO scheduler for the listed HDDs to `none`. |
| `zfs_pools` | `[]` | List of ZFS Pools (zpools). |
| **`zfs_pools[].name`** |  | Name of the ZPool. |
| **`zfs_pools[].vdev`** |  | VDev definition for the ZPool. |
| `zfs_pools[].scrub` | `true` | Enable scrub for this ZPool. |
| `zfs_pools[].dont_enable_features` | `false` | Don't enable any feature. Use this in combination with `properties` to enable a custom set of features. |
| `zfs_pools[].properties` | `{}` | ZPool properties. |
| `zfs_pools[].filesystem_properties` | `{}` | Filesystem properties to apply to the whole ZPool. |
| `zfs_pools[].extra_import_options` | `""` | String of extra options to pass to the ZPool import command. |
| `zfs_pools[].extra_create_options` | `""` | String of extra options to pass to the ZPool create command. |
| `zfs_pools_defaults` | `{}` | Default properties for ZPools. The properties can be overwritten on a per ZPool basis. |
| `zfs_volumes` | `[]` | List of ZFS Volumes. |
| **`zfs_volume[].name`** |  | ZFS volume name. |
| `zfs_volume[].properties` | `{}` | Dictionary (key-value pairs) of volume properties to be set. |
| `zfs_volume[].state` | `present` | Whether to create (present), or remove (absent) the volume. |
| `zfs_volumes_properties_defaults` | `volblocksize: 8K`<br>`volsize: 1G`<br>`compression: lz4`<br>`dedup: false`<br>`sync: standard`<br> | Default properties for ZFS volumes. The properties can be overwritten on a per Volume basis. |
| `zfs_filesystems` | `[]` | List of ZFS Filesystems. |
| **`zfs_filesystem[].name`** |  | ZFS Filesystem name. |
| `zfs_filesystem[].properties` | `{}` | Dictionary (key-value pairs) of filesystem properties to be set. |
| `zfs_filesystem[].state` | `present` | Whether to create (present), or remove (absent) the filesystem. |
| `zfs_filesystems_properties_defaults` | `acltype: posix`<br>`atime: false`<br>`canmount: true`<br>`casesensitivity: sensitive`<br>`compression: lz4`<br>`dedup: false`<br>`normalization: formD`<br>`setuid: true`<br>`snapdir: hidden`<br>`sync: standard`<br>`utf8only: true`<br>`xattr: sa`<br> | Default properties for ZFS filesystems. The properties can be overwritten on a per FS basis. |
| `zfs_zrepl_config` | `{}` | Configuration for ZREPL. See the [official documentation](https://zrepl.github.io/configuration.html) for a list of available parameters. Examples can be found [here](https://github.com/zrepl/zrepl/tree/master/config/samples). |
| `zfs_zrepl_enabled` | `true` | Install and enable [ZREPL](https://github.com/zrepl/zrepl) for replication and snapshots. |
| `zfs_zrepl_redhat_repo_url` | `https://zrepl.cschwarz.com/`<br>`rpm/repo` | Repository URL used for ZREPL installation. Applies only to RedHat systems.  |
| `zfs_zrepl_debian_repo_url` | `https://zrepl.cschwarz.com/`<br>`apt` | Repository URL used for ZREPL installation. Applies only to Debian systems.  |


## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  vars:
    #
    # Service
    #

    # generate mount points using systemd
    zfs_use_zfs_mount_generator: true
    # use zfs_mount_generator but don't invoke ZED (Docker triggers it quite often)
    zfs_service_zed_enabled: false


    #
    # Configuration
    #

    # https://openzfs.github.io/openzfs-docs/Performance%20and%20Tuning/Module%20Parameters.html#zfs-module-parameters
    zfs_kernel_module_parameters:
      # use 1/4 of the memory for ZFS ARC
      zfs_arc_max: "{{ (ansible_memtotal_mb * 1024**2 * 0.25) | int }}"

    # schedule for ZFS scrubs
    zfs_scrub_schedule: monthly

    _zfs_performance_tuning_default:
      # store less metadata (still redundant in mirror setups)
      redundant_metadata: most
      # use standard behaviour for synchronous writes
      sync: standard

    _zfs_performance_tuning_async_only:
      # store less metadata (still redundant in mirror setups)
      redundant_metadata: most
      # turn synchronous writes into asynchronous ones
      sync: disabled

    _zfs_performance_tuning_ssd:
      # use standard behaviour for synchronous writes
      sync: standard
      # store less metadata (still redundant in mirror setups)
      redundant_metadata: most
      # optimize synchronous operations to write directly to disk instead of writing
      # to log. On HDDs this decreases the latency, but won't do much on SSDs.
      logbias: throughput

    _zfs_filesytems_properties:
      canmount: true
      snapdir: hidden

      # make ZFS behave like a Linux FS
      casesensitivity: sensitive
      normalization: formD
      utf8only: on
      setuid: true
      atime: false

      # enable use of ACLs
      acltype: posix
      xattr: sa

      # compression and deduplication
      compression: lz4
      dedup: false

    zfs_filesystems_properties_defaults: "{{
        _zfs_filesytems_properties | combine(
        _zfs_performance_tuning_async_only
      )}}"

    _zfs_volumes_properties:
      volblocksize: 8K
      volsize: 1G
      compression: lz4
      dedup: false

    # https://openzfs.github.io/openzfs-docs/man/7/zfsprops.7.html
    zfs_volumes_properties_defaults: "{{
        _zfs_volumes_properties | combine(
        _zfs_performance_tuning_async_only
      )}}"


    #
    # ZPools
    #

    zfs_pools:
    - name: rpool
      vdev: >-
        mirror
          r1
          r2
      scrub: true
      properties:
        ashift: 12
      filesystem_properties:
        # don't mount, just supply a base path for sub datasets
        canmount: off
        mountpoint: /

    - name: bpool
      vdev: >-
        mirror
          {{ _zfs_boot_partition1 }}
          {{ _zfs_boot_partition2 }}
      scrub: true
      properties:
        ashift: 12
        "feature@async_destroy": enabled
        "feature@bookmarks": enabled
        "feature@embedded_data": enabled
        "feature@empty_bpobj": enabled
        "feature@enabled_txg": enabled
        "feature@extensible_dataset": enabled
        "feature@filesystem_limits": enabled
        "feature@hole_birth": enabled
        "feature@large_blocks": enabled
        "feature@lz4_compress": enabled
        "feature@spacemap_histogram": enabled
      dont_enable_features: true
      filesystem_properties:
        canmount: off
        mountpoint: /boot


    #
    # Datasets
    #

    zfs_filesystems: "{{ _zfs_filesystems_system }}"
    _zfs_filesystems_system:
      # root
      - name: rpool/ROOT
        properties:
          canmount: off
          mountpoint: none
      - name: rpool/ROOT/default
        properties:
          canmount: noauto
          mountpoint: /

      - name: rpool/home
      - name: rpool/home/root
        properties:
          mountpoint: /root
      - name: rpool/var/lib/docker
      - name: rpool/var/log
      - name: rpool/var/spool
      - name: rpool/var/cache

      # boot
      - name: bpool/default
        properties:
          mountpoint: /boot


    #
    # Automatic Snapthots Using ZREPL
    #

    zfs_zrepl_enabled: true
    zfs_zrepl_config:
      jobs:
        - name: storage
          type: snap
          filesystems: {
            "rpool<": true,
            "rpool/var<": false,
          }
          snapshotting:
            type: periodic
            interval: 12h
            prefix: auto_
          pruning:
            keep:
              # prune automatic snapshots
              - type: grid
                # in first 24 hours keep all snapshots
                # in first 7 days 1 snapshot each day
                # in first month keep 1 snapshot each week
                # discard the rest
                # details see: https://zrepl.github.io/configuration/prune.html#policy-grid
                grid: 1x24h(keep=all) | 7x1d(keep=1) | 3x7d(keep=1)
                regex: "^auto_.*"

              # keep manual snapshots
              - type: regex
                regex: "^manual_.*"

  roles:
    - aisbergg.zfs
```

## License

MIT

## Author Information

Andre Lehmann (aisberg@posteo.de)
