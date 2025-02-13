import asyncio
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

    print(f'Api client wrapper v{client.get_version()}. Running get_setups demo.')

    championships_result = await client.get_all_championships(account_id, hh.ApiGetOptions([
        '*',
        'Events.*',
        'Events.Cars.*',
        'Events.Cars.Car.*'
    ]))
    if not championships_result.success:
        print(f'Failed to get championship information: {championships_result.message}')
        return

    championship = get_named_input(championships_result.return_value, 'Select a championship: ')
    event = get_named_input(championship['Events'], 'Select an event: ')
    car = get_named_input(event['Cars'], 'Select a car: ', lambda x: x['Parameters']['Car']['Parameters']['Number'])
    car_id = car['Parameters']['CarId']

    setups_result = await client.get_all_setups_for_event_car(account_id, event['Id'], car_id, hh.ApiGetOptions(['*']))

    print(f'get_all_setups_for_event_car result: {setups_result.success}')
    print(json.dumps(setups_result.return_value, indent=4))

    await client.close()


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
