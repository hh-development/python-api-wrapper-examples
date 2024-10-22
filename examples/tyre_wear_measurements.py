import asyncio
from datetime import datetime, timezone
import json

import hhdm_apiclient_wrapper as hh


async def main():
    api_key = ''
    account_id = ''

    auth_settings = hh.AuthenticationSettings(
        api_key=api_key,
        authentication_mode=hh.AuthenticationMode.API_KEY,
    )
    client = hh.ApiClient(authentication_manager=hh.AuthenticationManager(auth_settings))

    print(f'Api client wrapper v{client.get_version()}. Running tyre_wear_measurements demo.')

    championships_result = await client.get_all_championships(account_id, hh.ApiGetOptions([
        '*',
        'Events.*',
        'Events.Cars.*',
        'Events.Cars.Car.*',
    ]))
    if not championships_result.success:
        print(f'Failed to get championship information: {championships_result.message}')
        return

    championship = get_named_input(championships_result.return_value, 'Select a championship: ')
    event = get_named_input(championship['Events'], 'Select an event: ')
    car = get_named_input(event['Cars'], 'Select a car: ', lambda x: x['Parameters']['Car']['Parameters']['Number'])
    car_id = car['Parameters']['CarId']

    print('Searching for tyres...')
    tyres_result = await client.search_for_tyres(
        account_id,
        hh.AssociatedModelSeachObject(hh.AssociatedModelSearchMode.EVENT_CAR, account_id, championship['Id'], event['Id'], car_id),
        hh.ApiGetOptions(parameters_to_include=['*', 'TyreWearMeasurements.*', 'TyreWearMeasurements.TyreWearMeasurementItems.*']))
    print(f'search tyres result result: {tyres_result.success}')

    if not tyres_result.success:
        return

    tyre = tyres_result.return_value[0]
    print(json.dumps(tyre, indent=4))
    tyre_id = tyre['Id']
    print(f'Selecting first tyre to add wear measurement to with name {tyre['Parameters']['Name']}')

    measurement_result = await client.add_tyre_wear_measurement(account_id, tyre_id, hh.CreateModel())
    print(f"Add measurements result {measurement_result.success}")


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
