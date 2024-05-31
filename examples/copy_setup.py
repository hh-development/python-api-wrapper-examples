import asyncio
import hhdm_apiclient_wrapper as hh


async def main():
    api_key = 'YOUR_API_KEY'
    account_id = 'YOUR_ACCOUNT_ID'

    event_id = 'YOUR_EVENT_ID'
    car_id = 'YOUR_CAR_ID'
    base_setup_id = 'YOUR_SETUP_ID'

    auth_settings = hh.AuthenticationSettings(
        api_key=api_key,
        authentication_mode=hh.AuthenticationMode.API_KEY,
    )
    client = hh.ApiClient(authentication_manager=hh.AuthenticationManager(auth_settings))

    print(f'Api client wrapper v{client.get_version()}. Running copy_setup demo.')

    response = await client.add_setup(
        account_id=account_id,
        event_id=event_id,
        car_id=car_id,
        create_model=hh.CreateModel(
            copy_from_last=False,
            copy_all=True,
            copy_from_id=base_setup_id,
            parameter_updates=[
                hh.ParameterUpdateModel('Name', 'Copied Setup'),
                hh.ParameterUpdateModel('aCamberFL', '-5.2'),
            ]
        )
    )

    if response.success:
        print(f'Copied setup "{base_setup_id}" successfully.')
    else:
        print(f'Failed to copy setup "{base_setup_id}".')


if __name__ == '__main__':
    asyncio.run(main())
