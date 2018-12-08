import falcon
import os
import requests
import random


from slackclient import SlackClient
from faceswap import FaceSwapper
from quotes import quotes

face_swapper = FaceSwapper()

BOT_ACCESS_TOKEN = os.environ['BOT_ACCESS_TOKEN']
slack = SlackClient(BOT_ACCESS_TOKEN)

class SwapResource:
    def __init__(self):
        self.finished_events = {}

    def _download_face_pic(self, pic_url):
        image_data = requests.get(
            pic_url,
            headers={'Authorization': 'Bearer {}'.format(BOT_ACCESS_TOKEN)}
        )
        return image_data.content
        
    def on_post(self, req, resp):

        if 'type' not in req.media:
            return

        # Used by Slack to check if service is running
        if req.media['type'] == 'url_verification':
            resp.body = req.media['challenge']
            return

        elif req.media['type'] == 'event_callback':
            try:
                if req.media['event_id'] in self.finished_events:
                    return
                self.finished_events[req.media['event_id']] = True
                pic_url = req.media['event']['files'][0]['url_private']
                face_pic = self._download_face_pic(pic_url)
                swapped_pic = face_swapper.run(face_pic)
                slack.api_call(
                    'files.upload',
                    channels=[req.media['event']['channel']],
                    file=open(swapped_pic, 'rb'),
                    initial_comment=random.choice(quotes)
                )
            except:
                pass


api = falcon.API()
api.add_route('/swap', SwapResource())
