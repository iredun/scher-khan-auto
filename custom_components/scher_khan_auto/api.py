"""Sample API Client."""
import asyncio
import logging
import socket

import aiohttp

TIMEOUT = 10


_LOGGER: logging.Logger = logging.getLogger(__package__)


class ScherKhanAutoApiClient:
    __headers = {
        "Content-type": "application/json; charset=UTF-8",
        "origin": "https://mf-t.ru",
        "referer": "https://mf-t.ru/",
    }
    __api_url = "https://api.mf-t.ru/v3/"
    __auth_api_url = "https://auth.mf-t.ru/v1/"

    user_token = None
    __username = None
    __password = None
    __session = None

    def __init__(
        self,
        username: str = None,
        password: str = None,
        user_token: str = None,
        session=None,
    ) -> None:
        """API Client."""
        if session is None:
            session = aiohttp.ClientSession(
                timeout=TIMEOUT,
                loop=asyncio.get_event_loop(),
            )
        self.__session = session

        if user_token:
            self.user_token = user_token
            self.__headers["Authorization"] = f"Token {self.user_token}"
        else:
            self.__username = username
            self.__password = password

    async def async_get_user(self) -> dict:
        """Get user data"""
        response = await self.api_wrapper("get", f"{self.__auth_api_url}user/")
        return response

    async def async_get_cars(self):
        """Get user cars"""
        response = await self.api_wrapper("get", f"{self.__api_url}cars/")
        return response

    async def async_send_car_command(self, car_id: int, command: str) -> dict:
        """Send command to car"""
        _LOGGER.info(f"Sending command {command} to car_id {car_id}")
        response = await self.api_wrapper(
            "post",
            f"{self.__api_url}cars/{car_id}/command/",
            data={
                "car_id": car_id,
                "cmd": command,
            },
        )
        return response

    async def async_login(self) -> str:
        """Login user."""
        if self.user_token:
            _LOGGER.info(f"Login user by token")

        _LOGGER.info(f"Login user - {self.__username}")
        response = await self.api_wrapper(
            "post",
            f"{self.__auth_api_url}login/",
            data={
                "email": self.__username,
                "password": self.__password,
            },
        )
        if response and "key" in response:
            _LOGGER.info(f"Login success")
            self.user_token = response["key"]
            self.__headers["Authorization"] = f"Token {self.user_token}"
            return self.user_token
        else:
            _LOGGER.info(f"Login wrong - {response}")
            return None

    async def api_wrapper(
        self, method: str, url: str, data: dict = None, headers: dict = None
    ) -> dict:
        """Get information from the API."""
        if headers is None:
            headers = self.__headers
        if data is None:
            data = {}

        try:
            if method == "get":
                response = await self.__session.get(url, headers=headers)
                return await response.json()

            elif method == "put":
                response = await self.__session.put(url, headers=headers, json=data)
                return await response.json()

            elif method == "patch":
                response = await self.__session.patch(url, headers=headers, json=data)
                return await response.json()

            elif method == "post":
                response = await self.__session.post(url, headers=headers, json=data)
                return await response.json()

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)
