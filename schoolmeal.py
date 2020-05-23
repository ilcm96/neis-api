import requests
import re
from rejson import Client, Path


def get_meal(url):
    # 나이스 급식 페이지 파싱
    response = requests.get(url).text
    # <tbody> 부분만 data에 저장
    data = response[response.find("<tbody>") : response.find("</tbody>")]

    # 정규식으로 <div> 부분만을 잘라서 data에 List로 저장
    regex = re.compile(r"[\n\r\t]")
    data = regex.sub("", data)
    regex = re.compile(r"<div>(.*?)</div>", re.S | re.M)
    data = regex.findall(data)

    # 메뉴를 담을 Ditctionary 생성
    lunch = {}

    # Dictionary 생성
    for dat in data:
        date = re.findall(r"[0-3][0-9]", dat[0:2])
        menu = dat[dat.find("[중식]<br />") :]
        if not date:
            date = dat[0:1]
            if date == "" or date == " ":
                continue
        if type(date) == list:
            date = date[0]

        # <br> 태그에 맞춰서 자른후 menu(List)에 저장
        menu = menu.split("<br />")
        # menu의 첫항목인 [중식] 제거
        menu.remove(menu[0])

        # 쓸모없는 문자 제거
        i = 0
        menu_num = len(menu) - 1
        while i <= menu_num:
            menu[i] = (
                menu[i]
                .replace(" ", "")
                .replace("*", "")
                .replace("@", "")
                .replace("s", "")
                .replace("(청)", "")
                .replace("(청 )", "")
                .replace("&amp;", " & ")
                .replace("1.", "")
                .replace("2.", "")
                .replace("3.", "")
                .replace("4.", "")
                .replace("5.", "")
                .replace("6.", "")
                .replace("7.", "")
                .replace("8.", "")
                .replace("9.", "")
                .replace("10.", "")
                .replace("11.", "")
                .replace("12.", "")
                .replace("13.", "")
                .replace("14.", "")
                .replace("15.", "")
                .replace("16.", "")
                .replace("17.", "")
                .replace("18.", "")
                .replace("1", "")
                .replace("2", "")
                .replace("3", "")
                .replace("4", "")
                .replace("5", "")
                .replace("6", "")
                .replace("7", "")
                .replace("8", "")
                .replace("9", "")
                .replace("10.", "")
                .replace("11", "")
                .replace("12", "")
                .replace("13", "")
                .replace("14", "")
                .replace("15", "")
                .replace("16", "")
                .replace("17", "")
                .replace("18", "")
            )
            i += 1

        # 급식이 없는 날은 None으로 저장
        if not menu:
            menu = "None"

        # lunch Dictionary에 날짜와 menu 저장
        lunch.update({date: menu})

    return lunch


def get_region(schoolcode):
    regionID = [
        ["B", "sen"],
        ["C", "pen"],
        ["D", "dge"],
        ["E", "ice"],
        ["F", "gen"],
        ["G", "dje"],
        ["H", "use"],
        ["I", "sje"],
        ["J", "goe"],
        ["K", "kwe"],
        ["M", "cbe"],
        ["N", "cne"],
        ["P", "jbe"],
        ["Q", "jne"],
        ["R", "gbe"],
        ["S", "gne"],
        ["T", "jje"],
    ]

    i = 0
    while True:
        if schoolcode[0] == regionID[i][0]:
            return regionID[i][1]
        else:
            i += 1


def send_schoolmeal(schoolcode, schooltype, year, month, rj):
    if len(str(month)) == 1:
        month = "0" + str(month)

    jh_key = schoolcode + "-" + schooltype + "-" + year + "-" + month
    try:
        if rj.exists(jh_key):
            result = rj.jsonget(jh_key, no_escape=True)
            return result
        else:
            url = (
                "https://stu."
                + get_region(schoolcode)
                + ".go.kr/sts_sci_md00_001.do?schulCode="
                + schoolcode
                + "&schulCrseScCode="
                + str(schooltype)
                + "&ay="
                + str(year)
                + "&mm="
                + str(month)
            )
            result = get_meal(url)
            rj.jsonset(jh_key, Path.rootPath(), result)
            rj.expire(jh_key, 604800)  # 1주일
            return result
    except:
        # 위 else 구문에서 redis에 키-값을 넣고 Expire를 설정하는 부분만 제외
        url = (
            "https://stu."
            + get_region(schoolcode)
            + ".go.kr/sts_sci_md00_001.do?schulCode="
            + schoolcode
            + "&schulCrseScCode="
            + str(schooltype)
            + "&ay="
            + str(year)
            + "&mm="
            + str(month)
        )
        result = get_meal(url)
        return result


if __name__ == "__main__":
    rj = Client(host="0.0.0.0", port=6379, decode_responses=True)
    result = send_schoolmeal("J100000815", "4", "2019", "03", rj)
    print(result)
