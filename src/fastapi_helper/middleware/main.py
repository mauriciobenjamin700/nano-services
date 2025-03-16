from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn

app = FastAPI()

class CustomErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except ValidationError as e:
            # Formatação de erro de validação do Pydantic
            return JSONResponse(
                status_code=422,
                content={"detail": "Validation Error", "errors": e.errors()},
            )
        except HTTPException as e:
            # Formatação de erro HTTP (por exemplo, 404, 400, etc.)
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
            )
        except Exception as e:
            # Formatação de erro genérico
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error: " + str(e)},
            )

# Adicionando o middleware ao aplicativo
app.add_middleware(CustomErrorMiddleware)

# Sobrescrevendo o manipulador de exceções para erros de validação do Pydantic
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    pydantic_errors = exc.errors()
    msg = pydantic_errors[0]["msg"]
    loc, field = pydantic_errors[0]["loc"]
    detail = f"{msg} {field} in {loc}"
    
    return JSONResponse(
        status_code=422,
        content={"detail": detail}
    )
    
# Sobrescrevendo o manipulador de exceções para erros HTTP


# Exemplo de rota para testar o middleware
@app.post("/test")
async def test_route(data: dict):
    if "error" in data:
        raise HTTPException(status_code=400, detail="Erro customizado")
    return {"message": "Tudo certo!"}

# Exemplo de rota para testar validação do Pydantic
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
async def create_item(item: Item):
    return item



if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8001
    )