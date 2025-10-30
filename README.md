# 이미지를 JPG로 변환

Windows 환경에서 동작하는 이미지 JPG 변환 프로그램입니다.

## 기능

- 개별 이미지 파일 선택 또는 폴더 전체 선택
- 선택된 이미지 목록 관리 (추가/제거)
- 출력 위치 설정 (같은 위치 또는 지정 폴더)
- 실시간 진행률 표시
- PNG, BMP, GIF, TIFF, WebP 등 다양한 형식 지원

## 설치 방법

1. Python 3.8 이상 설치 필요
2. 의존성 설치:
```bash
pip install -r requirements.txt
```

## 사용 방법

1. 프로그램 실행:
```bash
python main.py
```

2. "이미지 추가" 버튼으로 개별 파일 선택 또는 "폴더 추가"로 폴더 전체 선택
3. 출력 위치 설정:
   - "같은 위치에 저장" 체크: 원본 이미지와 같은 폴더에 저장
   - 체크 해제: 원하는 출력 폴더 선택
4. "JPG로 변환" 버튼 클릭
5. 진행률 확인 후 완료 메시지 확인

## 지원 형식

입력: PNG, BMP, GIF, TIFF, TIF, WebP, JPG, JPEG, ICO, PPM, PGM, PBM, PNM, DIB
출력: JPG (JPEG quality=95, optimize=True)

## 주의사항

- 투명도가 있는 이미지(RGBA, PNG 등)는 흰색 배경으로 변환됩니다
- 같은 이름의 파일이 존재하면 덮어씁니다
- 변환 중에는 프로그램을 종료하지 마세요

## 라이선스

MIT License
