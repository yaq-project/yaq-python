# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [2023.6.0]

### Added
- new fake-furnace daemon, useful for prototyping chemical engineering setups
- new fake-has-transformed-position daemon

### Changed
- moved to hatchling build system

## [2022.5.0]

### Changed
- moved to github
- rerendered avprs for updated has-position trait

## [2022.3.1]

### Added
- fake camera daemon (has mapping that produces a 2D image with indexed axes)

## [2022.3.0]

### Fixed
- Corrected links for fake-continuous-hardware and fake-has-turret
- rerendered avprs for sensors so that measurement_id travels as int

## [2021.10.0]

### Added
- Rerender avprs with [YEP 111](https://yeps.yaq.fyi/111) properties included

## [2021.8.0]

### Fixed
- add shape to fake-spectrometer channel

## [2021.3.0]

### Added
- new daemon fake-is-sensor, implementing sensor without software trigger

### Changed
- Updated fake-has-turret for string identifiers rather than int
- all avprs updated based on recent traits change

## [2021.2.0]

### Added
- new daemon "fake-spectrometer" implementing new has-mapping trait, see [YEP-311](https://yeps.yaq.fyi)

### Changed
- random_wak for fake-triggered-sensor is now heavy, weighted to center of dynamic range

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

[Unreleased]: https://github.com/yaq-project/yaq-python/compare/yaqd-fakes-2023.6.0...main
[2023.6.0]: https://github.com/yaq-project/yaq-python/compare/yaqd-fakes-2022.5.0...yaqd-fakes-2023.6.0
[2022.5.0]: https://github.com/yaq-project/yaq-python/compare/yaqd-fakes-2022.3.1...yaqd-fakes-2022.5.0
[2022.3.1]: https://github.com/yaq-project/yaq-python/compare/yaqd-fakes-2022.3.0...yaqd-fakes-2022.3.1
[2022.3.0]: https://github.com/yaq-project/yaq-python/compare/yaqd-fakes-2021.10.0...yaqd-fakes-2022.3.0
[2021.10.0]: https://github.com/yaq-project/yaq-python/compare/yaqd-fakes-2021.8.0...yaqd-fakes-2021.10.0
[2021.8.0]: https://github.com/yaq-project/yaq-python/compare/yaqd-fakes-2021.3.0...yaqd-fakes-2021.8.0
[2021.3.0]: https://github.com/yaq-project/yaq-python/compare/yaqd-fakes-2021.2.0...yaqd-fakes-2021.3.0
[2021.2.0]: https://github.com/yaq-project/yaq-python/compare/yaqd-fakes-2021.1.0...yaqd-fakes-2021.2.0
[2021.1.0]: https://github.com/yaq-project/yaq-python/compare/yaqd-fakes-2020.10.0...yaqd-fakes-2021.1.0
[2020.10.0]: https://github.com/yaq-project/yaq-python/compare/yaqd-fakes-2020.09.1...yaqd-fakes-2020.10.0
[2020.09.1]: https://github.com/yaq-project/yaq-python/compare/yaqd-fakes-2020.07.4...yaqd-fakes-2020.09.1
[2020.07.4]: https://github.com/yaq-project/yaq-python/compare/yaqd-fakes-2020.07.3...yaqd-fakes-2020.07.4
[2020.07.3]: https://github.com/yaq-project/yaq-python/compare/yaqd-fakes-2020.07.2...yaqd-fakes-2020.07.3
[2020.07.1]: https://gitlab.com/yaq/yaqd-fakes/compare/-/v2020.07.0...v2020.07.1
[2020.07.0]: https://gitlab.com/yaq/yaqd-fakes/compare/-/v2020.06.1...v2020.07.0
[2020.06.1]: https://gitlab.com/yaq/yaqd-fakes/compare/-/v2020.06.0...v2020.06.1
[2020.06.0]: https://gitlab.com/yaq/yaqd-fakes/-/tags/v2020.06.0
