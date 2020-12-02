# SFM2-PY-RPi
Python/PyGATT test software to connect to multiple SFM2's includes using external BLE USB Dongle

## How to run
1. Install pygatt
2. Check if the adapter name in line *adapters = ...* matches the RPIs adapter (it should).
3. Set correct SFM2s MAC addresses in SFM2S array common.py
4. Configure your SFM2s using Xam app (or USB). The test will use SFQT stream so make sure that SFOR is not 0.
5. Run test.py

## What the script will do
1. Connect to each SFM2 (they'll all be connected at the same time).
2. Subscribe to SFQT stream notifications
3. Measure SFQT sample rate and output a  single line each second containg the measured rates for each SFM2.

## Multiple adapters
Please see the commented *adapters = ...* line for how to setup two BLE adapters.

## Adapter configuration
There are two commented configure_adapter calls at the top of test.py.
Those will configure the min and max connection interval settings of RPi's BLE adapter.
Setting them may greatly increase the throughput (IIRC the best values are 24 for both min and max)