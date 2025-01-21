from .jobs.my_job import MyJob

from nautobot.apps.jobs import register_jobs

register_jobs(MyJob)


import sys

# Patch triggered only when running tests
# See https://github.com/nautobot/nautobot/issues/6778 for more info.
if sys.argv[1] == "test":
    class _dict(dict):
        def __setitem__(self, key, value):
            if key in self:
                return
            return super().__setitem__(key, value)

        def __delitem__(self, key):
            return

    special_sys_modules = _dict()
    for k, v in sys.modules.items():
        special_sys_modules[k] = v
    sys.modules = special_sys_modules