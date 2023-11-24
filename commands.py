from pathlib import Path
from typing import Generator
from math import factorial
import sys
import os
from argparse import Namespace

# TODO: Can make directories alternatives
# Warning: Very possible can create multiple alternatives of the same path, but cannot delete them because they recognize as the master. To fix. Set another alternative as master and then delete the extras

ALT = Path('/var/lib/alternatives')
ALT_CONFIG = ALT / 'config'  # Config
ALT_DIR = ALT / 'sym'  # Intermediate location of symlinks

# link -> name -> path
# strat: Keep reverse symlink to link to we can update
# update link
# link should link to a symlink in dir name
# On delete-all - set main link directly to path
# On deletion - set symlink to regular file with same name


def __validate_path(path: Path) -> Path:
    path = path.absolute()
    if not path.exists():
        print(f'{path} does not exist')
        exit(1)
    if not path.is_file():
        print(f'{path} is not a file')
        exit(1)
    if not os.access(path, os.X_OK):
        print(f'{path} is not executable')
        exit(1)
    return path


def install_command(args: Namespace):
    """
    a -> name -> *alt1, alt2, alt3
    name: directory
    symlink to name
    +symlinks to alts
    Folder: other symlinks

    """
    link: Path = args.link
    name: str = args.name
    path: Path = __validate_path(args.path)
    if link.exists():
        print(f'Cannot create alternative link: File at {link} already exists')
        exit(1)
    if (ALT_DIR / name).exists():
        print(f'Link group \'{name}\' already exists')
        exit(1)
    try:
        (ALT_DIR / name).mkdir(parents=True)
    except Exception as e:
        print(str(e) + '\nPlease Run again as superuser')
        exit(1)
    alternative_name_path = ALT_DIR / name
    os.symlink(path, alternative_name_path / '0')
    os.symlink(alternative_name_path / '0', link)
    os.symlink(link, alternative_name_path / 'link')
    print(f'Created link group {name}')


def add_command(args):
    """TODO:
    [ ] Check if link group exists
    It is fine if an endpoint already exists
    """
    name = args.name
    alternative_name_path = ALT_DIR / name
    if not alternative_name_path.exists():
        print(f'Link group \'{name}\' does not exist')
        exit(1)
    path = __validate_path(args.path)
    total = 0
    for each_path in alternative_name_path.iterdir():
        if each_path.is_file() and each_path.name != 'link':
            if not each_path.is_symlink():
                each_path.unlink()
                os.symlink(path, alternative_name_path / each_path.name)
                exit(0)
            total += 1
    os.symlink(path, alternative_name_path / str(total))


def set_command(args):
    name = args.name
    num = args.num
    num_dir = ALT_DIR / name / str(num)
    link_dir = (ALT_DIR / name / 'link').readlink()
    if not num_dir.exists():
        print('Does not exist')
        exit(1)
    if num_dir.samefile(link_dir):
        print('Already the master!')
        exit(1)
    # link -> name -> path
    link_dir.unlink()
    os.symlink(num_dir, link_dir)


def remove_command(args):
    name = args.name
    num = str(args.num)
    num_dir = ALT_DIR / name / num
    link_dir = ALT_DIR / name / 'link'
    if not num_dir.exists():
        print('Does not exist')
        exit(1)
    if num_dir.samefile(link_dir):
        print("This is the master!")
        exit(1)
    os.unlink(ALT_DIR / name / num)
    (ALT_DIR / name / num).touch()


def remove_all_command(args):
    name = args.name
    if not (ALT_DIR / name).is_dir():
        print(f'Link group {name} does not exist')
        exit(1)
    # Remove the alt link
    try:
        (ALT_DIR / name / 'link').readlink().unlink()
    except Exception as e:
        print(e)
    # Remove the name directory
    alt_name_dir = ALT_DIR / name
    for file in alt_name_dir.iterdir():
        try:
            file.unlink()
        except Exception as e:
            print(e)
    try:
        alt_name_dir.rmdir()
    except Exception as e:
        print(e)


def __sorter_dir(v: Path) -> int:
    try:
        return int(v.name)
    except:
        return 0


def display_command(args):
    name = args.name
    alt_name_dir = ALT_DIR / name
    try:
        link = (alt_name_dir / 'link').readlink()
        master_alternative = link.readlink()
        path = master_alternative.readlink()
    except Exception as e:
        print(e)
        exit(1)
    print(f'Link: {link}')
    print(f'Master: {path}')
    print('Alternatives:')
    for folder in sorted(alt_name_dir.iterdir(), key=__sorter_dir):
        if folder.is_symlink() and folder.name not in {master_alternative.name, 'link'}:
            print(f'{folder.name}. {folder.readlink()}')


def display_all_command(args):
    if not ALT_DIR.exists():
        exit()
    for folder in ALT_DIR.iterdir():
        # get the 'link' file and follow and get path
        try:
            link = (folder / 'link').readlink()
            path = (folder / 'link').readlink().readlink().readlink()
        except Exception as e:
            print(e)
            exit(1)
        print(f'{folder.name}: Command: {link.name}: {path}')
