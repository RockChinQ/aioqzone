from abc import ABC
from abc import abstractmethod
import asyncio

from qqqr.encrypt import gtk

from ..interface.hook import Emittable
from ..interface.hook import LoginEvent


class Loginable(ABC, Emittable[LoginEvent]):
    def __init__(self, uin: int) -> None:
        super().__init__()
        self.uin = uin
        self._cookie = {}
        self.lock = asyncio.Lock()

    @property
    def cookie(self) -> dict[str, str]:    # type: ignore
        """Get cookie in any way. Allow cached result.

        Returns:
            int: cookie. Cached cookie is preferable.
        """
        return self._cookie

    @abstractmethod
    async def _new_cookie(self) -> dict[str, str]:
        return

    async def new_cookie(self):
        """Get a new cookie. Means, cached cookie is not allowed.

        Returns:
            int: cookie. Shouldn't be a cached one.
        """
        if self.lock.locked():
            # if there is coro. updating cookie, then wait for its result.
            async with self.lock:
                return self.cookie
        else:
            # let the first coro. get result from Qzone.
            async with self.lock:
                self._cookie = await self._new_cookie()
                return self._cookie

    @property
    def gtk(self) -> int:
        """cal gtk from pskey.

        Returns:
            int: gtk. NOTE: 0 denotes no-login.
        """
        if (pskey := self.cookie.get('p_skey')) is None: return 0
        return gtk(pskey)
