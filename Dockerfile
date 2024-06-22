FROM python:latest

WORKDIR /double_sql
COPY . /double_sql
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
