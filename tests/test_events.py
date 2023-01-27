from connect_ext.events import ConnectExtensionInquireNotificationsEventsApplication


def test_send_email(
    mocker,
    connect_client,
    logger,
):
    config = {
        'AWS_ACCESS_KEY_ID': 'access_id',
        'AWS_SECRET_ACCESS_FOR_SES': 'access_secret',
        'AWS_REGION': 'region',
    }
    settings = {
        "sender_name": "John Doe",
        "sender_email": "doe@example.com",
        "email_title": "inquire request",
        "email_template": "Hi this is a template",
        "period": [1, 4, 10],
    }
    installation = {'settings': settings}
    email_to = 'test@receiver.com'
    body = '<p>rendered body</p>'

    mocked_ses_client = mocker.MagicMock()
    mocked_boto3 = mocker.patch('connect_ext.events.boto3.client', return_value=mocked_ses_client)
    ext = ConnectExtensionInquireNotificationsEventsApplication(connect_client, logger, config)
    ext.send_email(installation, email_to, body)
    mocked_ses_client.send_raw_email.assert_called_once_with(
        Source=f'{settings["sender_name"]} <{settings["sender_email"]}>',
        Destinations=[email_to],
        RawMessage={
            'Data': mocker.ANY,
        },
    )

    mocked_boto3.assert_called_once_with(
        'ses',
        aws_access_key_id='access_id',
        aws_secret_access_key='access_secret',
        region_name='region',
    )
