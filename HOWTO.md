# Welcome to Connect Extension Inquiring Notifications !

Overview
## About Email Platform
Email is the most used communication system. With email, you can send messages, photos, videos, and files of any type (doc, zip, mp3, etc).

## Connect Extension Inquiring Notifications
This **Inquiring Notification Extension** allows sending a customized email to your customer when a subscription is in status "Inquiring".
If you are a Distributor or a Reseller, you can define three periods of time for when the subscription becomes to the status "Inquiring", the extension sends an email to the customer contact using the template associated with the **installation**.

With this extension, for each installation you can:
- Create templates customized
- Define the email sender
- Include subscription metadata as
    - Customer name
    - Asset ID
- Include subscription metadata blocks as 
    - Items
    - Parameters
- Include links and images
- See in the extension log the date that the email was sent 

### Settings structure
To configure the installation is necessary to set up a json with the following structure:

{
  "period": [
    1,
    4,
    10
  ],
  "MP-03811": {
    "template": "![logo](https://www.cloudblue.com/assets/images/navlogo-dark.png) \n## Additional Information Is Required To Process Your Request \n### Hello {{request.asset.tiers.customer.name}}, \n### Additional information is required to process your request for the Product {{request.asset.product.name}} for {{request.asset.tiers.tier1.name}} by Vendor.\n### Please complete our [form]({{request.params_form_url}}) to resume processing of your request",
    "email_title": "inquire request",
    "sender_name": "Sender Name",
    "sender_email": "sender@gmail.com",
    "catchall_email": "pepe@gmail.com"
  },
  "MP-03812": {
    "template": "Template for marketplace MP-03812",
    "email_title": "inquire request",
    "sender_name": "Sender Name",
    "sender_email": "sender@gmail.com",
  },
  "defaults": {
    "template": "<!DOCTYPE HTML><html><head><title>Subscription product: {{request.asset.product.name}} </title><meta charset=\"utf-8\"></head><body><p>Lista con elementos desordenados</p><ul><li>Uno</li><li>Dos</li><li>Tres</li></ul><p>Lista con sublistas anidadas</p><ul><li>Primero</li><li>Segundo<ul><li>Segundo Uno</li><li>Segundo Dos</li></ul></li><li>Tercero</li></ul></body></html>",
    "email_title": "inquire request",
    "sender_name": "Sender Name",
    "sender_email": "sender@gmail.com",
    "catchall_email": "pepe@gmail.com"
  }
}
## License
**connect-extension-inquire-notifications** is licensed under the *Apache Software License 2.0* license.
