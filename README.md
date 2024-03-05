# HH Data Management Python API wrapper examples

This repository serves as library of examples showing how to use the HH Data Management Python API Wrapper.

In all examples an [API key](https://help.hh-dm.com/extensibility/api/#authentication) is needed to authenticate against the API.

## Table of Contents
* [`add_attached_file.py`](/examples/add_attached_file.py) Shows how to add and upload a file to an event. Also, how to automatically retry an upload if it fails.
* [`add_attached_file_without_downloading.py`](/examples/add_attached_file_without_downloading.py) Shows how to add and upload a file to a championship without a local filesystem.
* [`get_all_accounts.py`](/examples/get_all_accounts.py) Shows how to get all the account names and IDs your API key has access to.
* [`runsheet_laps.py`](/examples/runsheet_laps.py) Console application that walks the user through finding a run, then computes the average lap time for the run and writes the result to a variable on the run.
* [`get_setups.py`](/examples/get_setups.py) Console application that walks the user through finding setup information by selecting the championship, event and car of interest.
* [`get_run_setups.py`](/examples/get_run_setups.py) Console application that walks the user through finding setup information by selecting the championship, event and session, and car of interest. Displays how many runs each car has in the selected session and returns only the setups attached to found runs.
* [`write_weather_data.py`](/examples/write_weather_data.py) Console application that allows the user to select a championship/event and write weather measurement data to it.
* [`download_attached_file.py`](/examples/download_attached_file.py) Console application that allows the user to select an attached file from an event and downloads and automatically decompresses it to a given directory.
