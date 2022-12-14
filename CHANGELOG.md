# Changelog

## [0.1.45] - 2023

### Changed

- `join_path()`
    - Removes illegal characters (`<>:"/\|?*`)

## [0.1.441] - 2023-1-9

### Changed

- `README.md`
    - URL to the logo

## [0.1.44] - 2023-1-9

### Added

- `README.md`
    - Anchor points to all functions
- A docstring to each function

### Changed

- `try-traceback()`
    - Returns `None` instead `traceback.format_exc()` if `except` is called
- `fprint()`
    - Takes `*args:Any` instead of just a single `string` as input

### Removed

- `FastDebugger()`
    - Completely removed from `py_basic_commands`
    - [Separate GitHub repo](https://github.com/RasseTheBoy/FastDebugger)
    - Unnecessary imports removed from `py_basic_commands`

## [0.1.43] - 2023-1-3

### Added

- `chunker()`
    - type hint returns `Any`
- New file
    - `TODO.md`
- New logo added to `README.md`

### Changed

- `chunker()`
    - returns `list` instead of `generator`
- `fd()`
    - changed from a `function` to a `class`
    - input set as *args
        - can take multiple variables
- New function name
        - `join_dir()` -> `join_path()`

## [0.1.42] - 2023-1-1

### Added

- New function
    - `write_json()`
    - `chunker()`
- `read_json()`
    - return type hint set as `Any`
- `write_file()`
    - takes to account if input is a numpy array

## [0.1.41] - 2022-12-30

### Changed

- `create_file_dir()`
    - returns `bool` if file or directory was created
        - return type hint set as `bool`

## [0.1.4] - 2022-12-30

### The JSON update!

### Added

- New functions
    - `create_json()`
    - `read_json()`
- from `typing` import
    - `Any`

### Removed

- from `typing` import
    - `List`, `Tuple`
- `read_file().try_reading()`
    - return type hint removed

### Changed

- `read_file()`
    - return type hint set as `Any`

## [0.1.32] - 2022-12-24

### Added

- `read_file()`
    - `remove_empty` function added back
        - Was accidentally removed
    - `ret_did_create` added back

### Changed

- `read_file()`
    - Better and more accurate hint typing
    - given input variable for `create_file_dir()`
        - `file` -> `f`
- `@func_timer()`
    - `time.time()` -> `time.perf_counter()`

## [0.1.31] - 2022-12-21

### Added

- `fprint()`
    - You can add the `end` function to the print
- `read_file()`
    - `strip` all lines (default: `True`)
        - Only works if `splitlines` is set as `True` (default: `True`)
    - Type hints for returned values
        - Also for `try_read()`

### Changed

- Variables changed
    - `dir` -> `d`
    - `file` -> `f`
    - `filename` -> `fnam`
- `read_file()`
    - Removed `ret_did_create`
    - Now returns both `lines` and `did_create` as `tuple`
        - Due to Pylance giving some errors if `ret_did_create` was used
    - Input variable `do_splitlines` -> `splitlines`

## [0.1.3] - 2022-12-12

### Added

- `read_file()`
    - Able not to split lines -> Returns `string`
    - Able to change `encoding` (default: `'utf-8'`)
- New function `write_file()`
- New function `fd()`
    - For fast debugging
    - New `dependency required`: `colored`

### Todo

- `README` add
    - `write_file()`
    - `fd()`

## [0.1.21] - 2022-12-12

### Added

- `read_file()` can now return if a file was created (set `ret_did_create`=`True`)

## [0.1.2] - 2022-12-12

### Added

- `finput()`
    - `text` variable to `'Input: '` if empty/`None` empty `''`
- `choose_from_list()`
    - Possible to choose more than one variable from list
    - Returns an empty list, instead of `None` (line: `110`)
- `remove_file_dir()`
    - Shows correct `error` messages for both `'dir'` and `'file'`
    - Returns `traceback.format_exc()` if `except` happens
- `@try_traceback`
    - Now returns `traceback.format_exc()`
- `@func_timer`
    - Able to return `time_delta`
    - `do_print` to all prints
- `README`
    - Examples added for all functions and decorators

### Changed

- `get_path_for_file()` ---> `get_dir_path_for_file()`
    - Updated `__init__.py`
- `get_dir_path_for_file()`
    - `return_val` ---> `ret_val`

## [0.1.1] - 2022-12-11

### Added

- Added `do_print` to a lot of `fprint()` functions
 - `create_file_dir()`
 - `remove_file_dir()`
 - `read_files()`

## [0.1.0] - 2022-12-11

### Added

- New function `remove_file_dir()`
- New function `get_path_for_file()`

### Changed

- Some tweaks to `create_file_dir()`

## [0.0.9] - 2022-12-11

### Added

- New function `read_file()`

## [0.0.8] - 2022-12-11

### Added

- New function `create_file_dir()`

## [0.0.7] - 2022-12-11

### Added

- New function `join_dir()`
    - Works `like os.path.join()`
- `@func_timer` now prints when timer begins

## [0.0.6] - 2022-12-09

### Added

- New decorator `@func_timer`
    - Times and prints how long a function took to run

## [0.0.5] - 2022-12-09

### Added

- `choose_until_correct` variable to `choose_from_list()`
    - Waits in a while loop, until a valid and in range index is given

## [0.0.4] - 2022-12-09

### Added

- New decorator `@try_traceback()`
- New function `choose_from_list()`

### Changed

- `better_input()` to `finput()`

### Todo

- Update `README`

## [0.0.3] - 2022-12-08

### Added

- `better_input()` to `__init__.py`

## [0.0.2] - 2022-12-08

### Added

- New function created -> `better_input()`
- A new variable (`flush`) was added to`fprint()`
- New`CHANGELOG` added to the project

#### New function created -> `better_input()`

Customize your input as you wish!

```
def better_input(text='', nl=True, use_end_addon=True, ret_type: type = str):
    if use_end_addon:
        text = f'{text}: '

    inpt = input(text)

    if nl:
        print()

    try:
        return ret_type(inpt)
    except:
        print(f'Couldn\'t return input {inpt} as {ret_type}')
        print(f'Input type: {type(inpt)}')
        print('Returning value as string')
        return inpt
```

Function variable table:

| Variable name     | What it does                      | Type |
| -------------     |:-------------:                    |:-------------:|
| text              | Text to use in `input`            | String
| nl                | Add newline after `input`         | Bool
| use_end_addon     | Add `: ` at the end of to `text` variable    | Bool
| ret_type          | Returns value as given type       | Type


#### A new variable (`flush`) was added to`fprint()`

<pre>
def fprint(text='', nl=True, <b>flush=False</b>):
    if nl:
        text = f'{text}\n'
    print(text, <b>flush=flush</b>)
</pre>

`flush` has a default value (`False`), so this can be left empty

#### New`CHANGELOG` added to the project


A `CHANGELOG` file is added to the project and it will get updated with every new version.

### TODO

- Edit `README`

### Edit `README`

The `README` should include a guide and examples of the new function (`better_input()`).


## [0.0.1] - 2022-12-03

### Added

Files created and added to [GitHub](https://github.com/RasseTheBoy/Py_Basic_Tools) and [PyPi](https://pypi.org/project/py-basic-commands/).