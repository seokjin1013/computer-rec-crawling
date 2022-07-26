# 크롤링 데이터셋

pandas dataframe으로 저장한다.

### id (고유키) - str

다나와 웹사이트 제품 id의 숫자 부분

다나와 제품 id는 항상 productItem으로 시작하고 일련번호로 끝난다.

예를 들어 productItem15594638

여기서 15594638를 크롤링 데이터셋의 고유키로 사용한다.

### id_validator - bool

id가 유효한 지를 나타낸다. True이면 정상, False이 아니면 비정상

다나와 제품 id가 productItem으로 시작하지 않거나 숫자로 끝나지 않거나 등등의 경우이다.

id_validator의 값이 True가 아닐 경우 숫자만 파싱하지 않고 그대로 고유키로 넣는다.

### price - dictionary

매장명과 그 매장에서의 제품 가격이 쌍으로 매핑된 형태

### spec - dictionary

다나와 사이트 기준 스펙 정보. 문자열과 문자열이 쌍으로 매핑된 형태

### review

다나와 리뷰 공감 많은 순으로 5개

