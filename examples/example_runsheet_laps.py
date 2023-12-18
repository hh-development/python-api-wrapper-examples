import asyncio

import hhdm_apiclient_wrapper as hh


def main():
    api_key = 'YOUR_API_KEY'

    auth_settings = hh.AuthenticationSettings(
        api_key=api_key,
        authentication_mode=hh.AuthenticationMode.API_KEY,
    )
    client = hh.ApiClient(authentication_manager=hh.AuthenticationManager(auth_settings))

    print(f'Api client wrapper v{client.get_version()}. Running lap average computation demo.')

    result = asyncio.run(client.get_all_accounts())
    if not result.success:
        print(f'Failed to get account information: {result.message}')
        return

    account = get_named_input(result.return_value, 'Enter the number of the account to run the demo on: ', lambda x: x['Name'])
    account_id = account['Id']

    championships_result = asyncio.run(client.get_all_championships(account_id, hh.ApiGetOptions([
        '*',
        'Events.*',
        'Events.Sessions.*',
        'Events.Cars.*',
        'Events.Cars.Car.*'
    ])))
    if not championships_result.success:
        print(f'Failed to get championship information: {result.message}')
        return

    championship = get_named_input(championships_result.return_value, 'Select a championship: ')
    event = get_named_input(championship['Events'], 'Select an event: ')
    session = get_named_input(event['Sessions'], 'Select a session: ')
    session_id = session['Id']
    car = get_named_input(event['Cars'], 'Select a car: ', lambda x: x['Parameters']['Car']['Parameters']['Number'])
    car_id = car['Parameters']['CarId']

    print(f'Account: {account_id}')
    print(f'Session: {session_id}')
    print(f'Car: {car_id}')

    runsheets_result = asyncio.run(client.get_all_run_sheets_for_session_car(account_id, session_id, car_id, hh.ApiGetOptions(['RunName','Laps.LapTime'])))
    if not runsheets_result.success:
        print(f'Failed to get runsheets: {result.message}')
        return

    runsheet = get_named_input(runsheets_result.return_value, 'Select a runsheet: ', lambda x: x['Parameters']['RunName'])

    laptimes = [l['Parameters']['LapTime'] for l in runsheet['Laps']]
    avg_lap = sum(laptimes) / len(laptimes)

    print(f"Average laptime for \"{runsheet['Parameters']['RunName']}\" with {len(laptimes)} laps: {avg_lap} s")
    print('\nUpdating runsheet AverageLapTimeCalculated...')

    update_result = asyncio.run(client.update_run_sheet(account_id, runsheet['Id'], hh.UpdateModel(None,[
        hh.ParameterUpdateModel('AverageLapTimeCalculated', str(avg_lap))
    ])))
    if update_result:
        print('Success.')
    else:
        print('Failed.')


def get_named_input(items, prompt, name_accessor=lambda x: x['Parameters']['Name']):
    if len(items) == 0:
        print('No entities were found.')
        return None

    print('\n'.join([f"{i+1}) {name_accessor(item)}" for (i, item) in enumerate(items)]))
    idx = int(input(prompt)) - 1
    print(f'You selected "{name_accessor(items[idx])}"\n')
    return items[idx]


if __name__ == '__main__':
    main()
