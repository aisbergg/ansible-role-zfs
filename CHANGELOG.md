# Changelog

All notable changes to this project will be documented in this file.

- [3.3.1 (2023-01-03)](#331-2023-01-03)
- [3.3.0 (2022-12-18)](#330-2022-12-18)
- [3.2.0 (2022-03-31)](#320-2022-03-31)
- [3.1.0 (2022-01-28)](#310-2022-01-28)
- [3.0.0 (2021-10-12)](#300-2021-10-12)
- [2.0.0 (2021-04-02)](#200-2021-04-02)
- [1.0.0 (2020-08-25)](#100-2020-08-25)

---

<a name="3.3.1"></a>
## [3.3.1](https://github.com/aisbergg/ansible-role-zfs/compare/v3.3.0...v3.3.1) (2023-01-03)

### Bug Fixes

- fix syntax of requirements file

### Chores

- explicitly set Ansible as verifier
- use fully-qualified collection name


<a name="3.3.0"></a>
## [3.3.0](https://github.com/aisbergg/ansible-role-zfs/compare/v3.2.0...v3.3.0) (2022-12-18)

### Bug Fixes

- linting
- replace deprecated decorator
- rename vars/centos.yml to redhat.yml

### Documentation

- document yum/dnf variable
- **README.md:** update documentation

### Features

- add option 'zfs_trim_schedule' to control the TRIM schedule for drives
- add option 'zfs_manage_repository' to control the package repository management
- add proxy support for yum/dnf repositories.


<a name="3.2.0"></a>
## [3.2.0](https://github.com/aisbergg/ansible-role-zfs/compare/v3.1.0...v3.2.0) (2022-03-31)

### Bug Fixes

- make udev tasks also work in check mode
- run ZED script only if it is enabled
- run mount generator tasks before service mgt tasks

### CI Configuration

- add branch explicitly to make Ansible import action happy
- bump Ansible Galaxy action version

### Chores

- don't use bump2version to include the CHANGELOG in the bump commit, it doesn't do a good job

### Documentation

- update links to manpages

### Features

- load kernel module on boot, even if no pools are created first


<a name="3.1.0"></a>
## [3.1.0](https://github.com/aisbergg/ansible-role-zfs/compare/v3.0.0...v3.1.0) (2022-01-28)

### Bug Fixes

- correct 'boolean' test name
- update zrepl PGP key

### CI Configuration

- fix automatic release and publish process

### Chores

- include changelog in bump commits


<a name="3.0.0"></a>
## [3.0.0](https://github.com/aisbergg/ansible-role-zfs/compare/v2.0.0...v3.0.0) (2021-10-12)

### CI Configuration

- add Github action for automatic releases

### Chores

- update changelog
- update development configs
- **.ansible-lint:** update linter config
- **.pre-commit-config.yaml:** bump pre-commit hook versions
- **CHANGELOG.tpl.md:** update changelog template
- **requirements.yml:** add role requirements

### Code Refactoring

- rename variables, add assertions and other modifications

### Documentation

- **README.md:** add proper documentation


<a name="2.0.0"></a>
## [2.0.0](https://github.com/aisbergg/ansible-role-zfs/compare/v1.0.0...v2.0.0) (2021-04-02)

### Code Refactoring

- major overhaul


<a name="1.0.0"></a>
## [1.0.0]() (2020-08-25)

Initial Release
