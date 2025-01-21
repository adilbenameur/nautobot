
from nautobot.core.testing import create_job_result_and_run_job, TransactionTestCase, run_job_for_testing
from nautobot.extras.choices import JobResultStatusChoices
from nautobot.extras.models import Job

from unittest.mock import patch

class MockJobDependencyTest(TransactionTestCase):
    """
    Test the mocking of a job dependencies.
    """

    databases = ("default", "job_logs")

    @patch("jobs.jobs.my_job.check_file")
    def test_os_mock(self, mock_check_file):
        j = Job.objects.get(job_class_name="MyJob")
        j.enabled = True
        j.save()
        job_result = run_job_for_testing(job=j)
        self.assertEqual(job_result.status, JobResultStatusChoices.STATUS_SUCCESS)
        mock_check_file.assert_called_once()