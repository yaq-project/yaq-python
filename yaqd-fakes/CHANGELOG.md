# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [2021.1.0]

### Changed
- updated avprs corresponding to recent yaq-traits changes

## [2020.10.0]

### Changed
- refactored based on new yaqd-core multiple inheritence pattern
- slow down loop speed for fake-continuous-hardware, fake-has-turret

## [2020.09.1]

### Added
- Added `fake-has-turret` daemon to yaqd_fakes

### Added
- Fake hardware now have configurable units

### Fixed
- Avoid cpu spike in `fake-continuous-hardware`

## [2020.07.4]

### Changed
- added `has-measure-trigger` trait to `fake-triggered-sensor`, see [YEP-310](https://yeps.yaq.fyi/310/)

## [2020.07.3]

### Added
- new daemon: yaqd-fake-triggered-sensor

## 2020.07.2

There are no actual code changes, this release is to update the release pipeline

### Changed
- New repo home: https://gitlab.com/yaq/yaq-python

## [2020.07.1]

### Changed
- distribute with `-` instead of `_`

## [2020.07.0]

### Fixed
- prepended "fake" to continuous hardware protocol name, as intended

## [2020.06.1]

### Fixed
- include avpr and toml files in the distributed version

## [2020.06.0]

### Added
- initial release

[Unreleased]: https://gitlab.com/yaq/yaq-python/-/compare/yaqd-fakes-2021.1.0...master
[2021.1.0]: https://gitlab.com/yaq/yaq-python/-/compare/yaqd-fakes-2020.10.0...yaqd-fakes-2021.1.0
[2020.10.0]: https://gitlab.com/yaq/yaq-python/-/compare/yaqd-fakes-2020.09.1...yaqd-fakes-2020.10.0
[2020.09.1]: https://gitlab.com/yaq/yaq-python/-/compare/yaqd-fakes-2020.07.4...yaqd-fakes-2020.09.1
[2020.07.4]: https://gitlab.com/yaq/yaq-python/-/compare/yaqd-fakes-2020.07.3...yaqd-fakes-2020.07.4
[2020.07.3]: https://gitlab.com/yaq/yaq-python/-/compare/yaqd-fakes-2020.07.2...yaqd-fakes-2020.07.3
[2020.07.1]: https://gitlab.com/yaq/yaqd-fakes/-/compare/v2020.07.0...v2020.07.1
[2020.07.0]: https://gitlab.com/yaq/yaqd-fakes/-/compare/v2020.06.1...v2020.07.0
[2020.06.1]: https://gitlab.com/yaq/yaqd-fakes/-/compare/v2020.06.0...v2020.06.1
[2020.06.0]: https://gitlab.com/yaq/yaqd-fakes/-/tags/v2020.06.0
