
from nautobot.core.testing import create_job_result_and_run_job, TransactionTestCase
from nautobot.extras.choices import JobResultStatusChoices

from unittest.mock import patch

class MockJobDependencyTest(TransactionTestCase):
    """
    Test the mocking of a job dependencies.
    """

    databases = ("default", "job_logs")

    @patch("jobs.jobs.my_job.os")
    def test_os_mock(self, mock_os):
        job_result = create_job_result_and_run_job(
            "jobs.jobs.my_job",
            "MyJob",
        )
        self.assertEqual(job_result.status, JobResultStatusChoices.STATUS_SUCCESS)
        mock_os.path.dirname.assert_called_once()
        mock_os.path.exists.assert_called_once()
        mock_os.path.realpath.assert_called_once()
        mock_os.path.join.assert_called_once()