FROM python:3.10
WORKDIR /code
COPY . .
RUN pip install pyTelegramBotAPI openpyxl fuzzywuzzy Flask python-Levenshtein
CMD ["python", "app.py"]