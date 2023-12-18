import asyncio
import json

import hhdm_apiclient_wrapper as hh

def main():
    api_key = 'YOUR_API_KEY'

    auth_settings = hh.AuthenticationSettings(
        api_key=api_key,
        authentication_mode=hh.AuthenticationMode.API_KEY,
    )
    client = hh.ApiClient(authentication_manager=hh.AuthenticationManager(auth_settings))

    print(f'Api client wrapper v{client.get_version()}. Running get_all_accounts demo.')

    result = asyncio.run(client.get_all_accounts())

    print(f'get_all_accounts result: {result.status_code}')
    print(json.dumps(result.return_value, indent=4))


if __name__ == '__main__':
    main()
