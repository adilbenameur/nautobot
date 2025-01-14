from .jobs.my_job import MyJob

from nautobot.apps.jobs import register_jobs

register_jobs(MyJob)