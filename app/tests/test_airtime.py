import unittest
import africastalking
from unittest.mock import patch
from airtime import top_up_airtime


class TestAirtime(unittest.TestCase):
    # mock airtime.send with the patch decorator
    @patch('africastalking.Airtime.send')
    def test_top_up_airtime_success(self, mock_send):
        # Mock the response from the API
        mock_send.return_value = {
            "status": "Success", "transactionId": "123456"}

        # Call the function
        result = top_up_airtime("+254716299581", 20, "KES")

        # Assert the expected output
        self.assertEqual(
            result, {"status": "Success", "transactionId": "123456"})

    @patch('africastalking.Airtime.send')
    def test_top_up_airtime_failure(self, mock_send):
        # Mock an exception being raised
        mock_send.side_effect = Exception("An error occurred")

        # Call the function
        result = top_up_airtime("+254716299581", 20, "KES")

        # Assert the expected output
        self.assertEqual(
            result, "Encountered an error while sending airtime. More error details below\n An error occurred")


if __name__ == '__main__':
    unittest.main()
