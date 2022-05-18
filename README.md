# Quick start

## DWP 에서 Python (Backend) 서비스 생성

- DWP 내 서비스 생성 절차 참조

## DWP 서비스 소스 내려받기

- DWP 서비스로 생성한 SCM 에서 소스를 Local PC 로 내려받습니다.

## Local PC에 Python 환경 설정

- Local PC 에 Python 3.x 을 설치
  - Python 설치는 일반적인 사항으로 별도로 설명하지 않습니다.
- Local PC 에 IDE 인 VS Code 설치
  - VS Code 설치는 일반적인 사항으로 별도로 설명하지 않습니다.
- Python 라이브러리 설치를 위해 Repository 설정
  - Local PC 아래 경로에 pip.ini 파일을 만들고 파일내용을 작성합니다.
  - C:\Users\Administrator\AppData\Roaming\pip\pip.ini

    ```shell
    [global]
    trusted-host=nexus.skhynix.com
    index-url=http://nexus.skhynix.com/repository/pypi-group/simple
    ```

  - 또는 Source Template 폴더에 있는 pip.int 파일을 사용해도 됩니다.

    ```shell
    copy ${project_root}\pip.ini C:\Users\Administrator\AppData\Roaming\pip\pip.ini
    ```

## Local PC 에 가상환경 설정

- Local PC 에서 가상환경 라이브러리 설치 및 생성

  ```shell
  project_root$ pip install virtualenv
  project_root$ virtualenv venv
  ```

- Local PC 에서 가상환경 실행

  ```shell
  project_root$ venv\Scripts\activate.bat  # for windows
  project_root$ source venv/bin/activate # for linux
  ```

- Python 라이브러리 설치

  ```shell
  (venv) project_root$ pip install -r requirements.txt
  ```

## 테스트용 DB 생성

- 아래 명령어를 수행하여 테스트용 DB를 생성합니다.

  ```shell
  (venv) project_root$ python db.py db init
  (venv) project_root$ python db.py db migrate
  (venv) project_root$ python db.py db upgrade
  ```

## Local PC 에서 실행

- local 에서 실행할때는 아래와 같이 실행합니다.
  - debug = True 로 실행되므로 Debug Mode : on 됩니다.

    ```shell
    (venv) project_root$ python run.py
    ```

- server 에서 실행할때는 uwsgi 를 사용하여 실행됩니다.
  - uwsgi 는 windows 환경에서는 실행할 수 없습니다.
  - Dockerfile 에 아래와 같이 설정되어 있습니다.
  - uwsgi 는 flask 를 production 모드로 실행되도록 해줍니다.
  - Debug Mode : off 로 설정됩니다.

    ```shell
    (venv) project_root$ uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi
    ```

## Local PC 에서 실행 확인

- local 에서는 아래와 같이 접속합니다.
  - [swagger-ui](http://localhost:5000/plm-python-common/swagger-ui/)
  - [swagger.json](http://localhost:5000/plm-python-common/swagger.json)

## 개발에 필요한 라이브러리를 추가 설치가 필요한 경우

- 아래 명령어로 라이브러리를 설치합니다.

  ```shell
  (venv) project_root$ pip install packagename
  ```

- pip install 이 실패하는 경우 아래 Nexus 로 들어가서 필요한 라이브러리가 있는지 검색합니다.
- http://nexus.skhynix.com:8081/ 에 필요한 라이브러리가 없는 경우 전사 nexus 에 등록 요청을 해야 합니다.

  ```shell
  http://nexus.skhynix.com:8081/
  ```

## 배포전 확인 사항

- 개발이 완료되서 배포를 하기전에 설치 라이브러리 목록을 갱신하기 위해 아래 명령어를 실행해 줍니다.
- 설치 라이브러리 목록을 갱신해주지 않으면 Docker 에서 실행시 라이브러리 참조 오류가 발생합니다.

  ```shell
  (venv) project_root$ pip freeze > requirements.txt
  ```

## Cloud 배포

- DWP 내 CI/CD 화면을 통해 Dev/Prd 로 배포합니다.
- CI/CD 배포 절차는 별도 참고

## Cloud 에서 실행 확인

- DEV Cloud 에 배포된 서비스 확인은 아래 URL로 접속합니다.
  - [swagger-ui](http://plm-python-common-basic-dev.api.hcpnd01.skhynix.com/plm-python-common/swagger-ui/)
  - [swagger.json](http://plm-python-common-basic-dev.api.hcpnd01.skhynix.com/plm-python-common/swagger.json)
- PRD Cloud 에 배포된 서비스 확인은 아래 URL로 접속합니다.
  - [swagger-ui](http://plm-python-common-basic-prd.api.hcpp01.skhynix.com/plm-python-common/swagger-ui/)
  - [swagger.json](http://plm-python-common-basic-prd.api.hcpp01.skhynix.com/plm-python-common/swagger.json)
  
