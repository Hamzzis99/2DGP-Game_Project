# ball.py

from pico2d import *
import game_world
import game_framework
from game_object import GameObject
from states import game_state
from utils.camera import Camera  # 카메라 임포트
from utils.config import MarioConfig
from utils.score_text import ScoreText


class Ball(GameObject):
    image = None
    common_kick_sound = None  # 클래스 변수로 변경

    def __init__(self, x, y, velocity_x, velocity_y=0):
        print(f"Ball 객체 생성: 위치=({x}, {y}), 속도=({velocity_x}, {velocity_y})")
        if Ball.image is None:
            try:
                Ball.image = load_image('ball21x21.png')  # 이미지 경로와 파일명 확인
                #print("Ball 이미지 로드 성공")
            except Exception as e:
                print(f"Ball 이미지 로드 실패: {e}")
        self.x, self.y = x, y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.width = 32
        self.height = 32

        # 클래스 변수로 사운드 로드 (한 번만 로드)
        if Ball.common_kick_sound is None:
            try:
                Ball.common_kick_sound = load_wav('sound/kick.ogg')  # WAV 파일 로드
                Ball.common_kick_sound.set_volume(64)  # 볼륨 설정 (0-128)
                print("common_kick_sound 로드 및 설정 완료.")
            except Exception as e:
                Ball.common_kick_sound = None
                print(f"common_kick_sound 로드 실패: {e}")

    def draw(self):
        if self.image:
            self.image.draw(self.x, self.y)
            draw_rectangle(*self.get_bb())  # 충돌 박스 그리기
        else:
            print("Ball 이미지가 로드되지 않아 그릴 수 없습니다.")
        pass  # draw 메서드에서는 아무것도 하지 않음

    def draw_with_camera(self, camera):
        if self.image:
            screen_x, screen_y = camera.apply(self.x, self.y)
            self.image.draw(screen_x, screen_y)
            draw_rectangle(*self.get_bb_offset(camera))
        else:
            print("Ball 이미지가 로드되지 않아 그릴 수 없습니다.")

    def get_bb_offset(self, camera):
        left, bottom, right, top = self.get_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def update(self):
        #print(f"Ball 업데이트: 위치=({self.x}, {self.y})")
        self.x += self.velocity_x * game_framework.frame_time
        self.y += self.velocity_y * game_framework.frame_time

        if self.x < 0 or self.x > MarioConfig.WORLD_WIDTH or self.y < 0 or self.y > MarioConfig.WORLD_HEIGHT:
            try:
                game_world.remove_object(self)
                print("Ball 객체가 게임 월드에서 제거되었습니다.")
            except ValueError:
                print(f"Ball 객체 {self}는 이미 제거되었습니다.")
            # 'fire_ball:turtle' 충돌 그룹에서 제거
            if 'fire_ball:turtle' in game_world.collision_pairs:
                if self in game_world.collision_pairs['fire_ball:turtle'][0]:
                    game_world.collision_pairs['fire_ball:turtle'][0].remove(self)

    def get_bb(self):
        return self.x - self.width / 2, self.y - self.height / 2, \
               self.x + self.width / 2, self.y + self.height / 2

    def handle_collision(self, group, other, hit_position):
        if group == 'fire_ball:turtle':
            print(f"Ball이 Turtle과 충돌했습니다: Ball={self}, Turtle={other}")

            # 사운드 재생 추가 (클래스 변수 사용)
            if Ball.common_kick_sound:
                Ball.common_kick_sound.play()
                print("common_kick_sound 재생됨.")
            else:
                print("common_kick_sound가 로드되지 않았습니다.")

            # Turtle 제거
            try:
                game_world.remove_object(other)
                print("Turtle 객체가 제거되었습니다.")
            except ValueError:
                print(f"Turtle 객체 {other}가 이미 제거되었습니다.")

            # Ball 제거
            try:
                game_world.remove_object(self)
                print("Ball 객체가 제거되었습니다.")
            except ValueError:
                print(f"Ball 객체 {self}는 이미 제거되었습니다.")

            # 점수 추가
            game_state.score += 200
            print(f"Score increased by 200. Total Score: {game_state.score}")
            score_text = ScoreText(self.x, self.y + 30, "+200")
            game_world.add_object(score_text, 2)
            print("ScoreText 추가됨: +200")
