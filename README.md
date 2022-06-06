# Wesulloc 1차 클론 코딩 프로젝트
<br>

## 개요
* 오설록(https://www.osulloc.com/kr/ko) 웹페이지 클론코딩 프로젝트
* 클론코딩은 개발 환경 셋팅부터 시작하였으며, 하단 시연 영상은 모두 백엔드와의 데이터 연동을 통해 실제 서비스에서 이용되는 수준으로 구현하였습니다.
* 프로젝트는 2주동안 진행됨에 따라 웹사이트 클론 중 필수적인 기능 구현에 집중하여 필요한 API를 개발하였습니다.
  * 회원가입 & 로그인 API
  * 상품 카테고리 API
  * 상품 리스트 API
  * 상품 상세 페이지 API 
  * 추천 상품 리스트 API
  * 장바구니 API
  * 리뷰 API

* 개발 일정에 맞춘 작업량 배분, 기능별 git 분기 및 merge의 중요성을 직접 느낄 수 있었으며, 차주에 진행되는 2차 프로젝트에서는 해당 경험을 통해 보다 부드러운 일정 진행이 이뤄질 수 있도록 하려고 합니다.

<br>

## 개발 기간 및 팀원
* 개발 기간 : 2022.05.23 ~ 2022.06.03
* 개발 인원 : 프론트엔드 4명, 백엔드 2명 
* `FE` : 이윤섭, 손가영, 김현주, 안수정 [(프론트엔드 Github Repository)](https://github.com/wecode-bootcamp-korea/33-1st-Wesulloc-frontend)
* `BE` : 황재승, 최바다 [(백엔드 Github Repository)](https://github.com/wecode-bootcamp-korea/33-1st-Wesulloc-backend)

<br>

## 사용한 기술

`Front-End` 
  * HTML, CSS(SASS), Javascript, React

`Back-End` 
  * Django, Python, MySQL, AWS(RDS, EC2), Bcrypt, JWT, django-cors

`Cowork` 
  * Git, Slack, Trello

<br>

## 시연 연상

- [Wesulloc 시연 영상](https://www.youtube.com/watch?v=hi08z17A2s0)

<br>

## API DOCUMENTATION
- [POSTMAN API DOCUMENTATION](https://documenter.getpostman.com/view/21014545/Uz5JFa5h)

<br>

## 구현 기능

### Modeling
![스크린샷 2022-06-02 오후 9 38 22](https://user-images.githubusercontent.com/75832544/172129280-bc5a0ba8-51ef-4d2e-bc4a-c9296a10a1f4.png)

<br>

### API 구현

#### < 최바다 >

> 로그인 & 회원가입 API

![](https://velog.velcdn.com/images/jhwang/post/becc6a2d-767c-46e6-bd3e-51b513e89913/image.gif)

```
- 정규표현식을 활용한 유효성 검사
- Bcrpyt를 사용하여 비밀번호 암호화
- 암호화된 비밀번호를 다시 복호화하여 일치 여부 확인
- 로그인 성공시 JWT 토큰 발급
```
> Login Decorator
```
- 인가를 필요로하는 모든 API에 적용
```

<br>

#### < 황재승 >
> Project modeling
```
- PRODUCT 테이블을 기준으로 선정하고 차례차례 전체 모델링 완성
- 중복 카테고리에 대하여 알맞은 관계 설정
```
<br>

> 상품 리스트(필터링 & 정렬)

![ezgif com-gif-maker (4)](https://user-images.githubusercontent.com/75832544/172133011-fa721d6e-c916-4427-8a15-f306d16f25fa.gif)

```
- 전체 카테고리의 상품 리스트 구현
- Q 객체 & Annotate를 활용하여 필터 기능 구현
- Pagination 기능 구현
- 연산처리 속도 개선할 수 있는 코드 작성
```
<br>

> 상품 상세 페이지

![ezgif com-gif-maker (5)](https://user-images.githubusercontent.com/75832544/172133781-c0591054-5600-4ad9-a223-831f39d4d313.gif)


```
- 상품 상세 페이지 구성에 필요한 데이터 제공
```
<br>

> 상품 검색 기능
```
- 상품 이름을 검색을 통해서 원하는 상품 데이터를 출력 가능
```
<br>

> 장바구니 API

![ezgif com-gif-maker (6)](https://user-images.githubusercontent.com/75832544/172134501-2bf1e768-bf93-437e-831b-b010d5877ad8.gif)


```

- 장바구니 상품 추가(POST), 조회(GET), 수정(PATCH), 삭제(DELETE) 기능 구현
```
<br>

> 리뷰 API

![ezgif com-gif-maker (7)](https://user-images.githubusercontent.com/75832544/172137131-2a0e7697-199f-4130-91bb-da1971dbc7b2.gif)


```
- 상품 리뷰 추가(POST), 조회(GET), 삭제(DELETE) 기능 구현
- 별점, 평균 별점, 총 리뷰 수 출력
```
<br>
<br>

## REFERENCE
- 위 프로젝트는 "오설록" 사이트를 참조하여 학습 목적으로 만들어졌습니다.
- 실무 수준의 프로젝트이지만, 학습용으로 만들어졌기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제가 될 수 있습니다.
