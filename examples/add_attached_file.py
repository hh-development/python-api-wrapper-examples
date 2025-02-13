import asyncio
from os import path
from time import sleep

import hhdm_apiclient_wrapper as hh


async def main():
    # This can be found by visiting https://hh-dev.com, logging in, and selecting "HH Data Management" -> "Integrations"
    api_key = 'YOUR_API_KEY'
    account_id = 'YOUR_ACCOUNT_ID'
    event_id = 'YOUR_EVENT_ID'

    # You do not need to have a custom property attached file defined to upload a file and can set this to None if desired.
    custom_property_attached_file_name = 'TestFile'

    auth_settings = hh.AuthenticationSettings(
        api_key=api_key,
        authentication_mode=hh.AuthenticationMode.API_KEY,
    )
    client = hh.ApiClient(authentication_manager=hh.AuthenticationManager(auth_settings))

    print(f'Api client wrapper v{client.get_version()}. Running attached files demo on account "{account_id}" and event "{event_id}".\n')

    file_path = 'C:\\HHDM-Files\\test-file.png'

    if not path.isfile(file_path):
        return

    file_name = path.basename(file_path)  # This is the file name that HH DM will see

    result = await client.add_attachment_to_event(
        account_id,
        event_id,
        hh.ApiPrepareUploadModel(
            file_name,  # lets you specify the name that will appear for the file in the software (could just be the file name from the path)
            custom_property_attached_file_name,  # lets you specify a CustomPropertyAttachedFileName - for normal files would be None
            True, # whether to overwrite the existing file if uploading to a CustomPropertyAttachedFile that only allows one file. Only applicable if custom_property_attached_file_name is not None
            False,  # if True then the file will be automatically downloaded on all users computers that have access to the file (should be False in most cases)
            True  # lets you specify whether the file should be compressed before uploading, generally this should be set to True
        ),
        file_path
    )

    # This means there was an error adding the attached file property in HH DM
    if result.add_attachment_status == hh.AddAttachmentStatus.FAILED_TO_ADD:
        print(f'Failed to add attachment: {result.message}')
        return

    # This means uploading the content of the attachment failed.
    while result.add_attachment_status == hh.AddAttachmentStatus.FAILED_TO_UPLOAD or result.add_attachment_status == hh.AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
        print(f'Attachment failed for reason {result.add_attachment_status}.\n{result.message}\n Retrying...')
        result = await client.retry_event_attachment(result)
        sleep(0.5)

    print(f'File added successfully.')

    await client.close()


if __name__ == '__main__':
    asyncio.run(main())


