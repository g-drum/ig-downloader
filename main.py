#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from datetime import datetime

from Instagram import Instagram


def main():
    users = json.load(open('users.json'))
    credentials = json.load(open('credentials.json'))
    ig = Instagram(credentials['user'], credentials['password'])
    ig.download_stories_from_users(users, None)

if __name__ == '__main__':
    main()
