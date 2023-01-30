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
                                    contact = request['asset']['tiers']['customer']
                                    email_to = contact['contact_info']['contact']['email']
                                    marketplace = request['marketplace']['id']
                                    body = self.get_body(installation, request, marketplace)
                                    mail_response = self.send_email(
                                        installation['settings']['sender_name'],
                                        installation['settings']['sender_email'],
                                        email_to,
                                        installation['settings']['email_title'],
                                        body,
                                    )
                                    self.logger.info(f"Mail response: {mail_response}")
                                except Exception as e:
                                    self.logger.info(f'Error in template: {e}')
        except Exception:
            self.logger.exception("Extension error")
        return ScheduledExecutionResponse.done()

    def get_body(self, installation, request, marketplace):
        template = installation['settings']['default_template']
        if 'marketplace_template' in installation['settings']:
            for element in installation['settings']['marketplace_template']:
                if element['marketplace'] == marketplace:
                    template = element['template']
                    break
        return markdown.markdown(jinja.render(template, request))

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
        self.logger.info(f"ses result: {ses_client}")

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
