import asyncio
from datetime import datetime

import hhdm_apiclient_wrapper as hh

api_key = 'YOUR_API_KEY'
account_id = 'YOUR_ACCOUNT_ID'

session_id = ''
car_ids = []


async def get_runsheets_of_sessioncar(client, car_id):
    print(f'Starting get_runsheets_of_sessioncar of car id {car_id} at {datetime.now()}')
    results = await client.get_all_run_sheets_for_session_car(account_id, session_id, car_id, hh.ApiGetOptions(parameters_to_include=['*']))
    print(f'Finished get_runsheets_of_sessioncar of car id {car_id} at {datetime.now()}')
    return results


async def get_run_sheet_results():
    auth_settings = hh.AuthenticationSettings(
        api_key=api_key,
        authentication_mode=hh.AuthenticationMode.API_KEY,
    )
    client = hh.ApiClient(authentication_manager=hh.AuthenticationManager(auth_settings))

    coroutines = [get_runsheets_of_sessioncar(client, car_id) for car_id in car_ids]
    all_runsheet_results = await asyncio.gather(*coroutines)

    await client.close()
    return all_runsheet_results


run_sheet_results = asyncio.run(get_run_sheet_results())
