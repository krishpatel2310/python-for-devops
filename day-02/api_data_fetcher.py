"""Fetch and process API data for Day 02 practice.

This script pulls todo items from JSONPlaceholder, extracts useful fields,
prints a concise report, and saves processed data to a JSON file.
"""

from pathlib import Path
import json
import requests


API_URL = "https://jsonplaceholder.typicode.com/todos"
OUTPUT_FILE = Path(__file__).with_name("output.json")
TIMEOUT_SECONDS = 10


def fetch_data(url: str) -> list[dict]:
	"""Fetch JSON data from a public API endpoint."""
	response = requests.get(url, timeout=TIMEOUT_SECONDS)
	response.raise_for_status()
	return response.json()


def process_todos(todos: list[dict], limit: int = 10) -> list[dict]:
	"""Extract meaningful todo fields and derive status labels."""
	processed = []
	for item in todos[:limit]:
		processed.append(
			{
				"id": item.get("id"),
				"user_id": item.get("userId"),
				"title": item.get("title"),
				"status": "completed" if item.get("completed") else "pending",
			}
		)
	return processed


def print_summary(processed_todos: list[dict]) -> None:
	"""Print processed todo data and basic stats to terminal."""
	completed_count = sum(1 for item in processed_todos if item["status"] == "completed")
	pending_count = len(processed_todos) - completed_count

	print("Processed TODO Items:")
	for todo in processed_todos:
		print(
			f"- ID: {todo['id']}, User: {todo['user_id']}, "
			f"Status: {todo['status']}, Title: {todo['title']}"
		)

	print("\nSummary:")
	print(f"Total items: {len(processed_todos)}")
	print(f"Completed: {completed_count}")
	print(f"Pending: {pending_count}")


def save_to_json(data: list[dict], output_file: Path) -> None:
	"""Save processed data to JSON file."""
	with output_file.open("w", encoding="utf-8") as file:
		json.dump(data, file, indent=2)


def main() -> None:
	"""Run the API fetch workflow."""
	try:
		todos = fetch_data(API_URL)
		processed_todos = process_todos(todos)
		print_summary(processed_todos)
		save_to_json(processed_todos, OUTPUT_FILE)
		print(f"\nProcessed data saved to: {OUTPUT_FILE}")
	except requests.RequestException as exc:
		print(f"API request failed: {exc}")


if __name__ == "__main__":
	main()
