import json
import os
import argparse

def save_client_cache(client_id, client_secret, filename='client_cache.json'):
    """
    Saves client credentials to a JSON cache file.

    Args:
        client_id (str): Client identifier.
        client_secret (str): Client secret string.
        filename (str): Path to cache file (default: client_cache.json).
    """
    cache_data = {
        'client_id': client_id,
        'client_secret': client_secret
    }

    try:
        with open(filename, 'w') as f:
            json.dump(cache_data, f)
        print("Credentials saved successfully.")
    except IOError as e:
        print(f"Error saving cache: {e}")

def load_client_cache(filename='client_cache.json'):
    """
    Loads client credentials from cache file.

    Args:
        filename (str): Path to cache file (default: client_cache.json).

    Returns:
        tuple: (client_id, client_secret) or (None, None) if not found.
    """
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data.get('client_id'), data.get('client_secret')
    except FileNotFoundError:
        print("Cache file not found.")
    except json.JSONDecodeError:
        print("Invalid cache format.")
    except Exception as e:
        print(f"Error loading cache: {e}")

    return None, None

def main():
    parser = argparse.ArgumentParser(description="A sample CLI tool for managing client credentials.")

    parser.add_argument("--client_id", type=str, help="Enter Spotify Client ID")
    parser.add_argument("--client_secret", type=str, help="Enter Spotify Client Secret")
    parser.add_argument("--load", action="store_true", help="Load credentials from cache")

    args = parser.parse_args()

    if args.load:
        client_id, client_secret = load_client_cache()
        if client_id and client_secret:
            print(f"Loaded Client ID: {client_id}")
            print(f"Loaded Client Secret: {client_secret}")
        else:
            print("No cached credentials found.")
    elif args.client_id and args.client_secret:
        save_client_cache(args.client_id, args.client_secret)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
