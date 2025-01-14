import os
from nautobot.core.jobs import Job

class MyJob(Job):
    class Meta:
        name = 'MyJob'
        description = 'My Job'

    def run(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os.path.exists(os.path.join(dir_path, 'my_script.sh'))