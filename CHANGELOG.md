# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to a modified version of [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Geometry releases will be tagged as `Descriptive_tag_v_X.Y.Z`.

## [Unreleased]

### Changed

- Bump gegede to version 0.8.0

### Removed

- Removed old gdml files from repo.

### Added

- generate complete ND geo with SAND provided with a Drift Chamber using `build_hall.sh sand_opt3_DRIFT1`

## [TDR_Production_geometry_v_1.0.3]

### Fixed

- Fixed use of TGeoManager::Import in scripts.

### Changed

- Changed drift length and ND gaps to reflect ND CAD gap lengths.
- `checkOverlaps.C` now takes an optional argument to choose the overlap checking method.
- CI now runs both types of overlap checks.

## [TDR_Production_geometry_v_1.0.2]

### Fixed

- Fixed Overlaps in TMS geometry.

### Changed
- `checkOverlaps.C` now uses sampling method.

## [TDR_Production_geometry_v_1.0.1]

### Changed

- Added production gdml with no LArActive to build script

## [TDR_Production_geometry_v_1.0]

### Changed

- Update `build_hall.sh` to build production geom with prod option
