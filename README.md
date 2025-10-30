# JPG 변환기

[![Release](https://img.shields.io/github/v/release/kai6388/jpg_converter)](https://github.com/kai6388/jpg_converter/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/kai6388/jpg_converter/total)](https://github.com/kai6388/jpg_converter/releases)
[![License](https://img.shields.io/github/license/kai6388/jpg_converter)](LICENSE)

Windows 환경에서 동작하는 이미지 JPG 변환 프로그램입니다.

## ✨ 주요 기능

- 🎯 **드래그 앤 드롭 지원** - 이미지를 창에 드래그하여 간편하게 추가
- ⚙️ **JPG 퀄리티 조절** - 80~100 사이에서 원하는 퀄리티 선택
- 🖼️ **다양한 형식 지원** - PNG, BMP, GIF, TIFF, WebP 등
- 📁 **일괄 변환** - 개별 파일 또는 폴더 전체 선택
- 📊 **실시간 진행률** - 변환 과정을 시각적으로 확인
- 🎨 **투명 배경 처리** - 투명도가 있는 이미지를 자동으로 흰색 배경으로 변환
- 📂 **출력 위치 선택** - 같은 위치 또는 원하는 폴더에 저장

## 📥 설치 방법

### 방법 1: EXE 파일 다운로드 (권장)

Python 설치 없이 바로 사용 가능합니다!

1. [최신 릴리스](https://github.com/kai6388/jpg_converter/releases/latest)에서 `JPG변환기.exe` 다운로드
2. 다운로드한 파일 실행

### 방법 2: Python으로 실행

Python 3.8 이상 필요

```bash
# 저장소 클론
git clone https://github.com/kai6388/jpg_converter.git
cd jpg_converter

# 의존성 설치
pip install -r requirements.txt

# 실행
python main.py
```

## 🚀 사용 방법

### 1️⃣ 이미지 추가

다음 세 가지 방법 중 선택:
- **드래그 앤 드롭**: 이미지 파일이나 폴더를 프로그램 창의 목록 영역에 드래그
- **이미지 추가 버튼**: 개별 파일 선택
- **폴더 추가 버튼**: 폴더 내 모든 이미지 일괄 추가

### 2️⃣ JPG 퀄리티 설정

슬라이더로 원하는 퀄리티 선택 (80~100):
- **80-85**: 웹 업로드용 (작은 용량)
- **90-95**: 일반 사용 (권장, 기본값)
- **96-100**: 인쇄/보관용 (최고 화질)

### 3️⃣ 출력 위치 설정

- **"같은 위치에 저장" 체크**: 원본 이미지와 같은 폴더에 저장
- **체크 해제**: "선택..." 버튼으로 원하는 출력 폴더 지정

### 4️⃣ 변환 실행

"JPG로 변환" 버튼 클릭 → 진행률 확인 → 완료!

## 📋 지원 형식

### 입력 형식
PNG, BMP, GIF, TIFF, TIF, WebP, JPG, JPEG, ICO, PPM, PGM, PBM, PNM, DIB

### 출력 형식
JPG (JPEG, 사용자 지정 퀄리티, optimize=True)

## 💡 사용 팁

- **대량 변환**: 폴더를 드래그하면 폴더 내 모든 이미지가 자동으로 추가됩니다
- **퀄리티 vs 용량**: 퀄리티가 높을수록 파일 크기가 커집니다
- **투명 배경**: PNG 등 투명도가 있는 이미지는 흰색 배경으로 자동 변환됩니다
- **중복 방지**: 이미 추가된 이미지는 자동으로 제외됩니다

## ⚠️ 주의사항

- 투명도가 있는 이미지(RGBA, PNG 등)는 흰색 배경으로 변환됩니다
- 같은 이름의 파일이 존재하면 덮어씁니다
- 변환 중에는 프로그램을 종료하지 마세요

## 🛠️ 개발 환경

- **언어**: Python 3.12
- **GUI 프레임워크**: tkinter, tkinterdnd2
- **이미지 처리**: Pillow (PIL)
- **빌드 도구**: PyInstaller

## 📦 의존성

```
Pillow>=10.0.0
tkinterdnd2>=0.4.0
```

## 🔧 빌드 방법

EXE 파일 생성:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "JPG변환기" --clean main.py
```

생성된 파일: `dist/JPG변환기.exe`

## 📝 변경 이력

### v1.0.1 (2024-10-30)
- ✨ 드래그 앤 드롭 기능 추가
- ✨ JPG 퀄리티 조절 슬라이더 추가 (80~100)
- 🎨 UI 개선 (창 크기 600x650)
- 🐛 버튼 레이아웃 최적화

### v1.0.0 (2024-10-30)
- 🎉 초기 릴리스
- 기본 이미지 변환 기능
- 다양한 형식 지원
- 일괄 변환 지원

전체 변경 이력은 [Releases](https://github.com/kai6388/jpg_converter/releases)를 참조하세요.

## 💻 시스템 요구사항

- **운영체제**: Windows 10/11
- **디스크 공간**: 32MB 이상

## 📄 라이선스

MIT License

## 🤝 기여

버그 리포트나 기능 제안은 [Issues](https://github.com/kai6388/jpg_converter/issues)에 등록해주세요.

## 👨‍💻 개발자

kai6388

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
