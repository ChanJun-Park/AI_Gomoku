minmax 알고리즘, alpha beta pruning 기법을 적용한 AI 오목 게임

- 프로그램 실행 방법
프로그램을 실행하기 위해서는 pygame 라이브러리가 설치되어 있어야 한다.

설치 방법 : 명령 프롬프트(Anaconda python인 경우는 Anaconda prompt)에서 다음 명령어 입력

python3 -m pip install -U pygame --user
또는
python -m pip install -U pygame --user

pygame 라이브러리가 설치된 이후 다시 명령 프롬프트나 Anaconda prompt에서 AI_Gomoku.py가 포함된 디렉토리로 이동한 뒤 다음 명령어 입력

python3 AI_Gomoku.py
또는
python AI_Gomoku.py

- 실행 파일 : AI_Gomoku.py
- AI agent 클래스가 정의된 파일 : minmax.py, alpha_beta.py, alpha_beta3.py
- 게임에 사용되는 상수들이 정의된 파일 : gomoku_constant.py
- 평가함수를 적용할 패턴과 그에 대응하는 점수를 정의한 파일 : evaluation_constant.py