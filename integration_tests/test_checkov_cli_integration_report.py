import json
import os
import platform
import sys
import unittest

current_dir = os.path.dirname(os.path.realpath(__file__))


class TestCheckovJsonReport(unittest.TestCase):

    def test_guideline_in_custom_policy(self):
        report_path = os.path.join(current_dir, '..', 'checkov_report_custom_policy.json')
        with open(report_path, 'r') as fp:
            report = json.load(fp)
        failed_checks = report['results']['failed_checks']
        self.assertGreater(len(failed_checks), 100, 'Expected at least one failed check for the custom policy')
        self.assertIsNotNone(failed_checks[0]['guideline'], 'Expected the custom policy guideline field to have a value')
        self.assertGreater(len(failed_checks[0]['guideline']), 0, 'Expected the custom policy guideline field to have a value')

    def test_terragoat_report_dir_api_key(self):
        report_path = os.path.join(current_dir, '..', 'checkov_report_azuredir_api_key_terragoat.txt')
        self.validate_report(os.path.abspath(report_path))

    def test_terragoat_report_file_api_key(self):
        report_path = os.path.join(current_dir, '..', 'checkov_report_s3_singlefile_api_key_terragoat.txt')
        self.validate_report(os.path.abspath(report_path))

    def validate_report(self, report_path):
        if sys.version_info[1] == 7 and platform.system() == 'Linux':
            platform_url_found = False
            with open(report_path) as f:
                if 'More details: https://www.bridgecrew.cloud/projects?' in f.read():
                    platform_url_found = True
            self.assertTrue(platform_url_found, "when using api key, platform code review url should exist")


if __name__ == '__main__':
    unittest.main()
