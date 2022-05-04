# Namuwiki-hatespeech-checker
나무위키 덤프를 읽어와서 혐오발언인지 체크하고 DB에 넣는 스크립트

## 사용법
폴더 안에 namu.json으로 나무위키의 덤프파일을 집어넣으세요.
구조는 일단 최신 덤프와 맞춰 놓음

## 설정할 만한 것
maxprocess : 총 프로세스 수, 너무 많으면 out of memory 걸림.
cuda 가능하면 TextClassificationPipeline의 device를 수정하시오.

## 의존성
transformers, sqlalchemy, ijson, kss

## 사용 모델
https://github.com/sgunderscore/hatescore-korean-hate-speech/

## TODO
1. 태그 스트립
2. 좀 더 분석하기 편한 형태로 넣기