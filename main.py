# main.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator # Use field_validator for Pydantic v2+
from typing import Union # Added Union
from fastapi.exceptions import RequestValidationError
# Import the new functions along with the old ones
from app.operations import add, subtract, multiply, divide, power, modulo
import uvicorn
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Setup templates directory (Make sure you have a 'templates' folder)
templates = Jinja2Templates(directory="templates")

# Pydantic model for request data
class OperationRequest(BaseModel):
    a: Union[int, float] = Field(..., description="The first number") # Allow int or float
    b: Union[int, float] = Field(..., description="The second number") # Allow int or float

    # Note: Pydantic v2 automatically handles type validation.
    # The validator below is redundant if a/b are already typed as Union[int, float].
    # If using Pydantic v1, keep the @validator decorator.
    # @field_validator('a', 'b')
    # def validate_numbers(cls, value):
    #     if not isinstance(value, (int, float)):
    #         raise ValueError('Both a and b must be numbers.')
    #     return value

# Pydantic model for successful response
class OperationResponse(BaseModel):
    result: Union[int, float] = Field(..., description="The result of the operation") # Allow int or float

# Pydantic model for error response
class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")

# Custom Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException on {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extracting error messages might need adjustment based on Pydantic version
    try:
        error_messages = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
    except (IndexError, KeyError):
        error_messages = str(exc.errors()) # Fallback for different error structures
    logger.error(f"ValidationError on {request.url.path}: {error_messages}")
    return JSONResponse(
        status_code=400, # Use 422 for validation errors as per FastAPI convention? Or 400? Stick to 400 for now.
        content={"error": f"Invalid input: {error_messages}"},
    )

@app.get("/")
async def read_root(request: Request):
    """
    Serve the index.html template.
    Make sure you have an 'index.html' file in the 'templates' directory.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/add", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def add_route(operation: OperationRequest):
    """
    Add two numbers.
    """
    try:
        result = add(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Add Operation Error: {str(e)}")
        # Raise generic 400 for operation errors if not caught specifically
        raise HTTPException(status_code=400, detail=f"Calculation error: {str(e)}")

@app.post("/subtract", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def subtract_route(operation: OperationRequest):
    """
    Subtract two numbers.
    """
    try:
        result = subtract(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Subtract Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Calculation error: {str(e)}")

@app.post("/multiply", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def multiply_route(operation: OperationRequest):
    """
    Multiply two numbers.
    """
    try:
        result = multiply(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Multiply Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Calculation error: {str(e)}")

@app.post("/divide", response_model=OperationResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def divide_route(operation: OperationRequest):
    """
    Divide two numbers.
    """
    try:
        result = divide(operation.a, operation.b)
        return OperationResponse(result=result)
    except ValueError as e: # Catch division by zero specifically
        logger.error(f"Divide Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e: # Catch other potential errors
        logger.error(f"Divide Operation Internal Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error during division.")

# === NEW ENDPOINTS ADDED ===

@app.post("/power", response_model=OperationResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def power_route(operation: OperationRequest):
    """
    Raise the first number (a) to the power of the second number (b).
    """
    try:
        result = power(operation.a, operation.b)
        return OperationResponse(result=result)
    except ValueError as e: # Catch math domain errors (e.g., negative base to fractional power)
        logger.error(f"Power Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e: # Catch other potential errors
        logger.error(f"Power Operation Internal Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error during power calculation.")

@app.post("/modulo", response_model=OperationResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def modulo_route(operation: OperationRequest):
    """
    Calculate the remainder of a divided by b.
    """
    try:
        result = modulo(operation.a, operation.b)
        return OperationResponse(result=result)
    except ValueError as e: # Catch modulo by zero specifically
        logger.error(f"Modulo Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e: # Catch other potential errors
        logger.error(f"Modulo Operation Internal Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error during modulo calculation.")

# === END OF NEW ENDPOINTS ===

if __name__ == "__main__":
    # Ensure you have a 'templates' directory with an 'index.html' file
    # Run using: python main.py
    uvicorn.run(app, host="127.0.0.1", port=8000)