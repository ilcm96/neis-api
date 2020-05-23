import asyncio
from aiohttp import ClientSession
from rejson import Client, Path


async def get_schoolcode(url, session):
    json_data = {}
    try:
        async with session.get(url, ssl=False) as resp:
            raw = await resp.json()
            data = raw["resultSVO"]["data"]["orgDVOList"]
            if data == []:
                pass
            else:
                data = raw["resultSVO"]["data"]["orgDVOList"][0]
                json_data.update(
                    {
                        "name": data["kraOrgNm"],
                        "address": data["zipAdres"],
                        "org": data["atptOfcdcNm"],
                        "schoolcode": data["orgCode"],
                        "schooltype": data["schulKndScCode"],
                    }
                )
                return json_data
    except:
        pass


async def send_schoolcode(schoolname: str, rj):
    try:
        if rj.exists(schoolname):
            result = rj.jsonget(schoolname, no_escape=True)
            return result
        else:
            result = {}
            resp_list = []
            tasks = []
            url = "https://par.{}.go.kr/spr_ccm_cm01_100.do?kraOrgNm=" + schoolname
            org_list = [
                "goe",  # 경기 2438
                "sen",  # 서울 1367
                "gne",  # 경남 975
                "kbe",  # 경북 937
                "jne",  # 전남 833
                "jbe",  # 전북 775
                "cne",  # 충남 726
                "cbe",  # 충북 645
                "gwe",  # 강원 645
                "pen",  # 부산 640
                "ice",  # 인천 527
                "dge",  # 대구 461
                "gen",  # 광주 323
                "dje",  # 대전 309
                "use",  # 울산 246
                "jje",  # 제주 193
                "sje",  # 세종 91
            ]
            async with ClientSession() as session:
                for org in org_list:
                    task = asyncio.ensure_future(
                        get_schoolcode(url.format(org), session)
                    )
                    tasks.append(task)
                resp = await asyncio.gather(*tasks)
                for i in range(len(resp)):
                    if resp[i] is not None:
                        resp_list.append(resp[i])
                for i in range(len(resp_list)):
                    result.update({"schoolcode": resp_list})
                rj.jsonset(schoolname, Path.rootPath(), result)
                rj.expire(schoolname, 604800)  # 1주일
                return result
    except:
        # 위 else 구문에서 redis에 키-값을 넣고 Expire를 설정하는 부분만 제외
        result = {}
        resp_list = []
        tasks = []
        url = "https://par.{}.go.kr/spr_ccm_cm01_100.do?kraOrgNm=" + schoolname
        org_list = [
            "goe",  # 경기 2438
            "sen",  # 서울 1367
            "gne",  # 경남 975
            "kbe",  # 경북 937
            "jne",  # 전남 833
            "jbe",  # 전북 775
            "cne",  # 충남 726
            "cbe",  # 충북 645
            "gwe",  # 강원 645
            "pen",  # 부산 640
            "ice",  # 인천 527
            "dge",  # 대구 461
            "gen",  # 광주 323
            "dje",  # 대전 309
            "use",  # 울산 246
            "jje",  # 제주 193
            "sje",  # 세종 91
        ]
        async with ClientSession() as session:
            for org in org_list:
                task = asyncio.ensure_future(get_schoolcode(url.format(org), session))
                tasks.append(task)
            resp = await asyncio.gather(*tasks)
            for i in range(len(resp)):
                if resp[i] is not None:
                    resp_list.append(resp[i])
            for i in range(len(resp_list)):
                result.update({"schoolcode": resp_list})
            return result


if __name__ == "__main__":
    rj = Client(host="0.0.0.0", port=6379, decode_responses=True)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(send_schoolcode("서일초등학교", rj))
    result = loop.run_until_complete(future)
    print(result)
