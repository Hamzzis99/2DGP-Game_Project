# utils/bgm.py

from pico2d import load_music, Music
import os

class BGMManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BGMManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.music_tracks = {}
        self.current_music = None
        self._initialized = True

    def load_music(self, name, filepath):
        if name in self.music_tracks:
            print(f"[BGMManager] '{name}' 음악은 이미 로드되었습니다.")
            return
        if not os.path.exists(filepath):
            print(f"[BGMManager] 음악 파일을 찾을 수 없습니다: {filepath}")
            return
        try:
            music = load_music(filepath)
            self.music_tracks[name] = music
            print(f"[BGMManager] '{name}' 음악이 로드되었습니다: {filepath}")
        except Exception as e:
            print(f"[BGMManager] 음악 로드 실패: {filepath}, 에러: {e}")

    def play(self, name, volume=64):
        if name not in self.music_tracks:
            print(f"[BGMManager] '{name}' 음악을 찾을 수 없습니다.")
            return
        if self.current_music is not None:
            self.current_music.stop()
        self.current_music = self.music_tracks[name]
        self.current_music.set_volume(volume)
        try:
            self.current_music.play(-1)  # 무한 반복을 위해 loops=-1 설정
            print(f"[BGMManager] '{name}' 음악을 재생합니다. 볼륨: {volume}")
        except Exception as e:
            print(f"[BGMManager] 음악 재생 중 에러 발생: {e}")

    def stop(self):
        if self.current_music is not None:
            self.current_music.stop()
            print(f"[BGMManager] 현재 음악을 중지했습니다.")
            self.current_music = None

    def set_volume(self, volume):
        if self.current_music is not None:
            self.current_music.set_volume(volume)
            print(f"[BGMManager] 볼륨이 {volume}으로 설정되었습니다.")
        else:
            print("[BGMManager] 재생 중인 음악이 없습니다. 볼륨을 설정할 수 없습니다.")

    def get_volume(self):
        if self.current_music is not None:
            return self.current_music.get_volume()
        return None
