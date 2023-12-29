import asyncio
import requests
from time import sleep

import hhdm_apiclient_wrapper as hh


def main():
    # This can be found by visiting https://hh-dev.com, logging in, and selecting "HH Data Management" -> "Integrations"
    api_key = 'YOUR_API_KEY'

    account_id = 'YOUR_ACCOUNT_ID'
    championship_id = 'YOUR_CHAMPIONSHIP_ID'

    auth_settings = hh.AuthenticationSettings(
        api_key=api_key,
        authentication_mode=hh.AuthenticationMode.API_KEY,
    )
    client = hh.ApiClient(authentication_manager=hh.AuthenticationManager(auth_settings))

    print(
        f'Api client wrapper v{client.get_version()}. Running attached files without local filesystem demo on account "{account_id}" and championship "{championship_id}".\n')

    file_url = 'https://<REMOTE_FILE_URL>'
    file_name = 'YOUR_FILE_NAME'

    # You do not need to have a custom property attached file defined to upload a file and can set this to None if desired.
    custom_property_attached_file_name = None

    with requests.get(file_url, stream=True) as file_stream:
        result = asyncio.run(client.add_attachment_to_championship(
            account_id,
            championship_id,
            hh.ApiPrepareUploadModel(
                file_name,  # lets you specify the name that will appear for the file in the software (could just be the file name from the path)
                custom_property_attached_file_name,  # lets you specify a CustomPropertyAttachedFileName - for normal files would be None
                True,  # whether to overwrite the existing file if uploading to a CustomPropertyAttachedFile that only allows one file. Only applicable if custom_property_attached_file_name is not None
                False,  # if True then the file will be automatically downloaded on all users computers that have access to the file (should be False in most cases)
                True  # lets you specify whether the file should be compressed before uploading, generally this should be set to True
            ),
            file_stream.content))

        # This means there was an error adding the attached file property in HH DM
        if result.add_attachment_status == hh.AddAttachmentStatus.FAILED_TO_ADD:
            print(f'Failed to add attachment: {result.message}')
            return

        # This means uploading the content of the attachment failed.
        while (result.add_attachment_status == hh.AddAttachmentStatus.FAILED_TO_UPLOAD
               or result.add_attachment_status == hh.AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS):
            print(f'Attachment failed for reason {result.add_attachment_status}.\n{result.message}\n Retrying...')
            result = asyncio.run(client.retry_championship_attachment(result, file_stream.content))
            sleep(0.5)

    print(f'File added successfully.')


if __name__ == '__main__':
    main()


