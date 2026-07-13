from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse


def success_response(meg: str = "响应成功",data = None):
    content = {
        "code": 200,
        "message": meg,
        "data": data
    }

    return JSONResponse(content=jsonable_encoder(content))