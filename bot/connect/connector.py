import json
import asyncio
import cloudscraper
from bot.utils import logger
from bot.config import settings
from pathlib import Path

async def get_payload(session_name, scraper):
    url = f"https://clicker-api.crashgame247.io/user/wallet/proof"
    
    try:
        response = scraper.get(url)
        
        if response.status_code == 200:
            json_data = response.json()
            payload = json_data.get("payload")
            if settings.DEBUG:
                logger.debug(f"<light-yellow>{session_name}</light-yellow> | Connect Payload: {payload}")
            return payload
        else:
            try:
                error_data = response.json()
                logger.error(f"<light-yellow>{session_name}</light-yellow> | 🚫 Payload generation <red>error</red>: {error_data}")
            except json.JSONDecodeError:
                logger.error(f"<light-yellow>{session_name}</light-yellow> | 💀 Failed to decode error response: {response.content}")
            
            if response.status_code == 500:
                return False
    
    except cloudscraper.exceptions.CloudflareChallengeError as e:
        logger.error(f"<light-yellow>{session_name}</light-yellow> | 🚫 Cloudflare challenge <red>error</red> occurred: {e}")
    except Exception as e:
        logger.error(f"<light-yellow>{session_name}</light-yellow> | 🤷‍♂️ Unexpected <red>error</red>: {str(e)}")

async def generate_info(session_name, scraper):
    payload = await get_payload(session_name, scraper)
    script_dir = Path(__file__).resolve().parent
    generator_path = script_dir / 'generator.cjs'
    process = await asyncio.create_subprocess_exec(
        'node', str(generator_path), "https://clicker.crashgame247.io/", payload,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        logger.error(f"<light-yellow>{session_name}</light-yellow> | 🚫 Generate Wallet Info <red>Error</red> occurred: {stderr.decode()}")
        return None
    result_json = json.loads(stdout.decode())
    return result_json

async def connect_wallet(session_name, scraper):
    try:
        wallet_info = await generate_info(session_name, scraper)
        if settings.DEBUG:
            logger.debug(f"<light-yellow>{session_name}</light-yellow> | Generated Wallet: {wallet_info}")
        if not wallet_info:
            logger.error(f"<light-yellow>{session_name}</light-yellow> | 💀 Failed to retrieve wallet info.")
            return

        connect_info = {
            "address": wallet_info['address'],
            "network": wallet_info['network'],
            "public_key": wallet_info['public_key'],
            "proof": {
                "timestamp": wallet_info['proof']['timestamp'],
                "domain": {
                    "lengthBytes": 23,
                    "value": "clicker.crashgame247.io"
                },
                "signature": wallet_info['proof']['signature'],
                "payload": wallet_info['proof']['payload'],
                "state_init": wallet_info['proof']['state_init']
            }
        }

        url = "https://clicker-api.crashgame247.io/user/wallet/connect"
        
        response = scraper.patch(url, json=connect_info)
        
        if response.status_code == 200:
            json_data = response.json()
            nftCount = json_data.get("nftCount")
            if nftCount == 0:
                logger.info(f"<light-yellow>{session_name}</light-yellow> | ⚡️ Wallet <green>connected successfully!</green> Ton Address: <light-yellow>{wallet_info['wallet']['ton_address']}</light-yellow> <cyan>(Wallet info saved to connected_wallets.txt)</cyan>")
                
                with open("connected_wallets.txt", "a", encoding="utf-8") as f:
                    f.write(f"-------------------------\n")
                    f.write(f"┌──Session Name: {session_name}\n")
                    f.write(f"├──Ton Address: {wallet_info['wallet']['ton_address']}\n")
                    f.write(f"└──Mnemonics: {wallet_info['wallet']['mnemonics']}\n")
                    f.write(f"-------------------------\n")
                
                with open("connected_wallets.json", "a") as json_file:
                    entry = {session_name: wallet_info}
                    json_string = json.dumps(entry, indent=4, ensure_ascii=False)
                    json_file.write(json_string)
                    json_file.write(",\n")
                return True
            else:
                logger.error(f"<light-yellow>{session_name}</light-yellow> | 🚫 Error in connecting wallet: No payload in response.")
                return False
        else:
            logger.error(f"<light-yellow>{session_name}</light-yellow> | 🚫 Failed to connect wallet. Status code: {response.status_code}")
            return False
        
    except cloudscraper.exceptions.CloudflareChallengeError as e:
        logger.error(f"<light-yellow>{session_name}</light-yellow> | 🚫 Cloudflare challenge error: {e}")
        return False
    except Exception as e:
        logger.error(f"<light-yellow>{session_name}</light-yellow> | 🤷‍♂️ Unexpected error: {str(e)}")
        return False