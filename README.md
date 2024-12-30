# MapleWorld: In-Nae's Forest 2D Platformer - Reinforcement Learning Attempt

**MapleWorld** is a 2D platformer game based on the popular **MapleStory** game. This project attempts to utilize **Reinforcement Learning (RL)** to control a character in the **In-Nae's Forest** environment. The goal is to navigate platforms, avoid falling, and jump to reach the next platform, all while learning from the environment. Currently, the implementation focuses on capturing the game screen, detecting the platforms and character, and automating basic movement actions (left, right, jump).

The project utilizes Python libraries like **psutil**, **pyautogui**, **opencv**, and **numpy** to detect the game window and interact with the game environment. It employs **image processing** to track the character and platforms in the game world.

## Current Status

- The game process (`msw.exe`) is successfully located and the game window is activated using **psutil** and **win32gui**.
- Character and platform detection is based on color masks, but it struggles to find the platforms accurately, as using color-based tracking has its limitations (e.g., the game uses a variety of colors).
- Movement actions like jumping and moving left/right are automated using **pyautogui**.
- The **Reinforcement Learning** part is still under development, and rewards and penalties are calculated based on the character's vertical position relative to the platforms.

## Features

- **Process Detection**: Locates the running game process (`msw.exe`) and brings the game window to the foreground.
- **Platform Detection**: Uses image processing techniques to detect platforms based on color masks.
- **Character Detection**: Tracks the character's position by identifying skin-tone or label-based colors, but this could be improved with more reliable image recognition methods.
- **Movement Automation**: Moves the character using keyboard inputs (left, right, and jump).
- **Screen Capture**: Captures game screen in real-time and processes it to detect platforms and the character's position.
- **Reward Calculation**: Rewards or penalizes the character based on its position (currently using the height of the character relative to platforms).

## Future Goals

