from nautobot.core.jobs import Job
from ..utils.my_dependency import check_file

class MyJob2(Job):
    class Meta:
        name = 'MyJob'
        description = 'My Job'

    def run(self):
        check_file()