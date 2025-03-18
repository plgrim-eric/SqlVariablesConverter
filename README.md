# SQL Variables Converter for Sublime Text

오라클 SQL에서 바인드 변수와 Mybatis 스타일 변수 간의 변환을 쉽게 해주는 Sublime Text 플러그인입니다.

## 기능

- 오라클 바인드 변수(`:variable`)를 Mybatis 스타일(`#{variable:VARCHAR}`)로 변환
- Mybatis 스타일 변수를 오라클 바인드 변수로 변환
- 문자열 리터럴(따옴표 내부)과 주석 내용은 변환에서 제외

## 설치 방법

### Package Control 사용
1. Sublime Text에서 `Ctrl+Shift+P` (Windows/Linux) 또는 `Cmd+Shift+P` (Mac)를 눌러 명령 팔레트를 엽니다.
2. "Package Control: Install Package"를 입력하고 선택합니다.
3. "SQL Variables Converter"를 검색하고 선택합니다.

### 수동 설치
1. 이 저장소를 클론합니다.
2. Sublime Text의 Packages 디렉토리에 복사합니다.

## 사용 방법

1. SQL 파일을 열고 변환하려는 쿼리를 선택합니다.
2. 명령 팔레트(`Ctrl+Shift+P` 또는 `Cmd+Shift+P`)를 열고 다음 명령 중 하나를 실행합니다:
   - "SQL Variables Converter: Oracle to Mybatis" - 오라클 바인드 변수를 Mybatis 형식으로 변환
   - "SQL Variables Converter: Mybatis to Oracle" - Mybatis 형식을 오라클 바인드 변수로 변환

## 라이선스

MIT
