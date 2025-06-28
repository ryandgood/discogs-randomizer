from typing import List
from pathlib import Path
import httpx
import json
from ..models.discogs import CollectionResponse, Release
import pydantic
from rich import pretty
class DiscogsClient:
    BASE_URL = "https://api.discogs.com"

    def __init__(self, token: str, username: str):
        self.headers = {
            "User-Agent": "Discogs-Randomizer/1.0",
        }
        if token:
            self.headers["Authorization"] = f"Discogs token={token}"
        self.client = httpx.AsyncClient(headers=self.headers)
        self.username = username

    async def get_collection_page(
        self,
        username: str,
        folder_id: int = 0, # this corresponds to the "All" meta folder
        page: int = 1,
        per_page: int = 50
    ) -> CollectionResponse:
        url = f"{self.BASE_URL}/users/{username}/collection/folders/{folder_id}/releases"
        params = {
            "page": page,
            "per_page": per_page
        }
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return CollectionResponse.model_validate_json(response.text)


    async def get_collection(
        self,
        username: str,
        folder_id: int = 1,
        per_page: int = 50,
        only_first_page: bool = False
    ) -> List[Release]:
        """
        Get all releases or just the first page.

        Returns:
            A list of Release objects.
        """
        releases: List[Release] = []
        page = 1

        while True:
            collection = await self.get_collection_page(username, folder_id, page, per_page)
            releases.extend(collection.releases)

            if only_first_page or page >= collection.pagination.pages:
                break
            page += 1

        return releases

    async def sync(
        self,
        folder_id: int = 1,
        per_page: int = 50,
        output_file: str = "collection.json"
    ) -> bool:
        """
        Sync method: checks if item count has changed (based on saved JSON file)
        and updates the local collection file if needed.

        Returns True if an update occurred, False otherwise.
        """
        output_path = Path(output_file)

        try:
            # Step 1: Fetch current collection metadata
            first_page = await self.get_collection_page(self.username, folder_id, page=1, per_page=1)
            current_count = first_page.pagination.items

            # Step 2: If file does not exist, force full sync
            if not output_path.exists():
                print("Collection file not found — performing full sync.")
                all_releases = await self.get_collection(self.username, folder_id, per_page)
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump([r.model_dump() for r in all_releases], f, indent=2)
                return True

            # Step 3: Load existing JSON and get saved count
            with open(output_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
            last_count = len(existing)

            # Step 4: Compare counts
            if current_count == last_count:
                print("Item count unchanged, skipping update.")
                return False

            print(f"Item count changed: {last_count} → {current_count}")
            all_releases = await self.get_collection(self.username, folder_id, per_page)

            # Step 5: Save updated collection
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump([r.model_dump() for r in all_releases], f, indent=2)

            return True
        finally:
            await self.close()

    async def close(self):
        await self.client.aclose()
