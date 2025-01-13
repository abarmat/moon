import unittest
from unittest.mock import patch
from moon import get_historical_crypto_prices

class TestGetHistoricalCryptoPrices(unittest.TestCase):

    @patch('moon.requests.get')
    def test_get_historical_crypto_prices_success(self, mock_get):
        mock_response = {
            'prices': [
                [1622505600000, 35000],
                [1622592000000, 36000],
                [1622678400000, 37000]
            ]
        }
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status = lambda: None

        result = get_historical_crypto_prices('bitcoin', 'usd', 3)
        expected_result = {
            '2021-06-01': 35000,
            '2021-06-02': 36000,
            '2021-06-03': 37000
        }
        self.assertEqual(result, expected_result)

    @patch('moon.requests.get')
    def test_get_historical_crypto_prices_error_handling(self, mock_get):
        mock_get.side_effect = Exception('API request failed')

        with self.assertRaises(SystemExit):
            get_historical_crypto_prices('bitcoin', 'usd', 3)

if __name__ == '__main__':
    unittest.main()
