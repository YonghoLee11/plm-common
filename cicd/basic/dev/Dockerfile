# docker image
FROM dockerhub.skhynix.com/python:3.7.4

# env directory
ENV USER_DIR=/root
ENV WORK_DIR=/app

# file copy
COPY ./pip.conf $USER_DIR/.pip/pip.conf

# file copy
COPY ./ $WORK_DIR/

# working directory
WORKDIR $WORK_DIR

# pip 설치
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install uWSGI

# Flask 템플릿을 사용하지 않는다면 리마크 처리하세요.
RUN python db.py db init \
    && python db.py db migrate \
    && python db.py db upgrade
    
# port
EXPOSE 5000
# run
# ENTRYPOINT ["uwsgi", "--socket", "0.0.0.0:5000", "--protocol=http", "-w", "wsgi"]
ENTRYPOINT ["python", "wsgi.py"]