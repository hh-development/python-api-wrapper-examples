import asyncio
from datetime import datetime, timezone
import json

import hhdm_apiclient_wrapper as hh


async def main():
    api_key = 'YOUR_API_KEY'
    account_id = 'YOUR_ACCOUNT_ID'

    auth_settings = hh.AuthenticationSettings(
        api_key=api_key,
        authentication_mode=hh.AuthenticationMode.API_KEY,
    )
    client = hh.ApiClient(authentication_manager=hh.AuthenticationManager(auth_settings))

    print(f'Api client wrapper v{client.get_version()}. Running write_weather_data demo.')

    championships_result = await client.get_all_championships(account_id, hh.ApiGetOptions([
        'Name',
        'Events.Name',
    ]))
    if not championships_result.success:
        print(f'Failed to get championship information: {championships_result.message}')
        return

    championship = get_named_input(championships_result.return_value, 'Select a championship: ')
    event = get_named_input(championship['Events'], 'Select an event: ')

    # Enter your measurement data here
    weather_data = [
        hh.ParameterUpdateModel("MeasurementTime", datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')),  # e.g. 2024-01-23T11:42:45.083193Z
        hh.ParameterUpdateModel("AirTemperature", "13"),
        hh.ParameterUpdateModel("TrackTemperature", "30"),
        hh.ParameterUpdateModel("WindSpeed", "55"),
    ]

    print('Writing ambient measurements to selected event...')
    weather_result = await client.add_ambient_measurement(account_id, event['Id'], hh.CreateModel(False, False, -1, weather_data))

    print(f'add_ambient_measurement result: {weather_result.success}')
    print(json.dumps(weather_result.return_value, indent=4))


def get_named_input(items, prompt, name_accessor=lambda x: x['Parameters']['Name']):
    if len(items) == 0:
        print('No entities were found.')
        return None

    print('\n'.join([f"{i+1}) {name_accessor(item)}" for (i, item) in enumerate(items)]))
    idx = int(input(prompt)) - 1
    print(f'You selected "{name_accessor(items[idx])}"\n')
    return items[idx]


if __name__ == '__main__':
    asyncio.run(main())
