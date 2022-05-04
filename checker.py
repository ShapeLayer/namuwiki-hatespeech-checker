import kss
import ijson
import re
import multiprocessing
from transformers import TextClassificationPipeline, BertForSequenceClassification, AutoTokenizer
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from concurrent.futures import ProcessPoolExecutor

print("모델 로딩 시작")
model_name = 'sgunderscore/hatescore-korean-hate-speech'
model = BertForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
print("모델 로딩 완료")

# 프로세스 수 조정하세용
maxprocess = 2

Base = declarative_base()
engine = create_engine('sqlite:///namuhate.db')


class Namuhate(Base):
    __tablename__ = 'namuhate'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    title = Column(Text)
    sentence = Column(Text)
    none = Column(Float)
    etc = Column(Float)
    man = Column(Float)
    bad = Column(Float)
    genderminor = Column(Float)
    woman = Column(Float)
    age = Column(Float)
    nation = Column(Float)
    religion = Column(Float)
    region = Column(Float)


# 혐오발언 여부 체크
def checkHateSpeech(title, txtlist):
    #print(f"문서 {title} 대상 모델 적용, 문장 수 : {len(txtlist)}")
    output = []
    cnt = 0

    # 파이프라인 초기화
    pipe = TextClassificationPipeline(
        model=model,
        tokenizer=tokenizer,
        device=-1,  # gpu: 0, cpu: -1
        return_all_scores=True,
        function_to_apply='sigmoid')

    # 원문 데이터 저장
    for item in txtlist:
        # 모델 글자수가 300자까지인 것으로 추정되니 300자 이상 되는 물건은 체크하지 않는다.
        if (len(item) < 300):
            dat = (title, item, "")
            output.append(dat)

    # 혐오발언 체크
    for result in pipe(txtlist):
        output[cnt] = (output[cnt][0], output[cnt][1], result)
        cnt = cnt + 1
    #print(f"문서 {title} 작업 완료.")
    return output


def seperateSentence(doc):
    # 문장 분리, 텍스트를 넣으면 문장을 나눠 줌.
    txtlist = []
    #str = doc.split("\n")
    #str = [line for line in str if line.strip()]
    '''
    for line in str:
        st = kss.split_sentences(
            line, backend="none")
        txtlist = txtlist + st
    '''
    # 좀 더 빠른 성능을 위해 문장 분리 정확성을 포기
    txtlist = kss.split_sentences(doc, backend="none")
    return txtlist


def initDB():
    print("데이터베이스 초기화")
    try:
        Namuhate.__table__.create(bind=engine, checkfirst=True)
    except Exception as e:
        print("DB 작업 오류", e)
    return


def putdb(data):
    #print("DB 작업 시작")
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        for item in data:
            buf = Namuhate(title=item[0], sentence=item[1], none=item[2][0]['score'], etc=item[2][1]['score'], man=item[2][2]['score'], bad=item[2][3]['score'], genderminor=item[2][4]['score'], woman=item[2]
                           [5]['score'], age=item[2][6]['score'], nation=item[2][7]['score'], religion=item[2][8]['score'], region=item[2][9]['score'])
            session.add(buf)
            session.commit()
    except Exception as e:
        print("DB 작업 오류", e)
    return


def convertAndCheck(item):
    title = re.escape(item['title'])
    text = item['text']
    sentences = seperateSentence(text)
    output = checkHateSpeech(title, sentences)
    putdb(output)
    print(f"문서 : {title} 처리 완료.")
    return


def convertJson(fd_json):
    docs = ijson.items(fd_json, 'item')
    with ProcessPoolExecutor(max_workers=maxprocess) as pool:
        print("작업을 시작합니다.")
        pool.map(convertAndCheck, docs)


if __name__ == '__main__':
    multiprocessing.freeze_support()  # 윈도우 MP

    initDB()

    with open("namu.json", "rt", encoding='UTF8') as fd:
        convertJson(fd)
