# HH Data Management Python API wrapper examples

This repository serves as library of examples showing how to use the HH Data Management Python API Wrapper.

In all examples an [API key](https://help.hh-dm.com/extensibility/api/#authentication) is needed to authenticate against the API.

## Table of Contents
* [`add_attached_file.py`](/examples/add_attached_file.py) Shows how to add and upload a file to an event. Also, how to automatically retry an upload if it fails.
* [`add_attached_file_without_downloading.py`](/examples/add_attached_file_without_downloading.py) Shows how to add and upload a file to a championship without a local filesystem.
* [`get_all_accounts.py`](/examples/get_all_accounts.py) Shows how to get all the account names and IDs your API key has access to.
* [`runsheet_laps.py`](/examples/runsheet_laps.py) Console application that walks the user through finding a run, then computes the average lap time for the run and writes the result to a variable on the run.