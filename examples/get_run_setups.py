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

    print(f'Api client wrapper v{client.get_version()}. Running get_run_setups demo.')

    championships_result = await client.get_all_championships(account_id, hh.ApiGetOptions([
        '*',
        'Events.*',
        'Events.Cars.*',
        'Events.Cars.Car.*',
        'Events.Sessions.*',
    ]))
    if not championships_result.success:
        print(f'Failed to get championship information: {championships_result.message}')
        return

    championship = get_named_input(championships_result.return_value, 'Select a championship: ')
    event = get_named_input(championship['Events'], 'Select an event: ')
    session = get_named_input(event['Sessions'], 'Select a session: ')

    cars = []
    for c in event['Cars']:
        car_id = c['Parameters']['CarId']
        car_num = c['Parameters']['Car']['Parameters']['Number']
        result = await client.get_all_run_sheets_for_session_car(account_id, session['Id'], car_id, hh.ApiGetOptions(['*', 'Setup.*']))
        if not result.success:
            print(f"Failed to get run information for car {car_num}: {result.message}")
            cars.append({
                "Id": car_id,
                "Number": car_num,
                "Errored": True,
                "Runs": []
            })
        else:
            cars.append({
                "Id": car_id,
                "Number": car_num,
                "Runs": result.return_value
            })

    car = get_named_input(cars, 'Select a car: ', lambda x: f"{x['Number']} ({str(len(x['Runs'])) + ' runs' if 'Errored' not in x else 'Errored'})")

    run_setups = []
    for run in car['Runs']:
        run_setups.append(run['Parameters']['Setup'])

    print(json.dumps(run_setups, indent=2))

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