1. **Improve Platform Detection**: The current color-based approach has limitations and often fails to detect platforms accurately. A more reliable method such as using **template matching** or **image segmentation** could be implemented for better results.
2. **Enhance Character Detection**: Right now, character detection is done via simple color-based methods, but it can be improved using **machine learning-based object detection** (e.g., YOLO or OpenCV's Haar Cascades).
3. **Reinforcement Learning**: The RL component needs to be strengthened. Specifically, training an agent to navigate the platforms efficiently using RL algorithms (like **Q-learning** or **Deep Q Networks (DQN)**) should be explored.
4. **Keyboard Input Improvements**: Instead of simple key presses, more nuanced movements (such as holding down keys) can be implemented to make the character move more naturally.
5. **Generalization**: Currently, the setup is highly specific to the game's layout. A more generalized solution could allow this to work with other 2D platformer games.

## How to Run

1. **Install Required Libraries**:
   Make sure you have Python 3.x installed and the following libraries:
   
   ```
   pip install psutil pyautogui opencv-python numpy pywin32
   ```

2. **Run the Code**:
   Simply execute the Python script:

   ```bash
   python main.py
   ```

3. The game will start detecting the platforms and automatically move the character. It will also display the character and platform positions on the screen using **OpenCV**.

## Code Explanation

### 1. **find_msw_process()**:
   This function locates the `msw.exe` process running the MapleStory game. It uses **psutil** to iterate through all running processes and return the **PID** of the game.

### 2. **find_window_handle()**:
   Once the game process is located, the function finds the window handle using **win32gui** and **win32process**.

### 3. **activate_window()**:
   This function brings the game window to the foreground, ensuring that it is focused and ready to receive simulated keyboard inputs.

### 4. **capture_game_screen()**:
   Captures the current game screen using **pyautogui** and converts the image into a **NumPy array** for further processing with **OpenCV**.

### 5. **get_character_height_and_x()**:
   Uses image processing to detect the character in the game by looking for skin-tone or specific labels. The function returns the character's **x** and **y** coordinates.

### 6. **get_platforms()**:
   Detects platforms based on their color using **OpenCV**'s thresholding methods. It returns the **x**, **y**, width, and height of each detected platform.

### 7. **press_key()**:
   Automates keyboard input (left, right, and jump) using **pyautogui**.

### 8. **main()**:
   The main game loop, where the game processes the character and platform positions, makes decisions (move left, right, jump), and displays real-time data on the screen using **OpenCV**.

## Conclusion

This project shows a promising start towards building an AI agent capable of learning to play a 2D platformer game using **Reinforcement Learning**. The game environment is captured and processed using image-based methods, and basic automation tasks (like jumping and moving) are implemented. However, further improvements are needed in terms of platform and character detection accuracy and the integration of a proper reinforcement learning model.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### GitHub Account
**hwkims** - [GitHub Profile](https://github.com/hwkims)

# MapleWorld: 인내의 숲 2D 플랫폼 게임 - 강화학습 시도

**MapleWorld**는 인기 게임 **메이플스토리**의 **인내의 숲**을 기반으로 한 2D 플랫폼 게임입니다. 이 프로젝트는 **강화학습 (Reinforcement Learning, RL)**을 활용하여 게임 내 캐릭터를 제어하는 것을 목표로 하고 있습니다. 캐릭터는 플랫폼을 건너뛰며, 발판을 찾고, 점프하여 다음 발판에 도달해야 합니다. 현재 구현은 게임 화면 캡처, 플랫폼 및 캐릭터 추적, 그리고 기본적인 이동 동작(좌/우/점프)을 자동화하는 데 집중하고 있습니다.

이 프로젝트는 **psutil**, **pyautogui**, **opencv**, **numpy**와 같은 파이썬 라이브러리를 사용하여 게임 창을 찾고, 화면을 캡처하고, 게임 환경과 상호작용합니다. 현재 **이미지 처리**를 통해 캐릭터와 발판을 추적하고 있습니다.

## 현재 상태

- 게임 프로세스(`msw.exe`)를 성공적으로 찾고, **psutil**과 **win32gui**를 사용하여 게임 창을 활성화하는 데 성공했습니다.
- 발판 추적은 **색상 기반** 방법을 사용하지만, 다양한 색상이 사용되는 게임 환경에서는 제대로 발판을 추적하지 못하는 경우가 있습니다.
- 캐릭터와 발판을 추적하는 데 **이미지 처리**를 사용하고 있으며, 이를 바탕으로 좌/우 이동 및 점프 동작을 자동화합니다.
- **강화학습** 부분은 아직 개발 중이며, 캐릭터의 위치에 따른 보상 계산은 기본적인 형태로 구현되었습니다.

## 주요 기능

- **프로세스 탐지**: 실행 중인 게임 프로세스(`msw.exe`)를 찾아 게임 창을 활성화합니다.
- **발판 탐지**: 색상 마스크를 사용하여 발판을 추적합니다.
- **캐릭터 탐지**: 캐릭터의 위치를 추적하기 위해 색상 기반 또는 라벨을 기반으로 한 방법을 사용합니다.
- **이동 자동화**: 좌/우/점프 키 입력을 자동으로 생성하여 캐릭터를 이동시킵니다.
- **화면 캡처**: 게임 화면을 실시간으로 캡처하고, OpenCV로 처리하여 캐릭터와 발판을 추적합니다.
- **보상 계산**: 캐릭터의 위치에 따라 보상을 계산하며, 현재는 캐릭터의 높이에 따른 보상 시스템이 구현되어 있습니다.

## 향후 목표

1. **발판 탐지 개선**: 현재 색상 기반 방법은 한계가 있어, **템플릿 매칭**이나 **이미지 분할**을 사용하여 더 정확한 발판 탐지가 필요합니다.
2. **캐릭터 탐지 개선**: 캐릭터 탐지는 현재 단순한 색상 기반 방법을 사용하지만, **머신러닝 기반 객체 탐지**(예: YOLO 또는 OpenCV의 Haar Cascade)를 사용하여 개선할 수 있습니다.
3. **강화학습 구현**: 강화학습 알고리즘을 활용해, 에이전트가 발판을 안전하게 건너는 방법을 학습하도록 해야 합니다. **Q-러닝** 또는 **DQN**(심층 Q-네트워크)을 적용할 수 있습니다.
4. **키 입력 개선**: 현재 키 입력은 단순히 누르는 방식이지만, 키를 길게 눌러서 자연스러운 캐릭터 이동을 구현할 수 있습니다.
5. **일반화**: 현재 구현은 특정 게임 환경에 맞춰져 있으므로, 다른 2D 플랫폼 게임에서도 작동하도록 **일반화**할 수 있는 방법을 찾아야 합니다.

## 실행 방법

1. **필요한 라이브러리 설치**:
   Python 3.x과 다음 라이브러리를 설치해야 합니다:
   
   ```bash
   pip install psutil pyautogui opencv-python numpy pywin32
   ```

2. **코드 실행**:
   Python 스크립트를 실행하면 게임 화면이 캡처되고, 발판을 탐지하여 캐릭터가 자동으로 이동합니다:

   ```bash
   python main.py
   ```

3. 게임 화면과 발판 위치가 실시간으로 캡처되고, OpenCV를 통해 시각적으로 표시됩니다.

## 코드 설명

### 1. **find_msw_process()**:
   이 함수는 **psutil**을 사용하여 게임 프로세스(`msw.exe`)를 찾고, 해당 프로세스의 **PID**를 반환합니다.

### 2. **find_window_handle()**:
   게임 프로세스가 발견되면, **win32gui**와 **win32process**를 사용하여 해당 프로세스의 윈도우 핸들을 찾습니다.

### 3. **activate_window()**:
   이 함수는 게임 창을 화면에 띄우고, 게임 창이 사용자에게 포커스를 받을 수 있도록 합니다.

### 4. **capture_game_screen()**:
   **pyautogui**를 사용하여 게임 화면을 캡처하고, 이를 **NumPy 배열**로 변환하여 **OpenCV**로 처리할 수 있게 만듭니다.

### 5. **get_character_height_and_x()**:
   이미지 처리 기술을 사용하여 게임 화면에서 캐릭터를 추적합니다. 색상 기반 또는 라벨 기반 방법을 사용해 캐릭터의 **x**, **y** 좌표를 반환합니다.

### 6. **get_platforms()**:
   게임 화면에서 발판을 추적하는 함수로, 색상 마스크를 사용하여 발판의 **x**, **y**, 너비 및 높이를 반환합니다.

### 7. **press_key()**:
   **pyautogui**를 사용하여 좌/우/점프 키 입력을 자동으로 수행합니다.

### 8. **main()**:
   게임의 메인 루프에서 캐릭터와 발판 위치를 추적하고, **강화학습**을 바탕으로 행동을 선택합니다. 화면에 캐릭터와 발판 위치를 실시간으로 표시합니다.

## 결론

이 프로젝트는 **강화학습**을 활용하여 2D 플랫폼 게임을 자동으로 플레이하는 가능성을 보여주는 좋은 시작점입니다. 현재는 게임 화면 캡처 및 이미지 처리 방법을 사용하여 캐릭터와 발판을 추적하고, 기본적인 이동 동작을 구현하고 있습니다. 그러나 **발판 탐지**와 **강화학습** 모델의 성능 개선이 필요하며, **머신러닝 기반 객체 탐지**(예: YOLO)를 적용하여 더 정확한 추적을 할 수 있을 것입니다.

## 라이선스

이 프로젝트는 **MIT 라이선스** 하에 제공됩니다. 자세한 사항은 [LICENSE](LICENSE) 파일을 참고해주세요.

---

### GitHub 계정
**hwkims** - [GitHub 프로필](https://github.com/hwkims)
