# 🧮 FastAPI Calculator Application

This is a simple web application that performs basic calculator operations, built using the FastAPI framework in Python.

The project is set up with automated unit and integration testing using `pytest` and includes a CI/CD workflow with GitHub Actions to automatically run tests on every push.

## ✨ Features

* **FastAPI Backend:** A high-performance, easy-to-use API.
* **Unit & Integration Tests:** Comprehensive testing using `pytest` and FastAPI's `TestClient`.
* **Automated CI:** A GitHub Actions workflow (`.github/workflows/ci.yml`) automatically runs all tests.
* **Live Server:** Uses `uvicorn` as the ASGI server.

## 💻 Technologies Used

* **[FastAPI](https://fastapi.tiangolo.com/):** The web framework for building the API.
* **[Uvicorn](https://www.uvicorn.org/):** The ASGI server to run the application.
* **[Pytest](https://docs.pytest.org/):** The framework for writing and running unit and integration tests.
* **[GitHub Actions](https://github.com/features/actions):** The CI/CD platform for automating the test workflow.

---

## 🚀 Getting Started

### 1. Prerequisites

* Python 3.8+
* `pip` (Python package installer)

### 2. Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
    cd YOUR_REPOSITORY_NAME
    ```

2.  **Create and activate a virtual environment:**
    * **macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(**Note:** Make sure you have a `requirements.txt` file with at least `fastapi`, `uvicorn`, and `pytest` listed.)*

### 3. Running the Application

To run the application locally, use `uvicorn`:

```bash
uvicorn main:app --reload