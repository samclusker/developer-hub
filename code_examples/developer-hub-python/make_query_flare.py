import asyncio
import json

import aiohttp
from web3 import AsyncHTTPProvider, AsyncWeb3
from web3.middleware.geth_poa import async_geth_poa_middleware


async def main():
    registry_addr = "0xaD67FE66660Fb8dFE9d6b1b4240d8650e30F6019"
    w3 = AsyncWeb3(
        AsyncHTTPProvider("https://rpc.ankr.com/flare"),
        middlewares=[async_geth_poa_middleware],
    )
    params = {
        "module": "contract",
        "action": "getabi",
        "address": registry_addr,
    }
    async with (
        aiohttp.ClientSession() as session,
        session.get(
            "https://flare-explorer.flare.network/api", params=params
        ) as response,
    ):
        res = await response.json()
        abi = json.loads(res["result"])
    contract = w3.eth.contract(address=registry_addr, abi=abi)
    res = await contract.functions.getContractAddressByName("WNat").call()
    print(
        f"WNat address: {res}"
    )  # WNat address: 0x1D80c49BbBCd1C0911346656B529DF9E5c2F783d


if __name__ == "__main__":
    asyncio.run(main())