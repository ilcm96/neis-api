# neis-api

학교 코드와 급식을 제공하는 API 입니다.

## 학교 코드

### 요청

`GET /schoolcode/{학교명}`

### 예시

`GET /schoolcode/서일초등학교`

```
{
  "schoolcode": [
    {
      "name": "서울서일초등학교",
      "address": "서울특별시 서초구 서초1동",
      "org": "서울특별시교육청",
      "schoolcode": "B100000763",
      "schooltype": "02"
    },
    {
      "name": "전주서일초등학교",
      "address": "전라북도 전주시 완산구 서신동",
      "org": "전라북도교육청",
      "schoolcode": "P100001446",
      "schooltype": "02"
    },
    {
      "name": "서일초등학교병설유치원",
      "address": "광주 북구 일곡동",
      "org": "광주광역시교육청",
      "schoolcode": "F100000319",
      "schooltype": "01"
    }
  ]
}
```

## 급식

### 요청

`GET /schoolmeal/{학교코드}/{학교종류}/{연도}/{월}`

> **학교코드**와 **학교종류**는 [학교 코드 API](https://github.com/ilcm96/neis-api/blob/master/README.md#학교-코드)의 `schoolcode`, `schooltype`의 값입니다.

### 예시

`GET /schoolmeal/J100000815/4/2019/03`

```
{
    1: "None",
    2: "None",
    3: "None",
    4: [
        "쇠고기미역국",
        "햄버거스테이크/청양소스",
        "콘치즈구이",
        "배추김치",
        "소라곤약초무침",
        "기장밥",
        "요거타임"
    ],
    5: [
        "찰보리밥",
        "햄모듬찌개",
        "양배추샐러드(참깨소스)",
        "배추겉절이",
        "돈까스(수제,소스)"
    ],
    ...
}
```

## 배포

학교 코드는 거의 변하지 않는 반면 API 호출이 상당히 오래 걸리므로 [RedisJson](https://github.com/RedisJSON/RedisJSON)를 사용해 캐싱합니다.  

fast-api 백엔드는 포함된 Dockerfile로, Redis는 [RedisJson 이미지](https://hub.docker.com/r/redislabs/rejson/)를 사용하거나 RedisJson 모듈을 [빌드](https://oss.redislabs.com/redisjson/#building-and-loading-the-module)해서 사용하면 됩니다.  
RedisJson 세팅 후 `main.py`의 Redis [연결 부분](https://github.com/ilcm96/neis-api/blob/master/main.py#L9)을 수정하면 됩니다.  
만약 캐싱 기간을 기본값인 1주일 보다 늘리고 싶다면 `schoolcode.py`와 `schoolmeal.py`의 `rj.expire` 부분을 수정하면 됩니다.

## 마치며...

[neis-api.ilcm96.me](https://neis-api.ilcm96.me/)를 통해 직접 배포하지 않고 사용할 수는 있지만, 서버 유지 보수는 시간이 없어 접속이 불가할 수도 있으므로 간단한 테스트 용도로만 사용하는 것을 권장합니다.