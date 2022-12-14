import traceback, json

from functools  import wraps
from shutil     import rmtree
from typing     import Any, Optional
from time   import perf_counter
from os     import mkdir, listdir, remove

def try_traceback(skip_traceback=False):
    """Decorator to catch and handle exceptions raised by a function.
    
    Parameters:
    - `skip_traceback` (bool): Whether to skip printing the traceback information.
    
    Returns:
    - `function`: The decorated function.
    """

    def try_except(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                if not skip_traceback:
                    fprint(traceback.format_exc())
                return None
        return wrapper
    return try_except


def func_timer(ret_time=False, do_print=True):
    """Decorator to measure the runtime of a function.
    
    Parameters:
    - `ret_time` (bool): Whether to return the time taken by the function in addition to its return value.
    - `do_print` (bool): Whether to print the time taken by the function.
    
    Returns:
    - `function`: The decorated function.
    """

    def timer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            fprint('Function timer started', do_print=do_print)
            time_start = perf_counter()
            ret_val = func(*args, **kwargs)
            time_delta = perf_counter() - time_start
            fprint(f'Function {func.__name__}{args} {kwargs} Took {time_delta:.4f} seconds to run', do_print=do_print)
            if ret_time:
                return ret_val, time_delta
            return ret_val
        return wrapper
    return timer


def fprint(*args:Any, nl:bool=True, flush:bool=False, do_print:bool=True, end:Optional[str]=None) -> None:
    """Print one or more objects to the console, with optional newline, flushing, and ending characters.
    
    Parameters:
    - `args` (*Any): One or more objects to print.
    - `nl` (bool): Whether to append a newline character to the output.
    - `flush` (bool): Whether to flush the output buffer.
    - `do_print` (bool): Whether to actually print the output.
    - `end` (str | None): The string to print at the end of the output.
    """

    if do_print:
        if not args:
            print('')

        for arg in args:
            if nl:
                arg = f'{arg}\n'

            print(arg, end=end, flush=flush)


def finput(text:str='', nl:bool=True, use_suffix:bool=True, ret_type:type=str):
    """Get input from the user and return it as a specified type.
    
    Parameters:
    - `text` (str): The text to prompt the user with. Default is an empty string.
    - `nl` (bool): Whether to append a newline character after the input. Default is True.
    - `use_suffix` (bool): Whether to append a colon character to the end of the prompt text. Default is True.
    - `ret_type` (type): The type to return the input as. Default is `str`.
    
    Returns:
    - The input value, converted to the specified type. If the conversion fails, the value is returned as a string.
    """

    if not text:
        text = 'Input: '
    elif use_suffix and text.rstrip()[-1] != ':':
        text = f'{text}: '

    inpt = input(text)

    if nl:
        print()

    try:
        return ret_type(inpt)
    except:
        print(f'Couldn\'t return input {inpt} as {ret_type}')
        print(f'Input type: {type(inpt)}')
        fprint('Returning value as string')
    return inpt


def enter_to_continue(text:str='', nl:bool=True, use_suffix:bool=True) -> bool:
    """Prompt the user to press the enter key to continue.
    
    Parameters:
    - `text` (str): The text to prompt the user with.
    - `nl` (bool): Whether to append a newline character after the input.
    - `use_suffix` (bool): Whether to append '(press enter to continue)' to the end of the prompt text.
    
    Returns:
    - `bool`: True if the user pressed the enter key, False otherwise.
    """

    if text and use_suffix:
        text = f'{text} (press enter to continue) '

    elif not text and use_suffix:
        text = 'Press enter to continue... '
    
    inpt = input(text)
    
    if nl:
        print()

    return not any(inpt)


def choose_from_list(_array:Any, header_text:str='', header_nl:bool=False, input_text:str='Input index: ', choose_total:int=1, start_num:int=0, choose_until_correct:bool=True) -> list:
    """Prompt the user to choose one or more values from a list.
    
    Parameters:
    - `_array` (Any): The list of values to choose from.
    - `header_text` (str): The text to display as a header.
    - `header_nl` (bool): Whether to append a newline character after the header.
    - `input_text` (str): The text to prompt the user with.
    - `choose_total` (int): The number of values to choose. 
    - `start_num` (int): The number to start the indexing from.
    - `choose_until_correct` (bool): Whether to keep prompting the user until a correct input is given.
    
    Returns:
    - `list`: A list of the chosen values.
    """

    if not header_text:
        if choose_total == 1:
            header_text = '---Choose 1 value---'
        else:
            header_text = f'---Choose {choose_total} values---'

    fprint(header_text, nl=header_nl)

    for indx, val in enumerate(_array):
        print(f'({indx+start_num}) {val}')
    print()

    while True:
        inpt_indx = finput(input_text, ret_type=str)
        try:
            inpt_indx = tuple(int(x) for x in inpt_indx.split())

            if any({x<start_num for x in inpt_indx}):
                raise IndexError

            return [_array[x - start_num] for x in inpt_indx]

        except IndexError:
            print('Given index is out of range')
            fprint(f'Value has to be between: {start_num}-{start_num+len(_array)-1}')
        except:
            fprint(f'Input not a valid index: {inpt_indx}')

        if not choose_until_correct:
            return []


def read_file(file_path, create:bool=False, ret_did_create:bool=False, splitlines:bool=True, remove_empty:bool=True, strip:bool=True, encoding:str='utf-8', do_print:bool=True) -> Any:
    """Read the contents of a file.
    
    Parameters:
    - `file_path` (str): The path to the file to read.
    - `create` (bool): Whether to create the file if it does not exist.
    - `ret_did_create` (bool): Whether to return a tuple of the file contents and a bool indicating whether the file was created.
    - `splitlines` (bool): Whether to split the file contents into a list of lines.
    - `remove_empty` (bool): Whether to remove empty lines when `splitlines` is True.
    - `strip` (bool): Whether to strip leading and trailing whitespace from each line when `splitlines` is True.
    - `encoding` (str): The encoding to use when reading the file.
    - `do_print` (bool): Whether to print information about the file reading process.
    
    Returns:
    - `Any`: If `ret_did_create` is True, a tuple containing the file contents and a bool indicating whether the file was created. Otherwise, the file contents.
    """
    
    def try_reading(did_create:bool=False):
        lines: list[str] | str = []
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.read()
            if splitlines:
                lines = lines.splitlines()
                if remove_empty:
                    lines = [x for x in lines if x != '']
                if strip:
                    lines = [x.strip() for x in lines]
            return lines, did_create
        except FileNotFoundError:
            fprint(f'File not found: {file_path}')
            if create:
                create_file_dir('f', file_path, force=True, do_print=do_print)
                return try_reading(True)
        return lines, did_create

    lines,did_create = try_reading()

    if ret_did_create:
        return lines,did_create
    return lines


def write_file(text:Any, file_path:str, append:bool=False, create:bool=True, encoding:str='utf-8', do_print:bool=True) -> bool:
    """Write text to a file.
    
    Parameters:
    - `text` (Any): The text to write. Can be a string, list, tuple, set or a numpy.array.
    - `file_path` (str): The path to the file to write to.
    - `append` (bool): Whether to append the text to the end of the file.
    - `create` (bool): Whether to create the file if it does not exist.
    - `encoding` (str): The encoding to use when writing the file.
    - `do_print` (bool): Whether to print information about the file writing process.
    
    Returns:
    - `bool`: Whether the file was created.
    """

    if text.__class__.__name__ == 'ndarray':
        text = text.tolist()
    
    if text.__class__.__name__ in ('list', 'tuple', 'set'):
        text = '\n'.join(text)

    lines, did_create = read_file(file_path, create:=create, ret_did_create=True, remove_empty=False, splitlines=False, do_print=do_print)

    try:
        if not did_create and lines[-1] != '\n':
            text = '\n' + text 
    except IndexError:
        pass
    except Exception:
        print(traceback.format_exc())

    if append:
        mode = 'a'
    else:
        mode = 'w'

    with open(file_path, mode=mode, encoding=encoding) as f:
        f.write(text + '\n')

    return did_create


def create_file_dir(do:str, do_path:str, force:bool=False, do_print:bool=True) -> bool:
    """Create a file or directory at the specified path.
    
    Parameters:
    - `do` (str): Whether to create a `'d'`irectory or a `'f'`ile.
    - `do_path` (str): The path to create the file or directory at.
    - `force` (bool): Whether to force the creation of the file or directory by deleting any existing file or directory with the same name.
    - `do_print` (bool): Whether to print information about the file or directory creation process.
    
    Returns:
    - `bool`: Whether the file or directory was created.
    """

    def create_dir():
        try:
            mkdir(do_path)
            fprint(f'Directory created: {do_path}', do_print=do_print)
            return True
        except FileExistsError:
            fprint(f'Directory aleady exists: {do_path}', nl=not force, do_print=do_print)
            if force:
                rmtree(do_path)
                fprint(f'Directory removed: {do_path}', nl=False, do_print=do_print)
                return create_dir()

    if do == 'd': # Directory
        return create_dir()
    
    elif do == 'f': # File
        file_dir, filename = get_dir_path_for_file(do_path)
        files_in_path = listdir(file_dir)

        if force or filename not in files_in_path:
            try:
                open(do_path, 'w', encoding='utf-8').close()
                fprint(f'File created: {do_path}', do_print=do_print)
                return True
            except FileExistsError:
                fprint(f'File already exists: {do_path}', do_print=do_print)
                return False
        elif filename in files_in_path:
            fprint(f'File already exists: {do_path}', do_print=do_print)
            return False


@try_traceback(skip_traceback=True)
def remove_file_dir(do:str, do_path:str, force:bool=False, do_print:bool=True) -> bool:
    """Remove a file or directory at the specified path.
    
    Parameters:
    - `do` (str): Whether to remove a `'d'`irectory or a `'f'`ile.
    - `do_path` (str): The path to the file or directory to remove.
    - `force` (bool): Whether to force the removal of the file or directory.
    - `do_print` (bool): Whether to print information about the file or directory removal process.
    
    Returns:
    - `bool`: Whether the file or directory was removed.
    """

    if do == 'd': # Directory
        try:
            dir_content = listdir(do_path)
        except FileNotFoundError:
            fprint(f'Directory path not found: {do_path}', do_print=do_print)

        if not dir_content or force:
            rmtree(do_path)
            fprint(f'Directory removed: {do_path}', do_print=do_print)
            return True
            
        elif dir_content:
            fprint(f'Directory is not empty, not removing: {do_path}', do_print=do_print)
            return False
        
        else:
            return False

    elif do == 'f': # File
        lines = read_file(do_path)
        if lines and not force:
            fprint(f'File is not empty, not removing: {do_path}', do_print=do_print)
            return False
        remove(do_path)
        fprint(f'File removed: {do_path}', do_print=do_print)
        return True


def get_dir_path_for_file(file_path:str, ret_val='a') -> Any:
    """Get the directory path and filename for a file.
    
    Parameters:
    - `file_path` (str): The path to the file.
    - `ret_val` (str): Whether to return the `'d'`irectory path, `'fnam'`e of the file, or `'a'`ll (default).
    
    Returns:
    - `Any`: If `ret_val` is `'d'`, the directory path. If `ret_val` is `'fnam'`, the filename. Otherwise, a tuple containing the directory path and the filename.
    """

    dir_path = file_path.replace('\\', '/').split('/')
    if len(dir_path) == 1:
        dir_path = None
        filename = file_path
    else:
        filename = dir_path.pop()
        dir_path = '/'.join(dir_path)

    if ret_val == 'd': # Directory
        return dir_path
    elif ret_val == 'fnam': # Filename
        return filename

    return dir_path, filename


def join_path(*args:str, join_with='/', dir_end:bool=False):
    r"""Join path segments together, removing certain characters (`<>:"/\|?*`) and adjust for correct slash direction.

    Parameters:
    - `*args`: One or more path segments to join
    - `join_with`: The separator to use when joining the path segments
    - `dir_end`: Specify whether to add join_with character at the end of the returned path

    Return:
    A `string` representing the joined path
    """
    
    def split_join(var:str, split_with:str=' '):
        return join_with.join(var.split(split_with))

    new_args = []
    for arg in args:
        arg = split_join(split_join(arg, '\\'), '/')
        arg = arg.translate({ord(c): None for c in '<>:"|?*'})

        new_args.append(arg)

    out_path = join_with.join(new_args)

    if dir_end:
        out_path += join_with

    return out_path


def chunker(seq, size:int) -> Any:
    """Split a sequence into chunks of the specified size.
    
    Parameters:
    - `seq` (Any): The sequence to split. Can be a list, tuple, or any other iterable object.
    - `size` (int): The size of the chunks.
    
    Returns:
    - `Any`: A list of chunks of the specified size.
    """

    return [seq[pos:pos + size] for pos in range(0, len(seq), size)]


def create_json(filepath:str, force:bool=False, do_print:bool=True) -> bool:
    """Create a new empty JSON file.
    
    Parameters:
    - `filepath` (str): The path for the new JSON file.
    - `force` (bool): Whether to overwrite any existing file with the same name.
    - `do_print` (bool): Whether to print information about the file creation process.
    
    Returns:
    - `bool`: Whether the file was created.
    """

    did_create = create_file_dir('f', filepath, force=force, do_print=do_print)
    if did_create:
        open(filepath, 'w').write(json.dumps({}, indent=4))
    return did_create


def read_json(filepath:str) -> Any:
    """Read data from a JSON file.
    
    Parameters:
    - `filepath` (str): The path of the JSON file to read from.
    
    Returns:
    - `Any`: The data from the JSON file, as a dictionary or list.
    """

    try:
        with open(filepath, 'r') as f:
            file_data = json.load(f)
        return file_data
    except FileNotFoundError:
        fprint(f'File not found: {filepath}')
    except json.decoder.JSONDecodeError:
        fprint(f'File cannot be read as a JSON: {filepath}')
    except Exception:
        fprint(traceback.format_exc())


def write_json(data:Any, filepath:str, indent:int=4, force:bool=False, do_print:bool=True):
    """Write data to a JSON file.
    
    Parameters:
    - `data` (Any): The data to write to the JSON file. This can be a dictionary, list, or a string representation of JSON.
    - `filepath` (str): The path of the JSON file to write to.
    - `indent` (int): The number of spaces to use for indentation in the JSON file.
    - `force` (bool): Whether to overwrite any existing data in the JSON file.
    - `do_print` (bool): Whether to print information about the data writing process.

    Return:
    - `bool`: Whether the file was created.
    """

    try:
        if data.__class__.__name__ == ('str'):
            data = json.loads(data)

        d = read_json(filepath)
        
        if d and not force:
            fprint(f'Data found in JSON file, not writing new data: {filepath}', do_print=do_print)
            return False

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=indent)

        fprint(f'Wrote data to JSON file: {filepath}', do_print=do_print)
        return True
    except TypeError:
        fprint(f'Data type is wrong, can\'t write to JSON: {data.__class__.__name__}', do_print=do_print)
    except Exception:
        fprint(traceback.format_exc())
    return False