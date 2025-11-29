from typing import Optional


class MicrosoftTeams:
    """This class provides an API for interacting with the Microsoft Teams API."""

    STYLE_ATTENTION = 'attention'
    STYLE_GOOD = 'good'
    STYLE_EMPHASIS = 'emphasis'

    @staticmethod
    def send_alert(webhook_url: str, title: str, message: str, style: Optional[str] = None, url: Optional[str] = None,
                   url_text: Optional[str] = None):
        """This method is used to send an alert to Microsoft Teams via webhook."""
        import json
        import requests
        from loguru import logger

        headers = {'Content-Type': 'application/json'}

        payload = {
            "type": "message",
            "attachments": [{
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.2",
                    "body": [
                        {
                            "type": "Container",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "size": "Medium",
                                    "weight": "Bolder",
                                    "wrap": True,
                                    "text": title,
                                },
                            ],
                            "bleed": True,
                        }
                    ],
                }
            }]
        }

        messages = message.split('\n')

        for msg in messages:
            if not len(msg.strip()):
                continue
            payload['attachments'][0]['content']['body'].append({
                "type": "TextBlock",
                "text": msg,
                "wrap": True,
            })

        if isinstance(style, str):
            payload['attachments'][0]['content']['body'][0]['style'] = style

        if isinstance(url, str):
            payload['attachments'][0]['content']['actions'] = [
                {
                    "type": "Action.OpenUrl",
                    "title": url_text if isinstance(url_text, str) else 'Open',
                    "url": url,
                }
            ]

        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))

        if 200 <= response.status_code < 300:
            logger.debug(f'MicrosoftTeams: Successfully sent alert to Microsoft Teams webhook.')
        else:
            logger.error(f'MicrosoftTeams: Failed to send alert to Microsoft Teams webhook:'
                         + f'\nStatus Code: {response.status_code}\nResponse: {response.text}')
