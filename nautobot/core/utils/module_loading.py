from contextlib import contextmanager
import importlib
from importlib.util import find_spec, module_from_spec
import logging
import os
import pkgutil
import sys

logger = logging.getLogger(__name__)


@contextmanager
def _temporarily_add_to_sys_path(path):
    """
    Allow loading of modules and packages from within the provided directory by temporarily modifying `sys.path`.

    On exit, it restores the original `sys.path` value.
    """
    old_sys_path = sys.path.copy()
    sys.path.insert(0, path)
    try:
        yield
    finally:
        sys.path = old_sys_path


def clear_module_from_sys_modules(module_name):
    """
    Remove the module and all its submodules from sys.modules.
    """
    for name in list(sys.modules.keys()):
        if name == module_name or name.startswith(f"{module_name}."):
            del sys.modules[name]

import traceback
import gc
import sys, _imp
# remove the frozen module
del sys.modules['importlib']._bootstrap
del sys.modules['_frozen_importlib']
del sys.modules['importlib._bootstrap']
# import the non-frozen module
import importlib._bootstrap
# … and set it up as importlib/__init__.py does
importlib._bootstrap._setup(sys, _imp)

def walk_packages_filtering(module_prefix, path):
    for finder, discovered_module_name, is_package in pkgutil.walk_packages([path], onerror=logger.error):
        if module_prefix and not (
            module_prefix.startswith(f"{discovered_module_name}.")  # my_repo/__init__.py
            or discovered_module_name == module_prefix  # my_repo/jobs.py
            or discovered_module_name.startswith(f"{module_prefix}.")  # my_repo/jobs/foobar.py
        ):
            continue
        try:
            existing_module = find_spec(discovered_module_name)
        except (ModuleNotFoundError, ValueError):
            existing_module = None
        if existing_module is not None:
            existing_module_path = os.path.realpath(existing_module.origin)
            if not existing_module_path.startswith(path):
                logger.error(
                    "Unable to load module %s from %s as it conflicts with existing module %s",
                    discovered_module_name,
                    path,
                    existing_module_path,
                )
                continue
        yield discovered_module_name

def import_modules_privately(path, module_path=None, ignore_import_errors=True):
    """
    Import modules from the filesystem without adding the path permanently to `sys.path`.

    This is used for importing Jobs from `JOBS_ROOT` and `GIT_ROOT` in such a way that they remain relatively
    self-contained and can be easily discarded and reloaded on the fly.

    If you find yourself writing new code that uses this method, please pause and reconsider your life choices.

    Args:
        path (str): Directory path possibly containing Python modules or packages to load.
        module_path (list): If set to a non-empty list, only modules matching the given chain of modules will be loaded.
            For example, `["my_git_repo", "jobs"]`.
        ignore_import_errors (bool): Exceptions raised while importing modules will be caught and logged.
            If this is set as False, they will then be re-raised to be handled by the caller of this function.
    """
    if module_path is None:
        module_path = []
        module_prefix = None
    else:
        module_prefix = ".".join(module_path)
    with _temporarily_add_to_sys_path(path):
        for discovered_module_name in walk_packages_filtering(module_prefix, path):
            if discovered_module_name in sys.modules:
                #clear_module_from_sys_modules(discovered_module_name)
                pass
        for discovered_module_name in walk_packages_filtering(module_prefix, path):
            try:
                module = importlib.import_module(discovered_module_name)
                print(id(sys.modules["jobs"].jobs.my_job.MyJob), id(sys.modules["jobs.jobs"].my_job.MyJob), id(sys.modules["jobs.jobs.my_job"].MyJob), sys.modules["jobs.jobs.my_job"].MyJob, module.__name__)
            except Exception as exc:
                print(exc)
                logger.error("Unable to load module %s from %s: %s", discovered_module_name, path, exc)
                if not ignore_import_errors:
                    raise

        # module = importlib.import_module("jobs.jobs.my_job")
        # importlib.reload(module)
        # print(id(sys.modules["jobs"].jobs.utils.my_dependency.check_file), id(sys.modules["jobs.jobs.utils.my_dependency"].check_file), id(sys.modules["jobs.jobs.my_job"].check_file), module.__name__)
        # print("reloading")
        # for finder, discovered_module_name, is_package in pkgutil.walk_packages([path], onerror=logger.error):
        #     try:
        #         module = sys.modules[discovered_module_name]
        #         importlib.reload(module)
        #         print(id(sys.modules["jobs"].jobs.utils.my_dependency.check_file), id(sys.modules["jobs.jobs.utils.my_dependency"].check_file), id(sys.modules["jobs.jobs.my_job"].check_file), module.__name__)
        #     except Exception as exc:
        #         logger.error("Unable to reload module %s from %s: %s", discovered_module_name, path, exc)
        #         if not ignore_import_errors:
        #             raise

