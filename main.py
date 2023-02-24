import os
import datetime

from slack_sdk import WebClient

client = WebClient(token=os.environ["SLACK_USER_TOKEN"]) # unarchiveを使用するために、Bot tokenではなくUser OAurh Tokenを使用
today = datetime.datetime.now()
times_channel = "times-{}"

filtered_channels = [
    datetime.timedelta(days=0),
    datetime.timedelta(days=1),
    datetime.timedelta(days=3),
    datetime.timedelta(weeks=1),
    datetime.timedelta(weeks=2),
    datetime.timedelta(weeks=4),
    datetime.timedelta(weeks=8)
]
filtered_channel_names = [times_channel.format((today-delta).strftime("%Y%m%d")) for delta in filtered_channels]

def create_today_channel():
    today_channel = times_channel.format(today.strftime("%Y%m%d"))
    create_response = client.conversations_create(name=today_channel)
    print("[+] create:", create_response)
    return

def filter_channel():
    list_response = client.conversations_list()
    for channel in list_response["channels"]:
        channel_name = channel["name"]
        if not channel_name.startswith("times-"):
            # times channel以外は無視
            continue
    
        if channel_name in filtered_channel_names:
            # unarchive
            if not channel["is_archived"]:
                continue
            unarchive_response = client.conversations_unarchive(channel=channel["id"])
            print("[+] unarchive:", channel_name, unarchive_response)
        else:
            # archive
            if channel["is_archived"]:
                continue
            archive_response = client.conversations_archive(channel=channel["id"])
            print("[+] archive:", channel_name, archive_response)
    return

create_today_channel()
filter_channel()
