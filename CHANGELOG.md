# Changelog

All notable changes to this project will be documented in this file.

## [1.2.3] - 2021-01-18

### Added

- Adding the `fwupdate` command to upgrade the Octowire firmware
- Adding the version in on the show modules output
- Implementing the 'version' command which displays framework, library and firmware version

## Changed

- Improve Linux commands running
- Improve installation and update process (properly delete previous version)

## [1.2.2] - 2021-01-15

### Added

## Changed

- Modules import "octowire" when "octowire-lib" dependency is processed

## [1.2.1] - 2021-01-07

### Added

## Changed

- Create a backup of both options and advanced_options dictionary when "run" command is called. This ensures to keep values readability after the Validator's call.

## [1.2.0] - 2020-10-16

### Added

- Added type 'float' to argument validation.

## Changed

- Improvement of options printing due to BeautifulTable upgrade.
- Change octowire-lib required version.
- Properly manage Octowire serial instance state (After running a module).
- Old advanced options (Octowire port, baudrate and detect) are now loaded from the configuration file.

## [1.1.3] - 2020-10-15

### Added

- Added type 'hextobytes' to argument validation.

## Changed

## [1.1.2] - 2020-10-15

### Added

## Changed

- Network issues catch when calling owfupdate.

## [1.1.1] - 2020-09-29

### Added

## Changed

- Improvement of system command execution.

## [1.1.0] - 2020-09-10

### Added

- Add file/path completion for set and setg command if the option requires a file

## Changed

- Improvement of system command execution for Windows system
- Asciinema video link updated

## [1.0.1] - 2020-07-06

### Added

- Added .gitignore file

### Changed

- Fixed typos