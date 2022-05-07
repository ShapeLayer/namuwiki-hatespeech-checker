# Namumark syntax remover

## Usage
### Method 1. (Recommended) Using namuwiki-extractor and converted onmark-parser
```py
from namuparse.processing import Processing as Proc

# Returns String
Proc.processing('input string').read()
```

### Method 2. Using converted onmark-parser only
```py
from namuparse.onmark import onmarkParse as Proc

# Returns String
Proc.processing('input string').read()
```

### Example
```py
from namuparse.processing import Processing as Proc
Proc.processing(open('in.in', encoding='utf-8').read())
```

<details>
<summary>Result</summary>
<samp>
'||&lt;-2&gt;&lt;table width=500&gt;&lt;table align=right&gt;&lt;table bordercolor=#000,#ddd&gt;&lt;table bgcolor=#fff,#2d2f34&gt;&lt;colbgcolor=#000,#ddd&gt;&lt;colcolor=#fff,#2d2f34&gt; 악질 이름 생성기 ||\n||&lt;-2&gt;&lt;bgcolor=#F5F5F5,#2D2F34&gt; {{{#!wiki style="margin: -5px -10px"\n}}} ||\n||&lt;width=20%&gt; 사이트\n언어 ||&lt;colbgcolor=#fff,#2d2f34&gt;한국어 ||\n|| 회원가입 ||불가 ||\n|| 소유 ||침팬치 ||\n|| 개설 ||링크] ||\n|| 링크 ||# ||\n\n\n\n개요\n\n\n&gt; 당신만의 악질 이름을 생성하세요.\n&gt; - 사이트 설명\n\n팬치가 개발했다.\n\n역사\n링크\n\n서비스\n거주지와 이름을 넣고 생성 버튼을 누르면 이름 그대로 악질 이름을 생성해준다.\n\n특징\n녜힁제조기에서 영감을 얻었다. 단, 해당 사이트는 링크\n\n드립 자체는 엄준식 드립에서 가져온 것으로 보이나[* 여담이지만 이 악질 닉네임 형식을 최초 선보였던 인물은 자세한 정보 페이지에서는 악질 이름 드립이라는 용어를 사용하고 있다.\n\n초기에는 디시인사이드나 유튜브에서 사용되는 드립을 활용했으나, 실검에 오르며 유입이 증가함에 따라 논란이 되는 내용을 많이 제거한듯 하다.\n\n5월 14일 저녁, 개발 후기글이 올라왔다. 오는 주말(5월 16/17일) 수정을 마지막으로 악질 이름 생성기 관리에서 손을 떼겠다고 한다.\n\n기타 사항\n * 이름 란에 "엄준식"을 넣으면 엄준식 생성기로 변경된다. 이 기능은 잠깐 비활성화됐었는데, PD 아무무로부터 허락을 받고 다시 활성화되었다. 링크\n * 자세한 정보 페이지 하단에 ".xx"라는 문구가 있다. 단순 오타인 것으로 추정되었으나 해당 문구가 별도의 처리를 거친 "what-is-it-implied" 클래스로 지정되어 있는 것으로 볼 때 의도한 것 같다. 해석하면 "무엇을 암시하는 것이지" 정도.\n * 몇몇 게임에서는 작업장용 캐릭터의 아이디를 생성하는 데 쓰기도 한다. 이전에는 작업장 캐릭터는 의미없는 문자열의 조합이었으나 이런 것으로 신고를 많이 당하자 방식을 바꾼 것. 예시\n\n분류:대한민국의 웹사이트분류:웹 툴* \'녜힁\'이라는 유저닉에서 유래된 것. 온라인 게임 두 글자 닉네임이 특히 인기가 많은데, 이것 때문에 링크, 오픈사전. 바로 그 레어닉을 생성하는 사이트가 녜힁 제조기이다.* 자세한 정보 페이지 최하단의 "엄" 부분에 엄을 입력하면 정보가 나온다.* 초창기에는 배경이 바뀌었으나 재추가 이후에는 배경 변경 기능은 사라졌다. 또한 부활하지 못했다. 엄준식, 박원순 외에 트럼프도 기능이 있었던것 같지만, 현재는 빈 코드로 남아있다. '
</samp>
<p><a href="https://namu.wiki/w/악질%20이름%20생성기" target="_blank"><i>Source: 악질 이름 생성기 - 나무위키</i></a></p>
</details>
