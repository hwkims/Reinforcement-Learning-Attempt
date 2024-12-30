import psutil
import win32gui
import win32con
import pyautogui
import time
import win32process
import numpy as np
import cv2


# msw.exe 프로세스 찾기
def find_msw_process():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'msw.exe':
            return proc.info['pid']
    return None


# 특정 프로세스의 윈도우 핸들 찾기
def find_window_handle(pid):
    def enum_windows_callback(hwnd, lparam):
        try:
            _, process_id = win32process.GetWindowThreadProcessId(hwnd)
            if process_id == pid:
                lparam.append(hwnd)
        except Exception as e:
            print("Error in enum_windows_callback:", e)

    hwnds = []
    win32gui.EnumWindows(enum_windows_callback, hwnds)
    return hwnds[0] if hwnds else None


# 윈도우 활성화 및 포커스 맞추기
def activate_window(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)


# 게임 화면 캡처
def capture_game_screen(window):
    left, top, right, bottom = win32gui.GetClientRect(window)
    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
    screenshot_np = np.array(screenshot)
    screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    return screenshot_cv


# 키보드 입력 자동화 (방향키, 점프)
def press_key(key):
    if key == 'left':
        pyautogui.keyDown('left')
        time.sleep(0.1)
        pyautogui.keyUp('left')
    elif key == 'right':
        pyautogui.keyDown('right')
        time.sleep(0.1)
        pyautogui.keyUp('right')
    elif key == 'alt':  # 점프
        pyautogui.keyDown('alt')
        time.sleep(0.1)
        pyautogui.keyUp('alt')


# 캐릭터 위치 추적 (움직이는 객체 추적)
def get_character_height_and_x(window):
    # 게임 화면 캡처
    screen = capture_game_screen(window)

    # 화면을 그레이스케일로 변환
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # 특정 색상을 기반으로 캐릭터 영역 추적
    lower_skin = np.array([50, 40, 40])  # 살색 범위 (상대적으로 빨간색 계열)
    upper_skin = np.array([255, 220, 200])  # 살색 범위
    mask_skin = cv2.inRange(screen, lower_skin, upper_skin)

    # 이름표 "인내" 추적을 위한 마스크 추가 (가장 간단한 방법으로 예시)
    lower_label = np.array([0, 0, 0])  # 색상에 따라 조정
    upper_label = np.array([255, 255, 255])
    mask_label = cv2.inRange(screen, lower_label, upper_label)

    # 두 마스크 합치기
    combined_mask = cv2.bitwise_or(mask_skin, mask_label)

    # 마스크에서 가장 큰 객체(캐릭터)를 찾기
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    character_x = None
    character_height = None

    if contours:
        # 가장 큰 객체를 찾음
        largest_contour = max(contours, key=cv2.contourArea)

        # 객체의 경계 상자 계산
        x, y, w, h = cv2.boundingRect(largest_contour)

        # 캐릭터의 높이와 x 좌표
        character_x = x + w // 2  # 캐릭터의 중심 x 좌표
        character_height = y  # 캐릭터의 y 좌표 (높이)

    return character_x, character_height, screen


# 발판 추적 (발판의 y 좌표 찾기)
def get_platforms(window):
    # 게임 화면 캡처
    screen = capture_game_screen(window)

    # 특정 색상 범위를 이용해 갈색 발판 추적
    lower_platform = np.array([100, 50, 0])  # 갈색 발판 색상 범위 (예시)
    upper_platform = np.array([200, 150, 50])
    mask_platform = cv2.inRange(screen, lower_platform, upper_platform)

    # 마스크에서 발판 추적
    contours, _ = cv2.findContours(mask_platform, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    platforms = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        platforms.append((x, y, w, h))  # 발판 위치와 크기

    return platforms, screen


# MSW.exe 게임을 제어하는 메인 루프
def main():
    pid = find_msw_process()  # msw.exe 프로세스를 찾기
    if pid is None:
        print("msw.exe 프로세스를 찾을 수 없습니다.")
        return

    hwnd = find_window_handle(pid)  # 해당 프로세스의 윈도우 핸들 찾기
    if hwnd is None:
        print("게임 창을 찾을 수 없습니다.")
        return

    # 게임 창 활성화
    activate_window(hwnd)

    # 게임 루프
    for episode in range(10):  # 예시: 10번의 에피소드
        print(f"에피소드 {episode + 1} 시작")

        # 게임 상태 초기화
        done = False
        score = 0  # 예시: 점수 초기화
        last_time = time.time()
        jumping = False  # 점프 상태 추적 변수

        while not done:
            # 발판 추적
            platforms, screen = get_platforms(hwnd)

            # 캐릭터 위치 추적
            character_x, character_height, _ = get_character_height_and_x(hwnd)

            # 발판이 있으면 가장 가까운 발판 찾기
            if platforms:
                # 가장 높은 발판 찾기 (y 값이 가장 작은 발판)
                closest_platform = min(platforms, key=lambda p: p[1])

                # 발판의 y 좌표
                platform_y = closest_platform[1]
                platform_x = closest_platform[0]

                # 캐릭터가 발판 위에 있으면 점프하지 않음
                if character_height is not None and character_height < platform_y:
                    press_key('alt')  # 점프

                # 행동: 무작위 방향 (0: 왼쪽, 1: 오른쪽, 2: 점프)
                action = np.random.choice([0, 1, 2])

                # 발판 간 이동: 발판의 위치로 이동
                if action == 0:  # 왼쪽
                    if platform_x < 300:  # 발판이 왼쪽에 있을 때
                        press_key('left')
                    press_key('alt')  # 점프
                elif action == 1:  # 오른쪽
                    if platform_x > 300:  # 발판이 오른쪽에 있을 때
                        press_key('right')
                    press_key('alt')  # 점프
                else:  # 점프만
                    press_key('alt')

            # 화면에 발판과 캐릭터의 x, y 좌표 표시
            if character_x is not None:
                cv2.putText(screen, f"Character x: {character_x}, y: {character_height}",
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            if platforms:
                for plat in platforms:
                    plat_x, plat_y, plat_w, plat_h = plat
                    cv2.rectangle(screen, (plat_x, plat_y), (plat_x + plat_w, plat_y + plat_h), (0, 255, 0), 2)
                    cv2.putText(screen, f"Platform x: {plat_x}, y: {plat_y}",
                                (plat_x, plat_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

            # 화면 표시
            cv2.imshow('Captured Game Screen', screen)
            cv2.waitKey(1)

            # 시간에 따른 점수 감소
            current_time = time.time()
            time_elapsed = current_time - last_time
            score -= int(time_elapsed * 1)  # 시간이 지날수록 점수 감소

            # 보상 계산: 발판을 향해 올라가는지 확인
            reward = 1 if character_height is not None and character_height < 100 else -1
            score += reward

            # 출력: 현재 위치, 점수, 행동
            print(f"행동: {action}, 현재 위치(y): {character_height}, 보상: {reward}, 점수: {score}")

            # 종료 조건 (랜덤 종료 조건 예시)
            if np.random.rand() < 0.05:
                done = True
                print(f"에피소드 {episode + 1} 종료")

            last_time = current_time

    cv2.destroyAllWindows()


# 실행
if __name__ == '__main__':
    main()
