FROM python:3.11-slim

EXPOSE $PORT

WORKDIR /app

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc git && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY src/danish_to_english_llm/front_api.py src/danish_to_english_llm/front_api.py
COPY requirements_frontend.txt requirements_frontend.txt

#RUN pip3 install -r requirements_frontend.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements_frontend.txt

ENTRYPOINT ["streamlit", "run", "src/danish_to_english_llm/front_api.py", "--server.port", "8080", "--server.address=0.0.0.0"]
