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
  "settings": {
    "sender_name": "Martin Constante",
    "sender_email": "martin.constante@cloudblue.com",
    "email_title": "inquire request",
    "default_template": "![logo](https://example.com/logo.png) \n ## Additional Information Is Required To Process Your Request \n Hello ${tiers.customer.name}, Additional information is required to process your request for the Product ${asset.product.name} for ${tiers.tier1.name} by Vendor. \n Please complete our ![activation form](${activation_form}) to resume processing of your request",
    "marketplace_template": [
      {
        "template": "Template for marketplace MP-03811",
        "marketplace": "MP-03811"
      },
      {
        "template": "Template for marketplace MP-03812",
        "marketplace": "MP-03812"
      }
    ],
    "period": [
      1,
      4,
      10
    ]
  }
}

## License
**connect-extension-inquire-notifications** is licensed under the *Apache Software License 2.0* license.
