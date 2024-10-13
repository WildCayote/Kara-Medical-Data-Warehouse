import csv, os, argparse
from typing import List
from telethon import TelegramClient
from dotenv import load_dotenv

async def scrape_channel(client : TelegramClient, channel_username: str, writer: any, media_dir: str):
    """
    This is a function that will write messages found from a telegram channel into a csv file.

    Args:
        client(telethon.TelegramClient): an instance of a telethon TelegramClient class
        channel_username(string): the username of a telegram channel, starts with @
        writer(csv.writer): an instance of a csv writer
    Returns:
        None
    """
    entity = await client.get_entity(channel_username)
    channel_title = entity.title  # Extract the channel's title
    async for message in client.iter_messages(entity, limit=1000):
        media_path = None
        if message.media and hasattr(message.media, 'photo'):
            # Create a unique filename for the photo
            filename = f"{channel_username}_{message.id}.jpg"
            media_path = os.path.join(media_dir, filename)
            # Download the media to the specified directory if it's a photo
            await client.download_media(message.media, media_path)
        
        # Write the channel title along with other data
        writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])

async def obtain_channel_ads(client: TelegramClient, telegram_channels: List[str], save_path: str):
    """
    This is a function that wrappers the scrape_channel function and run it over multiple telegram channels.

    Args:
        clinet(telethon.TelegramClient): an instance of a telethon TelegramClient class
        telegram_channels(List[str]): a list of telegram channel usernames
        save_path(str): the path to the folder to save the scrapping result
    Returns:
        None
    """
    # start up the client
    await client.start()
    
    # Create a directory for media files
    csv_path = os.path.join(save_path, 'telegram_data.csv')
    media_dir = os.path.join(save_path, 'media')
    os.makedirs(media_dir, exist_ok=True)

    # Open the CSV file and prepare the writer
    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['channel_title', 'channel_username', 'id', 'message', 'date', 'media_path']) 
        
        # Iterate over channels and scrape data into the single CSV file
        for channel in telegram_channels:
            print(f"********** {channel} scrapping started **********")
            await scrape_channel(client, channel, writer, media_dir)
            print(f"********** {channel} scrapping finished **********")

if __name__ == "__main__":
    # initialize argparse
    parser = argparse.ArgumentParser(
        prog='Telegram Channel Scraper',
        description='Scrapes the messages of telegram channels and images attached to them.'
    )

    # define arguments for the script
    parser.add_argument('--path', type=str, default='./data/', help='the path to store the scrapping results')
    
    # obtain the passed arguments
    args = parser.parse_args()
    path = args.path

    # Load environment variables once
    load_dotenv('.env')
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    phone_num = os.getenv('PHONE')

    # Initialize the client once
    client = TelegramClient('scraping_session', api_id, api_hash)
    print("########## Client Initialization Succcessful ##########")

    # list the channels to be scraped
    channels = ['@DoctorsET', '@lobelia4cosmetics', '@yetenaweg']

    with client:
        client.loop.run_until_complete(
            obtain_channel_ads(
                client=client,
                telegram_channels=channels,
                save_path=path
            )
        )
