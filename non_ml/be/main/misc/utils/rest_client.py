import httpx
from typing import Any, Dict, Optional


class RestAPIClient:
    def __init__(self, base_url: str, token: Optional[str] = None):
        self.base_url = base_url
        self.token = token

    async def _request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}{endpoint}"
            headers = headers or {}
            if self.token:
                headers["Authorization"] = f"Bearer {self.token}"
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json,
            )
            response.raise_for_status()
            return response

    async def get(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        return await self._request("GET", endpoint, headers=headers, params=params)

    async def post(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        return await self._request("POST", endpoint, headers=headers, json=json)

    async def put(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        return await self._request("PUT", endpoint, headers=headers, json=json)

    async def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        return await self._request("DELETE", endpoint, headers=headers, params=params)
