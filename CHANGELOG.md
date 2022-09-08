# Changelog

## [unreleased]

* Add `py.typed` file
* Make the module callable, allowing the concise `import savefigs; savefigs()`

## [0.2.0] (2021-10-22)

* Fix caller file name stem detection for ipykernel and detect file name
  in more situations ([#9](https://github.com/zmoon/savefigs/pull/9))
* `Figure.savefig` kwargs passed in via the `savefig_kwargs` kwarg
  don't replace the whole dict of defaults, just individual values

## [0.1.2] (2021-06-14)

* Fix `__version__` (+ now testing to make sure it matches the one in `pyproject.toml`)

## [0.1.1] (2021-06-14)

* Start changelog
* Fix pre-commit hook settings
* Improve docs (readme)
* Improve `savefigs()` argument type annotations
* Use Agg backend in tests (faster)

## [0.1.0] (2021-06-11)

Initial version



[unreleased]: https://github.com/zmoon/savefigs/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/zmoon/savefigs/releases/tag/v0.2.0
[0.1.2]: https://github.com/zmoon/savefigs/releases/tag/v0.1.2
[0.1.1]: https://github.com/zmoon/savefigs/releases/tag/v0.1.1
[0.1.0]: https://github.com/zmoon/savefigs/releases/tag/v0.1.0
