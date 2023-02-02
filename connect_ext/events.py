import markdown
import boto3

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timezone

from connect.eaas.core.decorators import (
    schedulable,
    variables,
)
from connect.eaas.core.extension import EventsApplicationBase
from connect.eaas.core.responses import ScheduledExecutionResponse

from connect_ext import jinja

CHARSET = 'UTF-8'


@variables(
    [
        {
            'name': 'AWS_SECRET_ACCESS_FOR_SES',
            'initial_value': 'Change for the secret',
            'secure': True,
        },
        {
            'name': 'AWS_ACCESS_KEY_ID',
            'initial_value': 'Change for the access key',
        },
        {
            'name': 'AWS_REGION',
            'initial_value': 'Change for the region',
        },
        {
            'name': 'ENVIRONMENT',
            'initial_value': 'TEST',
        },
    ],
)
class ConnectExtensionInquireNotificationsEventsApplication(EventsApplicationBase):

    @schedulable('Schedulable method', 'It can be used to test DevOps scheduler.')
    def execute_scheduled_processing(self, schedule):  # noqa: CCR001
        try:
            extension_id = self.context.extension_id
            installations = self.client('devops').services[extension_id].installations.all()
            for installation in installations:
                installation_admin_client = self.get_installation_admin_client(installation['id'])
                if installation['owner']['role'] != 'vendor':
                    requests = installation_admin_client.requests.filter(status='inquiring')
                    for request in requests:
                        updated_at = datetime.fromisoformat(request['events']['updated']['at'])
                        age = (datetime.now(tz=timezone.utc) - updated_at).days
                        period = installation['settings']['period']
                        for p in period:
                            if age >= p and age < p + 1:
                                try:
                                    data = self.get_data(installation, request)
                                    if data.get('force_receiver_email'):
                                        email_to = data['force_receiver_email']
                                    else:
                                        contact = request['asset']['tiers']['customer']
                                        email_to = contact['contact_info']['contact']['email']
                                    self.send_email(
                                        data['sender_name'],
                                        data['sender_email'],
                                        email_to,
                                        data['email_title'],
                                        data['template'],
                                    )
                                    self.logger.info(f"Mail sent for request: {request['id']}")
                                    self.logger.info(f"To:{email_to} From:{data['sender_email']}")
                                    self.logger.info(f"Days from inquiring status: {age}")
                                except Exception as e:
                                    self.logger.info(f'Error in template: {e}')
        except Exception:
            self.logger.exception("Extension error")
        return ScheduledExecutionResponse.done()

    def get_data(self, installation, request):
        marketplace = request['marketplace']['id']
        if marketplace in installation['settings']:
            data = installation['settings'][marketplace]
        else:
            data = installation['settings']['defaults']
        data['template'] = markdown.markdown(jinja.render(data['template'], request))

        return data

    def send_email(
        self,
        sender_name,
        sender_email,
        email_to,
        email_title,
        body,
    ):
        aws_access_key_id = self.config['AWS_ACCESS_KEY_ID']
        aws_secret_access_key = self.config['AWS_SECRET_ACCESS_FOR_SES']
        region_name = self.config['AWS_REGION']

        ses_client = boto3.client(
            'ses',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
        email_source = f'{sender_name} <{sender_email}>'
        subject = email_title

        msg = MIMEMultipart()
        msg.set_charset(CHARSET)
        msg.add_header('X-Environment', self.config.get('ENVIRONMENT', 'PRODUCTION'))
        msg['Subject'] = subject
        msg['From'] = email_source
        msg['To'] = email_to

        html_body = MIMEText(body, 'html')

        msg.attach(html_body)
        response_email = ses_client.send_raw_email(
            Source=email_source,
            Destinations=[email_to],
            RawMessage={
                'Data': msg.as_string().encode(CHARSET),
            },
        )
        return response_email['ResponseMetadata']['RequestId']
