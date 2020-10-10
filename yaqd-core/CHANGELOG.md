# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [2020.10.0]

### Added
- Support for nested named types

### Changed
- changed logging location to user log directory

## [2020.07.4]

### Changed
- Updated to fastavro 0.24.0 named schema behavior

## [2020.07.3]

### Added
- new testing submodule: provides decorators to run daemons in context of single function
- Now handle schema-defined types (e.g. ndarray)

### Fixed
- fixed tuple handling (e.g. get_channel_shapes) by pinning to fastavro>=0.23.6

## 2020.07.2

There are no actual code changes, this release is to update the release pipeline

### Changed
- New repo home: https://gitlab.com/yaq/yaq-python

## [2020.07.1]

### Changed
- distribute with `-` instead of `_`

## [2020.07.0]

### Fixed
- Unpacking of union types as message request parameters
- Correct python requires, allowing python 3.7

### Changed
- migrated to flit build system
- Less verbose log messages for avro unpacking and performing message calls

## [2020.06.3]

### Added
- `--protocol` entry point to print the avro protocol

### Changed
- removed `pkg_resources` in favor of path manipulation when accessing .avpr files
- Behavior of `VERSION` entry point, now prints module and package version, no individual daemon version

## [2020.06.2]

### Changed
- Remove msgpack based rpc, replace with Apache [Avro](https://yeps.yaq.fyi/107)
    - This is a breaking change which requires updates to daemon

## [2020.06.1]

### Added
- now explicity testing against Python 3.7, 3.8 and latest

### Fixed
- remove old (now incorrect) references to abstract daemons in README
- remove task.get_name feature which was introduced in Python 3.8 (fixing broken 3.7)

## [2020.06.0]

### Added
- added DiscreteHardware class, implementing new trait is-discrete

### Changed
- required methods for subclasses now raise NotImplementedError rather than having default fallbacks with undesired behavior
- `hardware` class futureproofed in case base daemon ever has state to save or load

### Removed
- entry points for `hardware` and `continuous-hardware`: use [yaqd-fakes](https://gitlab.com/yaq/yaqd-fakes) instead

### Fixed
- correctly handle shared-settings at startup

## [2020.05.2]

### Added
- Add CHANGELOG to MANIFEST.in

### Fixed
- correctly await and return `aread` and `areadline`

## [2020.05.1]

### Added
- added git branch information to daemon, package version
- added gitlab-ci testing stage for entry points

### Changed
- refactored gitlab-ci

### Fixed
- fixed _version attribute mypy type for abstract daemons

## [2020.05.0]

### Added
- added `get_version` as described in [YEP-105](https://yeps.yaq.fyi/105)
- added changelog
- logging level can be set with the `--log-level` and `--verbose` cli options [YEP-106](https://yeps.yaq.fyi/106)
- default configuration options for "log-level" and "log-to-file"
- added version entry point
- updated README

### Changed
- from now on, yaqd-core-python will use calendar-based versioning
- logging is now done with separate loggers per daemon (rather than per file) [YEP-106](https://yeps.yaq.fyi/106)

## [0.7.0]

### Added
- Add handling of ndarray type msgpack extension, see [YEP-110](https://yeps.yaq.fyi/110)

### Changed
- Uses msgpack RPC as described by [YEP-100](https://yeps.yaq.fyi/100) rather than JSON-RPC

## [0.6.0]

### Added
- Locks for aserial operations
- `awrite_then_read` method
- Restarting over the RPC interface

### Changed
- `config_filepath` changed to `get_config_filepath`

## Removed
- yaqd-base and yaqd-sensor entry points

## [0.5.0]

### Added
- hardware have `get_units` method
- new method `get_traits` (and associated class variable for defining implemented traits)
- hardware now have `set_relative` method
- `aserial` subpackage for asyncronous serial I/O

### Changed
- Limits now have a single range, rather than a list of ranges
- `out_of_limits` defaults to "closest", rather than "error"
- `defaults` now properly get preserved when subclassing

### Removed
- `get_lineage` method

## [0.4.1]

### Changed
- Fix bug in sensor assertion

## [0.4.0]

### Added
- yaqd-sensor entry point
- Doc building using pdoc (https://yaqd-core-python.yaq.fyi)
- Ability to shutdown individual daemons over the RPC

### Changed
- Clean up implementation of RPC protocol
- Channel information now three separate fields for "name", "units", and "shape", new methods to access each

### Removed
- "entry" top level configuration parameter no longer respected

## [0.3.1]

### Added
- Manifest file for distribution of the LICENSE and README

## [0.3.0]

### Added
- Communicate type annotations

### Changed
- Ensure parsing of multiple incomming requests at the same time
- Improved testing infrastructure

### Removed
- `set_action` decorator

## [0.2.1]

### Added
- Handling of UNIX Signals SIGTERM, SIGHUP, SIGINT
- [PEP-484](https://www.python.org/dev/peps/pep-0484/) Type Hints

### Changed
- Correct calls when running files directly
- Fix inf usage without importing
- Update distribution information

## [0.2.0]

### Added
- pre-commit hooks
- Add continuous integration
- Add version attribute
- Sensor daemon
- `get_lineage` method to see parents
- Hooks for connecting and disconnecting clients
- Logging infrastructure

### Changed
- Use "method" rather than "command"
- Use consistent names for classes, entry points

### Removed
- Client (see [yaqc-python](https://gitlab.com/yaq/yaqc-python) instead)

## [0.1.0]

### Initial release
- The base daemon implementation
- JSON-RPC implementation
- Generic Client
- Continuous hardware base daemon

[Unreleased]: https://gitlab.com/yaq/yaq-python/-/compare/yaqd-core-2020.10.0...master
[2020.10.0]: https://gitlab.com/yaq/yaq-python/-/compare/yaqd-core-2020.07.4...yaqd-core-2020.10.0
[2020.07.4]: https://gitlab.com/yaq/yaq-python/-/compare/yaqd-core-2020.07.3...yaqd-core-2020.07.4
[2020.07.3]: https://gitlab.com/yaq/yaq-python/-/compare/yaqd-core-2020.07.2...yaqd-core-2020.07.3
[2020.07.1]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v2020.07.0...v2020.07.1
[2020.07.0]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v2020.06.3...v2020.07.0
[2020.06.3]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v2020.06.2...v2020.06.3
[2020.06.2]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v2020.06.1...v2020.06.2
[2020.06.1]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v2020.06.0...v2020.06.1
[2020.06.0]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v2020.05.2...v2020.06.0
[2020.05.2]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v2020.05.1...v2020.05.2
[2020.05.1]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v2020.05.0...v2020.05.1
[2020.05.0]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v0.7.0...v2020.05.0
[0.7.0]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v0.6.0...v0.7.0
[0.6.0]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v0.5.0...v0.6.0
[0.5.0]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v0.4.1...v0.5.0
[0.4.1]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v0.4.0...v0.4.1
[0.4.0]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v0.3.1...v0.4.0
[0.3.1]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v0.3.0...v0.3.1
[0.3.0]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v0.2.1...v0.3.0
[0.2.1]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v0.2.0...v0.2.1
[0.2.0]: https://gitlab.com/yaq/yaqd-core-python/-/compare/v0.1.0...v0.2.0
[0.1.0]: https://gitlab.com/yaq/yaqd-core-python/-/tags/v0.1.0
