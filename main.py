"""
이미지를 JPG로 변환하는 GUI 프로그램
Windows 환경에서 동작하도록 설계됨
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image
import os
import threading
from typing import List, Tuple


class ImageConverterApp:
    """이미지를 JPG로 변환하는 GUI 애플리케이션"""

    def __init__(self, root: TkinterDnD.Tk):
        """GUI 초기화 및 설정"""
        self.root = root
        self.root.title("JPG 변환기")
        self.root.geometry("600x650")
        self.root.resizable(False, False)

        # 상태 변수 초기화
        self.image_paths: List[str] = []
        self.same_location_var = tk.BooleanVar(value=False)
        self.output_folder = tk.StringVar()
        self.quality_var = tk.IntVar(value=95)
        self.is_converting = False

        # 지원 이미지 형식
        self.SUPPORTED_FORMATS = ('.png', '.bmp', '.gif', '.tiff', '.tif',
                                  '.webp', '.jpg', '.jpeg', '.ico', '.ppm',
                                  '.pgm', '.pbm', '.pnm', '.dib')

        # GUI 위젯 생성
        self.create_widgets()

    def create_widgets(self):
        """모든 GUI 위젯 생성 및 배치"""

        # ==================== 상단: 이미지 선택 버튼 ====================
        top_frame = tk.Frame(self.root, pady=10)
        top_frame.pack(fill=tk.X, padx=10)

        btn_add_images = tk.Button(
            top_frame,
            text="이미지 추가",
            command=self.add_images,
            width=15,
            height=2
        )
        btn_add_images.pack(side=tk.LEFT, padx=5)

        btn_add_folder = tk.Button(
            top_frame,
            text="폴더 추가",
            command=self.add_folder,
            width=15,
            height=2
        )
        btn_add_folder.pack(side=tk.LEFT, padx=5)

        # ==================== 중단: 이미지 목록 ====================
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        list_label = tk.Label(list_frame, text="선택된 이미지 (드래그 앤 드롭으로 추가 가능):", anchor=tk.W)
        list_label.pack(fill=tk.X)

        # Listbox + Scrollbar
        list_container = tk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True, pady=5)

        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            list_container,
            yscrollcommand=scrollbar.set,
            selectmode=tk.EXTENDED,
            height=12
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)

        # 드래그 앤 드롭 설정
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.on_drop)

        # 목록에서 제거 버튼
        btn_remove = tk.Button(
            list_frame,
            text="선택 항목 제거",
            command=self.remove_selected_images,
            width=15
        )
        btn_remove.pack(pady=5)

        # ==================== 중하단: 출력 설정 ====================
        output_frame = tk.Frame(self.root)
        output_frame.pack(fill=tk.X, padx=10, pady=10)

        self.check_same_location = tk.Checkbutton(
            output_frame,
            text="같은 위치에 저장",
            variable=self.same_location_var,
            command=self.toggle_output_path
        )
        self.check_same_location.pack(anchor=tk.W)

        path_frame = tk.Frame(output_frame)
        path_frame.pack(fill=tk.X, pady=5)

        path_label = tk.Label(path_frame, text="출력 폴더:", width=10, anchor=tk.W)
        path_label.pack(side=tk.LEFT)

        self.entry_output = tk.Entry(
            path_frame,
            textvariable=self.output_folder,
            state=tk.NORMAL
        )
        self.entry_output.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.btn_select_output = tk.Button(
            path_frame,
            text="선택...",
            command=self.select_output_folder,
            width=10
        )
        self.btn_select_output.pack(side=tk.LEFT)

        # 퀄리티 설정
        quality_frame = tk.Frame(output_frame)
        quality_frame.pack(fill=tk.X, pady=5)

        quality_label = tk.Label(quality_frame, text="JPG 퀄리티:", width=10, anchor=tk.W)
        quality_label.pack(side=tk.LEFT)

        self.quality_scale = tk.Scale(
            quality_frame,
            from_=80,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.quality_var,
            length=200
        )
        self.quality_scale.pack(side=tk.LEFT, padx=5)

        self.quality_value_label = tk.Label(
            quality_frame,
            text="95",
            width=5,
            anchor=tk.W
        )
        self.quality_value_label.pack(side=tk.LEFT)

        # 퀄리티 값 변경 시 레이블 업데이트
        self.quality_var.trace_add('write', self.update_quality_label)

        # ==================== 진행률 표시 ====================
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(fill=tk.X, padx=10, pady=10)

        progress_label = tk.Label(progress_frame, text="진행률:")
        progress_label.pack(anchor=tk.W)

        self.progress = ttk.Progressbar(
            progress_frame,
            orient=tk.HORIZONTAL,
            length=100,
            mode='determinate'
        )
        self.progress.pack(fill=tk.X, pady=5)

        self.progress_text = tk.Label(
            progress_frame,
            text="0 / 0 (0%)",
            anchor=tk.W
        )
        self.progress_text.pack(anchor=tk.W)

        # ==================== 변환 실행 버튼 ====================
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.btn_convert = tk.Button(
            button_frame,
            text="JPG로 변환",
            command=self.convert_images,
            width=15,
            height=2
        )
        self.btn_convert.pack()

    def add_images(self):
        """개별 이미지 파일 선택"""
        filetypes = [
            ("이미지 파일", " ".join(f"*{ext}" for ext in self.SUPPORTED_FORMATS)),
            ("모든 파일", "*.*")
        ]

        files = filedialog.askopenfilenames(
            title="이미지 선택",
            filetypes=filetypes
        )

        if files:
            added_count = 0
            for file in files:
                if file not in self.image_paths:
                    self.image_paths.append(file)
                    self.listbox.insert(tk.END, os.path.basename(file))
                    added_count += 1

            if added_count > 0:
                messagebox.showinfo("완료", f"{added_count}개의 이미지가 추가되었습니다.")

    def add_folder(self):
        """폴더 선택하여 이미지 일괄 추가"""
        folder = filedialog.askdirectory(title="폴더 선택")

        if folder:
            added_count = 0
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    _, ext = os.path.splitext(filename)
                    if ext.lower() in self.SUPPORTED_FORMATS:
                        if file_path not in self.image_paths:
                            self.image_paths.append(file_path)
                            self.listbox.insert(tk.END, filename)
                            added_count += 1

            if added_count > 0:
                messagebox.showinfo("완료", f"{added_count}개의 이미지가 추가되었습니다.")
            else:
                messagebox.showwarning("경고", "지원하는 이미지 파일을 찾을 수 없습니다.")

    def remove_selected_images(self):
        """선택된 이미지를 목록에서 제거"""
        selected_indices = self.listbox.curselection()

        if not selected_indices:
            messagebox.showwarning("경고", "제거할 항목을 선택해주세요.")
            return

        # 역순으로 제거 (인덱스 변경 방지)
        for index in reversed(selected_indices):
            self.listbox.delete(index)
            self.image_paths.pop(index)

        messagebox.showinfo("완료", f"{len(selected_indices)}개 항목이 제거되었습니다.")

    def on_drop(self, event):
        """드래그 앤 드롭 이벤트 핸들러"""
        # 드롭된 파일 경로들을 파싱
        files = self.root.tk.splitlist(event.data)

        added_count = 0
        for file_path in files:
            # 경로에서 중괄호 제거 (Windows 경로 포맷)
            file_path = file_path.strip('{}')

            if os.path.isfile(file_path):
                # 파일인 경우: 이미지 형식 확인
                _, ext = os.path.splitext(file_path)
                if ext.lower() in self.SUPPORTED_FORMATS:
                    if file_path not in self.image_paths:
                        self.image_paths.append(file_path)
                        self.listbox.insert(tk.END, os.path.basename(file_path))
                        added_count += 1

            elif os.path.isdir(file_path):
                # 폴더인 경우: 폴더 내 모든 이미지 추가
                for filename in os.listdir(file_path):
                    full_path = os.path.join(file_path, filename)
                    if os.path.isfile(full_path):
                        _, ext = os.path.splitext(filename)
                        if ext.lower() in self.SUPPORTED_FORMATS:
                            if full_path not in self.image_paths:
                                self.image_paths.append(full_path)
                                self.listbox.insert(tk.END, filename)
                                added_count += 1

        if added_count > 0:
            messagebox.showinfo("완료", f"{added_count}개의 이미지가 추가되었습니다.")
        else:
            messagebox.showwarning("경고", "지원하는 이미지 파일을 찾을 수 없습니다.")

    def toggle_output_path(self):
        """'같은 위치에 저장' 체크박스 토글"""
        if self.same_location_var.get():
            self.entry_output.config(state=tk.DISABLED)
            self.btn_select_output.config(state=tk.DISABLED)
        else:
            self.entry_output.config(state=tk.NORMAL)
            self.btn_select_output.config(state=tk.NORMAL)

    def select_output_folder(self):
        """출력 폴더 선택"""
        folder = filedialog.askdirectory(title="출력 폴더 선택")
        if folder:
            self.output_folder.set(folder)

    def update_quality_label(self, *args):
        """퀄리티 값 레이블 업데이트"""
        self.quality_value_label.config(text=str(self.quality_var.get()))

    def validate_images(self) -> bool:
        """변환 전 검증"""
        if not self.image_paths:
            messagebox.showerror("오류", "변환할 이미지를 선택해주세요.")
            return False

        if not self.same_location_var.get():
            if not self.output_folder.get():
                messagebox.showerror("오류", "출력 폴더를 선택하거나\n'같은 위치에 저장'을 체크해주세요.")
                return False

            if not os.path.exists(self.output_folder.get()):
                messagebox.showerror("오류", "선택한 출력 폴더가 존재하지 않습니다.")
                return False

        return True

    def convert_images(self):
        """변환 시작"""
        if self.is_converting:
            messagebox.showwarning("경고", "이미 변환이 진행 중입니다.")
            return

        if not self.validate_images():
            return

        # 버튼 비활성화
        self.is_converting = True
        self.btn_convert.config(state=tk.DISABLED)

        # 진행률 초기화
        self.progress['value'] = 0
        self.progress_text.config(text="0 / 0 (0%)")

        # 별도 스레드에서 변환 실행
        thread = threading.Thread(target=self._convert_thread, daemon=True)
        thread.start()

    def _convert_thread(self):
        """백그라운드 스레드에서 실제 변환 수행"""
        total = len(self.image_paths)
        success_count = 0
        failed_files: List[Tuple[str, str]] = []

        for index, input_path in enumerate(self.image_paths, 1):
            try:
                output_path = self.get_output_path(input_path)

                # 파일 덮어쓰기 확인 (같은 파일명이면 스킵)
                if os.path.exists(output_path) and output_path == input_path:
                    # JPG를 JPG로 변환하는 경우, 임시 파일로 저장 후 교체
                    temp_output = output_path + ".temp.jpg"
                    self._convert_single_image(input_path, temp_output)
                    os.replace(temp_output, output_path)
                else:
                    self._convert_single_image(input_path, output_path)

                success_count += 1

            except Exception as e:
                failed_files.append((os.path.basename(input_path), str(e)))

            # 진행률 업데이트
            self.update_progress(index, total)

        # 변환 완료
        self.conversion_complete(success_count, total, failed_files)

    def _convert_single_image(self, input_path: str, output_path: str):
        """단일 이미지 변환"""
        quality = self.quality_var.get()

        with Image.open(input_path) as img:
            # RGBA, LA, P 모드는 RGB로 변환 (흰 배경)
            if img.mode in ('RGBA', 'LA', 'P'):
                # 흰 배경 생성
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))

                # 알파 채널이 있으면 마스크로 사용
                if img.mode == 'RGBA':
                    rgb_img.paste(img, mask=img.split()[3])
                elif img.mode == 'LA':
                    rgb_img.paste(img.convert('L'), mask=img.split()[1])
                elif img.mode == 'P':
                    # 팔레트 모드는 RGB로 변환 후 붙여넣기
                    if 'transparency' in img.info:
                        img = img.convert('RGBA')
                        rgb_img.paste(img, mask=img.split()[3])
                    else:
                        rgb_img.paste(img.convert('RGB'))

                rgb_img.save(output_path, 'JPEG', quality=quality, optimize=True)
            else:
                # 다른 모드는 RGB로 변환하여 저장
                img.convert('RGB').save(output_path, 'JPEG', quality=quality, optimize=True)

    def get_output_path(self, input_path: str) -> str:
        """출력 경로 결정"""
        filename = os.path.splitext(os.path.basename(input_path))[0]

        if self.same_location_var.get():
            output_dir = os.path.dirname(input_path)
        else:
            output_dir = self.output_folder.get()

        return os.path.join(output_dir, filename + '.jpg')

    def update_progress(self, current: int, total: int):
        """진행률 바 업데이트"""
        percentage = (current / total) * 100

        # UI 업데이트는 메인 스레드에서 실행
        self.root.after(0, self._update_progress_ui, current, total, percentage)

    def _update_progress_ui(self, current: int, total: int, percentage: float):
        """진행률 UI 업데이트 (메인 스레드)"""
        self.progress['value'] = percentage
        self.progress_text.config(text=f"{current} / {total} ({percentage:.1f}%)")
        self.root.update_idletasks()

    def conversion_complete(self, success_count: int, total_count: int,
                           failed_files: List[Tuple[str, str]]):
        """변환 완료 처리"""
        # UI 업데이트는 메인 스레드에서 실행
        self.root.after(0, self._conversion_complete_ui, success_count,
                       total_count, failed_files)

    def _conversion_complete_ui(self, success_count: int, total_count: int,
                                failed_files: List[Tuple[str, str]]):
        """변환 완료 UI 업데이트 (메인 스레드)"""
        # 진행률 100%
        self.progress['value'] = 100
        self.progress_text.config(text=f"{total_count} / {total_count} (100%)")

        # 버튼 다시 활성화
        self.btn_convert.config(state=tk.NORMAL)
        self.is_converting = False

        # 결과 메시지
        if failed_files:
            failed_list = "\n".join([f"- {name}: {error}" for name, error in failed_files])
            message = (f"변환 완료!\n\n"
                      f"성공: {success_count}개\n"
                      f"실패: {len(failed_files)}개\n\n"
                      f"실패한 파일:\n{failed_list}")
            messagebox.showwarning("변환 완료", message)
        else:
            messagebox.showinfo("변환 완료",
                              f"모든 이미지가 성공적으로 변환되었습니다!\n\n"
                              f"총 {success_count}개 파일")


def main():
    """메인 실행 함수"""
    root = TkinterDnD.Tk()
    app = ImageConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
