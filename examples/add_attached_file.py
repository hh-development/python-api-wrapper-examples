import asyncio
from os import path

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
        f'Api client wrapper v{client.get_version()}. Running attached files demo on "{client.api_endpoint}" on account "{account_id}" and event "{event_id}".\n')

    try:
        filepath = 'C:\\HHDM-Export\\HHDM-Files\\test.jpg'
        file_name = path.basename(filepath)
        custom_property_attached_file_name = None

        result = await client.add_attachment_to_event_and_wait_for_upload(
            account_id,
            event_id,
            hh.ApiPrepareUploadModel(
                file_name,  # specify the name that will appear for the file in the software (could just be the file name from the path)
                custom_property_attached_file_name,  # specify a CustomPropertyAttachedFileName - for normal files would be None
                True,  # whether to overwrite the existing file if uploading to a CustomPropertyAttachedFile that only allows one file. Only applicable if custom_property_attached_file_name is not None
            ),
            filepath)

        if result.add_attachment_status != hh.AddAttachmentStatus.SUCCESS:
            print(f'Failed to add attachment: {result.add_attachment_status} -- {result.message}')
            return

        print(f'File added successfully.')
    finally:
        await client.close()


if __name__ == '__main__':
    asyncio.run(main())


