import asyncio
from os import path
import lz4.frame
import requests

import hhdm_apiclient_wrapper as hh


async def main():
    # This can be found by visiting https://hh-dev.com, logging in, and selecting "HH Data Management" -> "Integrations"
    api_key = 'YOUR_API_KEY'

    account_id = 'YOUR_ACCOUNT_ID'
    event_id = 'YOUR_EVENT_ID'

    auth_settings = hh.AuthenticationSettings(
        api_key=api_key,
        authentication_mode=hh.AuthenticationMode.API_KEY,
    )
    client = hh.ApiClient(authentication_manager=hh.AuthenticationManager(auth_settings))

    print(f'Api client wrapper v{client.get_version()}. Running download compressed attached file demo on account "{account_id}" and event "{event_id}".\n')

    dest_path = 'C:\\HHDM-Export\\HHDM-Files'

    if not path.isdir(dest_path):
        return

    events_result = await client.get_event_by_id(account_id, event_id, hh.ApiGetOptions(['AttachedFiles.*']))

    if not events_result.success:
        print(f'Failed to get file information: {events_result.message}')
        return

    selected_file = get_named_input(events_result.return_value['AttachedFiles'], 'Select file to download: ', lambda x: x['Parameters']['FileName'])
    file_name = selected_file['Parameters']['FileName']
    is_compressed = selected_file['Parameters']['UseCompression']

    download_result = await client.get_event_attachments_by_id(account_id, event_id, [selected_file['Id']])

    if not download_result.success:
        print(f'Failed to get signed URL to download file from: {download_result.message}')
        return

    download_url = download_result.return_value[0]['SignedURL']
    file_content = requests.get(download_url)

    dest_filepath = f'{dest_path}\\{file_name}.lz4' if is_compressed else f'{dest_path}\\{file_name}'

    with open(dest_filepath, 'wb') as f:
        f.write(file_content.content)

    print(f'Downloaded file to: {dest_filepath}')

    if not is_compressed:
        return

    uncompressed = lz4.frame.decompress(file_content.content)

    with open(f'{dest_path}\\{file_name}', 'wb') as f:
        f.write(uncompressed)

    print(f'Uncompressed file to: {dest_path}\\{file_name}')

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


