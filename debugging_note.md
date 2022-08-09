# 디버깅 기록 노트

### Pandas DataFrame 저장 시 퍼포먼스 경고

PerformanceWarning: 
your performance may suffer as PyTables will pickle object types that it cannot
map directly to c-types

수정

| type    | info                                                                                                                                                 |
| :------ | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| bool    | Boolean (true/false) types. Supported precisions: 8 (default) bits.                                                                                  |
| int     | Signed integer types. Supported precisions: 8, 16, 32 (default) and 64 bits.                                                                         |
| uint    | Unsigned integer types. Supported precisions: 8, 16, 32 (default) and 64 bits.                                                                       |
| float   | Floating point types. Supported precisions: 16, 32, 64 (default) bits and extended precision floating point (see note on floating point types).      |
| complex | Complex number types. Supported precisions: 64 (32+32), 128 (64+64, default) bits and extended precision complex (see note on floating point types). |
| string  | Raw string types. Supported precisions: 8-bit positive multiples.                                                                                    |
| time    | Data/time types. Supported precisions: 32 and 64 (default) bits.                                                                                     |
| enum    | Enumerated types. Precision depends on base type.                                                                                                    |

위 목록은 PyTables에서 지원하는 자료형이다. Pandas에서는 PyTables를 이용하여 빠르게 c-style type과 매핑하고 hdf5로 저장할 수 있지만 위 자료형이 아닌 원소가 존재하면 PyTables를 활용할 수 없어 속도가 느려진다는 경고이다.

to_hdf를 호출했을 때 한 행의 type에 여러 타입이 섞여있으면 위와 같은 경고가 출력된다.

int와 float가 함께 쓰이면 float로 형변환된다.

string은 object형으로 저장된다. pd.StringDType으로 형변환할 수 있지만 hdf가 지원하지 않는 형식이다.

np.NaN은 float이다.

pd.NA는 int형으로, np.NaN과는 달리 dtype을 int형으로 유지하면서 결측치를 나타낼 수 있다. 다만 hdf가 지원하지 않는 형식으로 바뀐다.

feather는 확장자가 .ft인데, 여러 타입이 섞여있어도 퍼포먼스 경고가 나오지 않고 pd.NA를 저장할 수 있다.

feather가 퍼포먼스 면에서는 좋아보이지만 hdf의 계층적 저장 구조도 좋아서 hdf를 다음에도 사용할 것 같다.

### 원소가 숨겨지면 텍스트를 크롤링할 수 없음

html의 inline CSS로 display: none 속성이 들어가면 웹페이지 상에 보이지 않게 되는데 DOM에는 존재하지만 크롤링도 못한다.

### xpath 인덱싱

practice_xpath.py, .html을 참고하자.

0부터 시작하지 않고 1부터 시작한다.

### html, head, body태그 자동 생성

모든 웹페이지에는 html태그로 시작하여 그 안에 head, body태그로 나뉜다.

내가 만든 html파일에 html, head, body태그가 없으면 웹 브라우저에서 실행시킬 때 자동으로 태그를 달아준다.

보통 head에는 title이나 meta태그가, body에는 컨텐츠가 들어가는데 자동으로 태그가 생길 땐 이를 어느정도 반영해준다.

여러 번 실험한 결과 몇 가지 규칙이 있는 듯한데 모든 태그를 체계적으로 실험하지 않아 부정확하고, 자세히 알 필요도 없을 것 같다.

1. html태그가 없으면 항상 전체를 html태그로 감싸주는 것 같다.
2. head, body태그가 없으면 앞에서부터 head에 들어갈 원소를 다 head에 넣어주고 나머지는 body에 넣어준다.
   1. head에 들어가야할 title같은 태그가 가장 앞에 나온다면 head에 들어가게 된다.
   2. 하지만 title이 컨텐츠 중간에 나온다면 body에 들어가게 된다.
3. head태그가 없고 body태그가 있으면 body태그 앞에 head태그를 넣어준다.
   1. 이때 body태그 안에 title태그가 있으면 title태그가 가장 앞에 있더라도, body에서 빼서 head로 넣어주지는 않는다.
4. head태그가 있고 body태그가 없으면 head태그 뒤에 body태그를 넣어준다.
   1. 이때 head태그 안에 컨텐츠가 있으면 앞에서부터 head에 남아있어야 할 원소를 남겨두고 나머지는 head에서 빼서 body로 넣어준다.
   2. 만약 컨텐츠 가장 앞이 아닌 곳에 title태그가 있으면 title은 head에 남아있어야 하지만 컨텐츠와 함께 body로 들어가진다.
5. tr태그는 inline CSS가 적용되지 않는다.
6. tr태그는 내부의 텍스트를 밖으로 빼고 tr태그가 삭제된다.
7. tr태그가 여러 개 연속되어있을 땐 내부의 텍스트가 한 줄의 문자열로 합쳐진다.
8. body로 들어간 title도 정상적으로 작동한다.

규칙이 복잡하니 head에 들어갈 것과 body에 들어갈 것을 순서에 맞춰 적고, html, head, body가 적절히 생성된다고 생각해야겠다.

### 꼭 wait를 사용해야하는 이유

practice_explicit_wait.py, .html 참고하자.

웹페이지를 불러올 때 가벼운 html을 통해 빠르게 화면을 대략적으로 구성한 뒤 무거운 자바스크립트를 통해 뒤늦게 후보정한다.

때문에 크롤링하고 싶은 정보가 자바스크립트까지 다 받은 뒤의 정보여야 할 땐 크롤링을 적절히 기다려줘야 한다.

driver의 options로 page load stretgy를 통해 html까지 다 받아졌을 때까지 기다리도록 할 수는 있으나 자바스크립트의 경우는 복잡하기 때문에 직접 얼마나 기다릴지 설정해줘야한다.

myhtml0.html은 텍스트 원소 하나만 있는 페이지이다. 이 텍스트는 자바스크립트를 통해 페이지가 켜진 1초, 2초, 3초 뒤에 텍스트가 바뀌도록 만들었다.

wait_practice를 실행하면 가장 처음 텍스트가 나온다. 하지만 적절히 explicit wait를 하면 3초 뒤의 텍스트를 얻을 수 있다.

### 원소를 찾을 수 없는 오류

practice_classname_search.py, .html 참고하자.

원소를 By.CLASS_NAME이나 By.CSS_SELECTOR로 클래스명으로 찾을 때 클래스 명에 공백 문자가 있을 경우 항상 그러한 원소를 찾을 수 없다는 오류가 발생한다.

By.XPATH로 검색하면 클래스 명에 공백 문자가 있어도 원소를 찾을 수 있다.

주석처리한 부분을 실행하면 오류가 난다.

내가 크롤링하려는 사이트의 클래스 명에 공백 문자가 있을 수 있으므로 항상 xpath를 사용해야겠다.