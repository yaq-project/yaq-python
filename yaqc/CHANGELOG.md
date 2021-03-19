# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [2020.10.0]

### Added
- Support for nested named types
- Clients will reconnect on failure, with callbacks for action needed upon reconnect

## [2020.07.3]

### Changed
- Updated to fastavro 0.24.0 named schema behavior
- Open sockets in blocking mode instead of timeout

## [2020.07.2]

### Added
- Now handle schema-defined types (e.g. ndarray)

## 2020.07.1

There are no actual code changes, this release is to update the release pipeline

### Changed
- New repo home: https://gitlab.com/yaq/yaq-python

## [2020.07.0]

### Fixed
- Serialize based on the type of a request parameter, not the whole record
- Correct version of python supported (>=3.6)

## [2020.06.2]

### Changed
- moved to flit build system

### Removed
- no longer attempt to read protocol version

## [2020.06.1]
- Include handshake schema files

## [2020.06.0]

### Changed
- from now on, yaqc-python will use date based versioning
- updated README
- Remove msgpack, use Apache Avro, as described in [YEP-107](https://yeps.yaq.fyi/107)

## [0.2.0]

### Added
- msgpack ndarray extension

### Changed
- switch to msgpack, as described in [YEP-100](https://yeps.yaq.fyi/100)

## [0.1.2]

### Added
- mypy in precommit
- added README file

### Fixed
- added manifest, actually distribute license

## [0.1.1]

### Added
- gitlab-ci
- threading

### Fixed
- prevent failure on long messages

## [0.1.0]

### Added
- initial release

[Unreleased]: https://gitlab.com/yaq/yaq-python/-/compare/yaqc-2020.10.0...master
[2020.10.0]: https://gitlab.com/yaq/yaq-python/-/compare/yaqc-2020.07.3...yaqc-2020.10.0
[2020.07.3]: https://gitlab.com/yaq/yaq-python/-/compare/yaqc-2020.07.2...yaqc-2020.07.3
[2020.07.2]: https://gitlab.com/yaq/yaq-python/-/compare/yaqc-2020.07.1...yaqc-2020.07.2
[2020.07.0]: https://gitlab.com/yaq/yaqc-python/-/compare/v2020.06.2...v2020.07.0
[2020.06.2]: https://gitlab.com/yaq/yaqc-python/-/compare/v2020.06.1...v2020.06.2
[2020.06.1]: https://gitlab.com/yaq/yaqc-python/-/compare/v2020.06.0...v2020.06.1
[2020.06.0]: https://gitlab.com/yaq/yaqc-python/-/compare/v0.2.0...v2020.06.0
[0.2.0]: https://gitlab.com/yaq/yaqc-python/-/compare/v0.1.2...v0.2.0
[0.1.2]: https://gitlab.com/yaq/yaqc-python/-/compare/v0.1.1...v0.1.2
[0.1.1]: https://gitlab.com/yaq/yaqc-python/-/compare/v0.1.0...v0.1.1
[0.1.0]: https://gitlab.com/yaq/yaqc-python/-/tags/v0.1.0
