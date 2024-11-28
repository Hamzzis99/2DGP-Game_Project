# ball.py

from pico2d import *
import game_world
import game_framework
from game_object import GameObject
from states import game_state
from utils.camera import Camera  # 카메라 임포트
from utils.config import MarioConfig
from utils.score_text import ScoreText
import math  # 거리 계산을 위한 math 모듈 임포트


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

        # 시작 위치 저장
        self.start_x = x
        self.start_y = y
        self.distance_traveled = 0  # 이동 거리 누적을 위한 변수 추가

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

    def draw_with_camera(self, camera: Camera):
        if self.image:
            screen_x, screen_y = camera.apply(self.x, self.y)
            self.image.draw(screen_x, screen_y)
            draw_rectangle(*self.get_bb_offset(camera))
        else:
            print("Ball 이미지가 로드되지 않아 그릴 수 없습니다.")

    def get_bb_offset(self, camera: Camera):
        left, bottom, right, top = self.get_bb()
        return left - camera.camera_x, bottom - camera.camera_y, right - camera.camera_x, top - camera.camera_y

    def update(self):
        # 이전 위치 저장
        prev_x, prev_y = self.x, self.y

        # 위치 업데이트
        self.x += self.velocity_x * game_framework.frame_time
        self.y += self.velocity_y * game_framework.frame_time

        # 이동한 거리 계산 및 누적
        delta_x = self.x - prev_x
        delta_y = self.y - prev_y
        delta_distance = math.hypot(delta_x, delta_y)
        self.distance_traveled += delta_distance

        #print(f"Ball 업데이트: 위치=({self.x}, {self.y}), 이동 거리 누적={self.distance_traveled}")

        # 이동 거리 제한 확인
        if self.distance_traveled >= 200:
            try:
                game_world.remove_object(self)
                print("Ball 객체가 이동 거리 200을 초과하여 제거되었습니다.")
            except ValueError:
                print(f"Ball 객체 {self}는 이미 제거되었습니다.")
            return  # 이후 코드 실행 방지

        # 월드 범위 밖으로 나갔을 경우 제거
        if self.x < 0 or self.x > MarioConfig.WORLD_WIDTH or self.y < 0 or self.y > MarioConfig.WORLD_HEIGHT:
            try:
                game_world.remove_object(self)
                print("Ball 객체가 월드 밖으로 나가 제거되었습니다.")
            except ValueError:
                print(f"Ball 객체 {self}는 이미 제거되었습니다.")

            # 충돌 그룹에서 제거 (필요에 따라 추가)

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

        elif group == 'fire_ball:koomba':
            print(f"Ball이 Koomba와 충돌했습니다: Ball={self}, Koomba={other}")

            # 사운드 재생 추가 (클래스 변수 사용)
            if Ball.common_kick_sound:
                Ball.common_kick_sound.play()
                print("common_kick_sound 재생됨.")
            else:
                print("common_kick_sound가 로드되지 않았습니다.")

            # Koomba 제거
            try:
                game_world.remove_object(other)
                print("Koomba 객체가 제거되었습니다.")
            except ValueError:
                print(f"Koomba 객체 {other}가 이미 제거되었습니다.")

            # Ball 제거
            try:
                game_world.remove_object(self)
                print("Ball 객체가 제거되었습니다.")
            except ValueError:
                print(f"Ball 객체 {self}는 이미 제거되었습니다.")
            # 점수 추가
            game_state.score += 100
            print(f"Score increased by 100. Total Score: {game_state.score}")
            score_text = ScoreText(self.x, self.y + 30, "+100")
            game_world.add_object(score_text, 2)
            print("ScoreText 추가됨: +100")

        elif group == 'fire_ball:boss_turtle':
            print(f"Ball이 Boss_turtle과 충돌했습니다: Ball={self}, Boss_turtle={other}")

            # 사운드 재생 추가 (클래스 변수 사용)
            if Ball.common_kick_sound:
                Ball.common_kick_sound.play()
                print("common_kick_sound 재생됨.")
            else:
                print("common_kick_sound가 로드되지 않았습니다.")

            # Ball 제거
            try:
                game_world.remove_object(self)
                print("Ball 객체가 제거되었습니다.")
            except ValueError:
                print(f"Ball 객체 {self}는 이미 제거되었습니다.")

            # 점수 추가 (각 충돌 시)
            #game_state.score += 100  # 점수는 필요에 따라 조정 가능
            #print(f"Score increased by 100. Total Score: {game_state.score}")
            #score_text = ScoreText(self.x, self.y + 30, "+100")
            #game_world.add_object(score_text, 2)
            #print("ScoreText 추가됨: +100")

        elif group in ['fire_ball:brick', 'fire_ball:clean_box', 'fire_ball:gun_box', 'fire_ball:random_box']:
            print(f"Ball이 벽과 충돌했습니다: {group}")
            # Ball 제거
            try:
                game_world.remove_object(self)
                print("Ball 객체가 벽과의 충돌로 제거되었습니다.")
            except ValueError:
                print(f"Ball 객체 {self}는 이미 제거되었습니다.")

        else:
            pass
