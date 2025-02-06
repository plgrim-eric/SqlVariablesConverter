# SqlVariablesConverter

SQL 변수 형식을 Mybatis와 일반 SQL 형식 간에 상호 변환해주는 Sublime Text 플러그인입니다.

## 기능

이 플러그인은 두 가지 변환 기능을 제공합니다:

1. SQL -> Mybatis 변환
   - `:변수명` 형식을 `#{변수명:VARCHAR}` 형식으로 변환
   - 이미 Mybatis 형식이 있는 경우 변환하지 않음
   - 상단의 변수 선언부는 유지

2. Mybatis -> SQL 변환
   - `#{변수명:VARCHAR}` 형식을 `:변수명` 형식으로 변환
   - SQL에서 사용되는 변수들을 자동으로 수집하여 상단에 변수 선언부 생성
   - 변수 선언 형식: `:변수명 = NULL`

## 사용법

1. 커맨드 팔레트 열기 (Windows/Linux: `Ctrl+Shift+P`, Mac: `Cmd+Shift+P`)
2. 다음 명령어 중 하나 선택:
   - `SQL Variables: Convert to Mybatis`
   - `SQL Variables: Convert to SQL`

## 설치

1. Sublime Text의 Packages 디렉토리 열기
   - Windows: `Sublime Text 설치폴더\Data\Packages`
2. 이 저장소를 `SqlVariablesConverter` 폴더로 클론하거나 다운로드

## Package Control 사용 시

   - 패키지 컨트롤에서 폴더를 강제로 지울수 있음.
   - Preferences -> Package Settings -> Package Control -> Settings - User 에 아래 내용 추가 "installed_packages": [ // 기존 패키지 목록 ... "SqlVariablesConverter" ],
