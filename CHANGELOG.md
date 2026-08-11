# Changelog

All notable changes to this project are documented in this file.

This project follows semantic versioning where practical. The repository does not
currently have Git release tags, so versions below are reconstructed from the
commit history.

## [1.0.0] - 2026-08-11

First public-ready release with the 2026 data refresh, release metadata, and
repository quality gates.

### Added

- Added the 2026 Community Builders source export and processed dashboard data.
- Added `src/format_2026_data.py` to regenerate the processed 2026 dashboard CSV
  from `dashboard/data/anonymized_cb_data_2026_original.csv`.
- Added support for rows with unknown source countries by preserving them as
  `Unknown` with region `Unknown`.
- Added `VERSION` as the single source for the dashboard version.
- Added `CHANGELOG.md` with the project history reconstructed from Git.
- Added `.markdownlint.yaml` for Markdown documentation linting.
- Added pre-commit hooks for Python formatting, Python linting, Markdown linting,
  YAML/JSON validation, repository hygiene, Bandit security checks, and secret
  detection.
- Added README documentation for installing and running pre-commit.

### Changed

- Updated the dashboard to load `dashboard/data/anonymized_cb_data_2026.csv`.
- Updated the dashboard footer to display the app version from `VERSION`.
- Updated cohort ordering to include 2025 and 2026.
- Updated country-specific charts to exclude `Unknown` while keeping those rows
  in overall totals and non-country charts.
- Updated map country metadata for new real countries introduced by the 2026
  data.
- Updated setup documentation to run Shiny with `python -m shiny` from the active
  Python environment.
- Reformatted Python utilities and normalized data file line endings through the
  new pre-commit checks.

### Security

- Verified the 2026 data files contain categorical dashboard fields only.
- Added automated checks for private keys, AWS credentials, Bandit findings, and
  secret-like values.

## [0.3.0] - 2025-08-29

2025 data refresh and data-processing workflow.

### Added

- Added `dashboard/data/anonymized_cb_data_2025_original.csv` as the 2025 source
  export.
- Added `dashboard/data/anonymized_cb_data_2025.csv` as the processed 2025
  dashboard data.
- Added `src/format_2025_data.py` to clean country names, map regions, and write
  the processed dashboard CSV.
- Added `src/update_countries_metadata.py` to maintain map coordinate metadata.
- Added `src/test_country_counts.py` to verify country-count calculation.
- Added `src/verify_data.py` to summarize and validate processed dashboard data.

### Changed

- Renamed the original dashboard data from `anonymized_cb_data.csv` to
  `anonymized_cb_data_2024.csv`.
- Updated the dashboard to load the processed 2025 data file.
- Updated country metadata to calculate country counts dynamically from CB data
  instead of storing counts in `countries.csv`.
- Expanded map coordinate metadata for countries present in the 2025 refresh.

## [0.2.1] - 2025-07-31

Repository maintenance before the 2025 data refresh.

### Added

- Added Dependabot configuration for repository dependency maintenance.

### Changed

- Updated GitHub Funding metadata with the dashboard project URL.

## [0.2.0] - 2024-06-16

Dependency layout cleanup.

### Changed

- Moved `requirements.txt` into the `dashboard/` directory as
  `dashboard/requirements.txt`.
- Updated README setup instructions to install dependencies from the dashboard
  requirements file.

## [0.1.0] - 2024-05-28

Initial dashboard implementation.

### Added

- Added the Python Shiny dashboard application.
- Added Plotly charts for Community Builders by region, category, cohort,
  country, and cohort/category.
- Added an interactive `ipyleaflet` map with country markers and country-level
  category popups.
- Added the initial anonymized Community Builders data export.
- Added country coordinate metadata for map rendering.
- Added dashboard static assets, AWS Community Builders branding, backgrounds,
  logo, and favicon.
- Added dashboard screenshots for README documentation.
- Added initial README and CONTRIBUTING documentation.
- Added initial pre-commit configuration.

## [0.0.1] - 2024-05-24

Repository scaffold.

### Added

- Added the initial Git repository structure.
- Added `.gitignore`.
- Added the MIT `LICENSE`.
- Added the initial placeholder `README.md`.
