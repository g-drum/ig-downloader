import json
import os

from instagrapi import Client


class Instagram:

    def __init__(self, user, password):
        self.client = Client()
        self.client.login(user, password)

    def download_stories_from_users(self, users, path):
        for user in users:
            self.download_stories_by_user(user, path)

    def download_stories_by_user(self, user, path):
        user_id = None
        user_name = None
        if 'user_id' in user:
            user_id = user['user_id']
            user_name = user['user_name'] if 'user_name' in user else self.client.username_from_user_id(user_id)
        elif 'user_name' in user:
            user_name = user['user_name']
            user_id = self.client.user_id_from_username(user_name)
        else:
            print('User has no id|username')
            return
        path = 'users/{}/stories'.format(user_name) if path is None else path
        self.check_path(path)
        stories = self.client.user_stories(user_id, 100)
        for story in stories:
            formatted_date = story.taken_at.strftime('%Y-%m-%d-%H-%M-%S')
            ext = self.get_media_extension(story)
            filename = '{}_{}'.format(user_name, formatted_date, ext)
            file = '{}.{}'.format(filename, ext)
            if not os.path.exists(path + '/' + file):
                print('Downloading story {} [{}] from {} [{}]'.format(
                        story.pk,
                        story.taken_at.timestamp(),
                        user_id,
                        user_name
                    )
                )
                self.client.story_download(story.pk, filename, path)

    def get_media_extension(self, media_object):
        types = {
            1: 'jpg',
            2: 'mp4',
        }
        return types.get(media_object.media_type) if hasattr(media_object, 'media_type') else None

    def check_path(self, path):
        os.makedirs(path, exist_ok=True)
