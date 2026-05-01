"""Improved API data fetcher for Day 03 with detailed comments.

This script is an enhanced and well-documented version of the Day 02
`api_data_fetcher.py`. It demonstrates good structure for DevOps scripts:

- Clear separation of concerns via functions
- Basic and robust exception handling for network and file operations
- Command-line arguments for flexibility (`--limit`, `--output`)
- Helpful comments explaining what each block does and why

Run this script from the repository root:

python day-03/improved_api_fetcher.py --limit 5

The script will attempt to fetch data from the public JSONPlaceholder API.
If the network request fails, it will try to fall back to a local cached
`day-02/output.json` file (if available). All errors are handled gracefully
and reported to the user instead of letting the script crash.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional

import requests

# Configure a simple logger so users can see what's happening.
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Default API and file settings. Keeping them as module-level constants
# makes it easy to change without digging into the code.
API_URL = "https://jsonplaceholder.typicode.com/todos"
DEFAULT_TIMEOUT = 10  # seconds for network operations
LOCAL_FALLBACK = Path(__file__).parents[1] / "day-02" / "output.json"


def fetch_data(url: str, timeout: int = DEFAULT_TIMEOUT) -> List[Dict]:
    """Fetch JSON from `url` and return parsed data.

    This function raises `requests.RequestException` on network failures so the
    caller can decide how to handle retries or fallback strategies.
    """
    logger.info("Fetching data from API: %s", url)
    response = requests.get(url, timeout=timeout)
    # `raise_for_status` will raise an HTTPError for 4xx/5xx responses which we
    # catch in the caller. It's a good practice to handle non-2xx codes explicitly.
    response.raise_for_status()
    return response.json()


def load_local_json(path: Path) -> Optional[List[Dict]]:
    """Attempt to read a JSON file from disk and return the parsed content.

    Returns None if the file doesn't exist or cannot be decoded as JSON.
    """
    try:
        logger.info("Attempting to load local fallback file: %s", path)
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        logger.warning("Fallback file not found: %s", path)
        return None
    except json.JSONDecodeError as exc:
        logger.error("Fallback file exists but contains invalid JSON: %s", exc)
        return None


def process_todos(todos: List[Dict], limit: int = 10) -> List[Dict]:
    """Extract a smaller, more useful representation of todo items.

    We only keep a few fields and normalize names to be more Pythonic. The
    `limit` parameter keeps the output concise for demonstrations and terminal
    viewing. Processing logic should be deterministic and well-typed.
    """
    processed: List[Dict] = []
    for item in todos[:limit]:
        # Use `.get()` to avoid KeyError in case the API shape changes; this
        # is defensive programming which is important for long-running scripts.
        processed.append(
            {
                "id": item.get("id"),
                "user_id": item.get("userId"),
                "title": item.get("title"),
                # Convert the boolean `completed` into a human-friendly label
                "status": "completed" if item.get("completed") else "pending",
            }
        )
    return processed


def print_summary(processed: List[Dict]) -> None:
    """Print the processed items and basic statistics.

    Keeping output human-readable is critical for quick debugging and
    verification when running scripts interactively.
    """
    if not processed:
        logger.info("No items to display.")
        return

    completed = sum(1 for it in processed if it.get("status") == "completed")
    total = len(processed)
    pending = total - completed

    logger.info("Processed TODO Items (showing %d):", total)
    for todo in processed:
        print(f"- ID: {todo['id']}, User: {todo['user_id']}, Status: {todo['status']}, Title: {todo['title']}")

    print("\nSummary:")
    print(f"Total items: {total}")
    print(f"Completed: {completed}")
    print(f"Pending: {pending}")


def save_to_json(data: List[Dict], output: Path) -> bool:
    """Save processed data to `output` JSON file.

    Returns True on success, False on failure. We catch IO-related errors and
    report them without raising, which keeps the script user-friendly.
    """
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        logger.info("Saved processed data to: %s", output)
        return True
    except OSError as exc:
        logger.error("Failed to write output file %s: %s", output, exc)
        return False


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments to make the script flexible.

    Having CLI arguments is a small, but practical improvement that lets you
    reuse the same script for different limits or output locations without
    changing the code.
    """
    parser = argparse.ArgumentParser(description="Improved API data fetcher for Day 03")
    parser.add_argument("--limit", "-n", type=int, default=10, help="Number of todo items to process")
    parser.add_argument("--output", "-o", type=Path, default=Path(__file__).with_name("output.json"), help="Output JSON file path")
    parser.add_argument("--no-fallback", dest="no_fallback", action="store_true", help="Do not attempt local fallback if the API fails")
    return parser.parse_args()


def main() -> None:
    """Main entry point: orchestrates fetching, processing, printing, and saving."""
    args = parse_args()

    todos_raw: Optional[List[Dict]] = None

    # Step 1: Try to fetch from network and handle network-related errors.
    try:
        todos_raw = fetch_data(API_URL)
    except requests.RequestException as exc:
        # Instead of crashing, give a clear message and optionally try a
        # local cached file. In production, you might also implement retries.
        logger.warning("Network request failed: %s", exc)

        if not args.no_fallback:
            todos_raw = load_local_json(LOCAL_FALLBACK)
        else:
            logger.info("Local fallback disabled by --no-fallback flag.")

    # If we still don't have data, exit gracefully with a helpful message.
    if not todos_raw:
        logger.error("No data available. Exiting without processing.")
        return

    # Step 2: Process the raw data into a smaller, predictable structure.
    processed = process_todos(todos_raw, limit=args.limit)

    # Step 3: Print a human-friendly summary to the terminal.
    print_summary(processed)

    # Step 4: Save results to disk, but don't raise on failure.
    save_to_json(processed, args.output)


if __name__ == "__main__":
    main()
