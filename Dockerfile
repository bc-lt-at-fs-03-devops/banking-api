# stage1 - run unit test
FROM python:3.11.2-slim-buster AS build
WORKDIR /app
COPY requirements_api.txt .
RUN pip install -r requirements_api.txt
COPY . .
CMD ["coverage", "run", "-m", "pytest"]

# Stage 2 - run the API
FROM python:3.11.2-slim-buster
WORKDIR /app
COPY --from=build /app/requirements_api.txt .
RUN pip install -r requirements_api.txt
COPY --from=build /app .
EXPOSE 9000
CMD [ "python", "bank_api/api.py"]
