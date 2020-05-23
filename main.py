from fastapi import FastAPI
from rejson import Client
import schoolcode
import schoolmeal

app = FastAPI()

# RedisJSON 연결
rj = Client(host="172.17.0.4", port=6379, decode_responses=True, socket_timeout=1 * 0.5)


@app.get("/schoolcode/{schoolname}")
async def school_code(schoolname: str):
    result = await schoolcode.send_schoolcode(schoolname, rj)
    return result


@app.get("/schoolmeal/{schoolcode}/{schooltype}/{year}/{month}")
def school_meal(schoolcode, schooltype, year, month):
    return schoolmeal.send_schoolmeal(schoolcode, schooltype, year, month, rj)
