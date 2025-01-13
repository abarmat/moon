# Moon

Moon is a Python script for querying current and historical cryptocurrency prices using the CoinGecko API.

## Installation

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

To run the `moon.py` script, use the following command:

```bash
python moon.py [OPTIONS]
```

### Options

- `-i`, `--crypto_ids`: Cryptocurrency IDs (default: bitcoin). Examples: bitcoin ethereum litecoin.
- `-c`, `--currency`: Currency code (default: usd). Examples: usd, eur, gbp, jpy.
- `-d`, `--historical`: Number of days for historical data (default: 0).

### Examples

Get the current price of Bitcoin in USD:

```bash
python moon.py -i bitcoin -c usd
```

Get the historical prices of Bitcoin for the past 7 days in USD:

```bash
python moon.py -i bitcoin -c usd -d 7
```

## Running Tests

To run the tests in `tests/test_moon.py`, use the following command:

```bash
python -m unittest discover
```
