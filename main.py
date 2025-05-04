import asyncio
import sys
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeExpiredError
import os

# Maximum number of retry attempts for expired code
MAX_RETRIES = 3

async def main():
    # Get API ID and Hash from the user
    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_HASH")

    # Get phone number from the user
    phone = os.environ.get("PHONE")

    # Create the Telegram client
    client = TelegramClient(f'session_{phone}', api_id, api_hash)
    await client.connect()

    # Send the code request to the phone number
    await client.send_code_request(phone)
    print("Code sent! Please check your phone and enter the code:")

    # Try to log in with retries for expired code
    retries = 0
    while retries < MAX_RETRIES:
        code = input("Enter the code: ").strip()

        try:
            await client.sign_in(phone, code)
            break  # Exit loop if successful
        except PhoneCodeExpiredError:
            retries += 1
            if retries < MAX_RETRIES:
                print(f"The code has expired. Attempt {retries}/{MAX_RETRIES}. Trying again...")
                await client.send_code_request(phone)  # Resend code
            else:
                print("The code has expired too many times. Please try again later.")
                return
        except SessionPasswordNeededError:
            password = input("2FA password is required. Please enter your password: ")
            await client.sign_in(password=password)
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return

    print("Successfully logged in!")

    # Load message from file
    try:
        with open("message.txt", "r", encoding="utf-8") as f:
            message = f.read().strip()
    except FileNotFoundError:
        print("Error: 'message.txt' file not found in the current directory.")
        return

    # Get the interval
    interval = int(input("Enter the interval in minutes (e.g., 5): "))

    # Get the group to send the message to
    dialogs = [d async for d in client.iter_dialogs() if d.is_group]
    print("Select a group to send the message to:")
    for i, d in enumerate(dialogs):
        print(f"{i}: {d.name} ({d.id})")

    group_index = int(input("Enter the group number: "))
    group = dialogs[group_index]

    # Confirm the details
    print(f"✅ Confirm the following:")
    print(f"Message:\n{message}")
    print(f"Interval: {interval} minutes")
    print(f"Group: {group.name} ({group.id})")
    confirm = input("Type 'yes' to confirm or 'cancel' to abort: ").lower()

    if confirm != 'yes':
        print("Cancelled.")
        return

    # Send messages at the specified interval
    print("Scheduled messages successfully! The bot will keep sending them.")
    while True:
        await client.send_message(group.id, message)
        await asyncio.sleep(interval * 60)  # Wait for the specified interval before sending again

if __name__ == '__main__':
    asyncio.run(main())
