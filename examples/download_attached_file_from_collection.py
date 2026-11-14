import asyncio

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

    print(
        f'Api client wrapper v{client.get_version()}. Running collection attached files demo on "{client.api_endpoint}" on account "{account_id}" and event "{event_id}".\n')

    try:
        collection_name = 'TestEventCollection'
        dest_path = 'C:\\HHDM-Export\\HHDM-Files'

        collection_result = await client.get_event_by_id(account_id, event_id, hh.ApiGetOptions([f'{collection_name}.Name', f'{collection_name}.AttachedFiles.*']))
        selected_item = get_named_input(collection_result.return_value['Collections'][collection_name], 'Select collection item: ',
                                        lambda x: x['Parameters']['Name'])

        selected_file = get_named_input(selected_item['AttachedFiles'], 'Select file to download: ',
                                        lambda x: x['Parameters']['FileName'])
        file_name = selected_file['Parameters']['FileName']

        download_result = await client.get_event_collection_item_attachments_by_id(account_id, event_id, collection_name, selected_item['Id'], [selected_file['Id']])

        if not download_result.success:
            print(f'Failed to get signed URL to download file ({download_result.status_code}): {download_result.message}')
            return

        dest_filepath = f'{dest_path}\\{file_name}'
        await client.download_file(download_result.return_value[0], f'{dest_path}\\{file_name}')

        print(f'Downloaded file to: {dest_filepath}')
    finally:
        await client.close()


def get_named_input(items, prompt, name_accessor=lambda x: x['Parameters']['Name']):
    if len(items) == 0:
        print('No entities were found.')
        return None

    print('\n'.join([f"{i + 1}) {name_accessor(item)}" for (i, item) in enumerate(items)]))
    idx = int(input(prompt)) - 1
    print(f'You selected "{name_accessor(items[idx])}"\n')
    return items[idx]


if __name__ == '__main__':
    asyncio.run(main())


