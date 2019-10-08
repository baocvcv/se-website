#first stage, build the frontend
FROM node:10.16.1

RUN npm config set registry https://registry.npm.taobao.org

ENV FRONTEND=/opt/frontend

WORKDIR $FRONTEND

COPY frontend/package.json $FRONTEND

RUN npm install

COPY frontend/ $FRONTEND

RUN npm run build

#second stage for the backend

FROM python:3.7.4

ENV HOME=/opt/app

WORKDIR $HOME

COPY requirements.txt $HOME

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . $HOME

#Copy frontend from the first stage
COPY --from=0 /opt/frontend/dist frontend/dist

EXPOSE 80

ENV PYTHONUNBUFFERED=true

CMD ["/bin/sh", "config/run.sh"]
