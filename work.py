import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import matplotlib  # 이 부분이 필요합니다.


# CSV 파일 경로 지정
file_path = "data/england-premier-league-matches-2018-to-2019-stats.csv"

# 데이터 읽기
try:
    data = pd.read_csv(file_path)
    st.write("데이터 미리보기:")
    st.write(data.head())
except FileNotFoundError:
    st.error("CSV 파일을 찾을 수 없습니다. 파일 경로를 확인하세요.")

# 나눔고딕 폰트 경로
font_path = "fonts/NanumGothic.ttf"
font_prop = fm.FontProperties(fname=font_path)

# 폰트 설정
plt.rc('font', family=font_prop.get_name())
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 앱 제목
st.title("확률적 사고를 위한 융합 학습 앱")

# 메뉴 선택
menu = st.sidebar.selectbox("메뉴 선택", ["복권 시뮬레이션", "룰렛 시뮬레이션", "스포츠 시뮬레이션"])

# 복권 시뮬레이션
if menu == "복권 시뮬레이션":
    st.image("나눔 로또.jpeg", caption="복권 시뮬레이션", use_column_width=True)

    # 초기화
    if "lottery_balance" not in st.session_state:
        st.session_state["lottery_balance"] = 0
    if "lottery_bet_history" not in st.session_state:
        st.session_state["lottery_bet_history"] = []

    st.header("복권의 위험성")
    승리확률 = 1 / st.number_input("당첨 확률 입력 (1/값)", min_value=1, step=1, value=8140000)
    보상 = st.number_input("당첨 보상 입력", min_value=0, step=10000000, value=3000000000)
    손실 = st.number_input("손실 금액 입력", min_value=0, step=100, value=1000)
    기대값 = 승리확률 * 보상 - (1 - 승리확률) * 손실
    st.write(f"기대값: {기대값:.2f}")

    if st.button("복권 결과 확인"):
        result = random.random() < 승리확률
        if result:
            st.success(f"축하합니다! {보상}원을 획득했습니다!")
            st.session_state["lottery_balance"] += 보상 - 손실
        else:
            st.error(f"아쉽습니다! {손실}원을 잃었습니다.")
            st.session_state["lottery_balance"] -= 손실

        # 기록 저장
        st.session_state["lottery_bet_history"].append({
            "승리 여부": "당첨" if result else "꽝",
            "손익": 보상 - 손실 if result else -손실
        })

    st.write(f"복권 누적 손익: {st.session_state['lottery_balance']}원")
    if st.checkbox("복권 기록 보기"):
        st.write(pd.DataFrame(st.session_state["lottery_bet_history"]))

    if st.checkbox("복권 손익 그래프 보기"):
        history = st.session_state["lottery_bet_history"]
        balances = [h["손익"] for h in history]
        cumulative_balance = [sum(balances[:i+1]) for i in range(len(balances))]

        fig, ax = plt.subplots()
        ax.plot(cumulative_balance, marker="o", linestyle="-")
        ax.set_title("복권 누적 손익 변화")
        ax.set_xlabel("베팅 횟수")
        ax.set_ylabel("손익 (원)")
        st.pyplot(fig)

# 룰렛 시뮬레이션
elif menu == "룰렛 시뮬레이션":
    st.image("카지노 룰렛.jpeg", caption="룰렛 시뮬레이션", use_column_width=True)

    # 초기화
    if "casino_balance" not in st.session_state:
        st.session_state["casino_balance"] = 0
    if "casino_bet_history" not in st.session_state:
        st.session_state["casino_bet_history"] = []

    st.title("룰렛 시뮬레이션")
    roulette_numbers = list(range(0, 37)) + ["00"]
    roulette_colors = {
        0: "green", "00": "green",
        **{n: "red" for n in range(1, 37) if n % 2 == 1},
        **{n: "black" for n in range(1, 37) if n % 2 == 0}
    }

    bet_type = st.radio("베팅 방식을 선택하세요:", ("숫자", "빨강/검정", "홀수/짝수"))
    if bet_type == "숫자":
        user_choice = st.selectbox("베팅할 숫자를 선택하세요:", roulette_numbers)
    elif bet_type == "빨강/검정":
        user_choice = st.selectbox("빨강 또는 검정을 선택하세요:", ["red", "black"])
    else:
        user_choice = st.selectbox("홀수 또는 짝수를 선택하세요:", ["홀수", "짝수"])

    bet_amount = st.number_input("베팅 금액을 입력하세요 (단위: 원):", min_value=1, step=1, value=100)

    if st.button("룰렛 돌리기"):
        roulette_result = random.choice(roulette_numbers)
        roulette_color = roulette_colors[roulette_result]
        st.write(f"룰렛 결과: **{roulette_result}** ({roulette_color.upper()})")

        if bet_type == "숫자":
            win = (user_choice == roulette_result)
            payout = bet_amount * 35 if win else 0
        elif bet_type == "빨강/검정":
            win = (user_choice == roulette_color)
            payout = bet_amount * 2 if win else 0
        else:
            is_odd = roulette_result not in ["0", "00"] and roulette_result % 2 == 1
            win = (user_choice == "홀수" and is_odd) or (user_choice == "짝수" and not is_odd)
            payout = bet_amount * 2 if win else 0

        balance_change = payout - bet_amount
        st.session_state["casino_balance"] += balance_change
        st.session_state["casino_bet_history"].append({
            "베팅": user_choice,
            "결과": roulette_result,
            "보상": payout,
            "손익": balance_change
        })

        if win:
            st.success(f"축하합니다! {payout}원을 획득했습니다! (손익: +{balance_change}원)")
        else:
            st.error(f"아쉽습니다! {bet_amount}원을 잃었습니다. (손익: {balance_change}원)")

    st.write(f"룰렛 누적 손익: {st.session_state['casino_balance']}원")
    if st.checkbox("룰렛 기록 보기"):
        st.write(pd.DataFrame(st.session_state["casino_bet_history"]))

    if st.checkbox("룰렛 손익 그래프 보기"):
        balance_changes = [h["손익"] for h in st.session_state["casino_bet_history"]]
        cumulative_balance = [sum(balance_changes[:i+1]) for i in range(len(balance_changes))]

        fig, ax = plt.subplots()
        ax.plot(cumulative_balance, marker="o", linestyle="-")
        ax.set_title("룰렛 누적 손익 변화")
        ax.set_xlabel("베팅 횟수")
        ax.set_ylabel("손익 (원)")
        st.pyplot(fig)

# 스포츠 시뮬레이션
elif menu == "스포츠 시뮬레이션":
    st.image("프리미어리그.jpeg", caption="스포츠 시뮬레이션", use_column_width=True, width=100)

    # 초기화
    if "sports_balance" not in st.session_state:
        st.session_state["sports_balance"] = 0
    if "sports_bet_history" not in st.session_state:
        st.session_state["sports_bet_history"] = []

    st.title("스포츠 시뮬레이션")
    matches = st.multiselect(
        "베팅할 경기를 선택하세요:",
        data[['home_team_name', 'away_team_name']].apply(
            lambda x: f"{x['home_team_name']} vs {x['away_team_name']}", axis=1
        )
    )

    if matches:
        predictions = {}
        for match in matches:
            st.write(f"경기: {match}")
            selected_match = data.loc[data[['home_team_name', 'away_team_name']].apply(
                lambda x: f"{x['home_team_name']} vs {x['away_team_name']}", axis=1
            ) == match]

            odds_home = selected_match['odds_ft_home_team_win'].values[0]
            odds_draw = selected_match['odds_ft_draw'].values[0]
            odds_away = selected_match['odds_ft_away_team_win'].values[0]

            st.write(f"배당률: 홈 승리({odds_home}), 무승부({odds_draw}), 원정 승리({odds_away})")

            predictions[match] = {
                "prediction": st.radio(
                    f"{match} 결과 예측:", ["홈 승리", "무승부", "원정 승리"],
                    key=f"prediction_{match}"
                ),
                "bet_amount": st.number_input(
                    f"{match} 배팅 금액 (원):", min_value=1000, step=1000, key=f"bet_{match}"
                )
            }

        if st.button("결과 확인"):
            for match in matches:
                selected_match = data.loc[data[['home_team_name', 'away_team_name']].apply(
                    lambda x: f"{x['home_team_name']} vs {x['away_team_name']}", axis=1
                ) == match]

                home_goals = selected_match['home_team_goal_count'].values[0]
                away_goals = selected_match['away_team_goal_count'].values[0]

                if home_goals > away_goals:
                    actual_result = "홈 승리"
                elif home_goals < away_goals:
                    actual_result = "원정 승리"
                else:
                    actual_result = "무승부"

                st.write(f"경기: {match}, 실제 결과: {actual_result}")

                prediction = predictions[match]["prediction"]
                bet_amount = predictions[match]["bet_amount"]

                if prediction == actual_result:
                    if actual_result == "홈 승리":
                        payout = bet_amount * odds_home
                    elif actual_result == "무승부":
                        payout = bet_amount * odds_draw
                    else:
                        payout = bet_amount * odds_away

                    st.success(f"예측 성공! {payout:.2f}원 획득!")
                    balance_change = payout - bet_amount
                else:
                    st.error(f"예측 실패! {bet_amount}원을 잃음!")
                    balance_change = -bet_amount

                st.session_state["sports_balance"] += balance_change
                st.session_state["sports_bet_history"].append({
                    "match": match,
                    "prediction": prediction,
                    "actual_result": actual_result,
                    "bet_amount": bet_amount,
                    "balance_change": balance_change
                })

            st.write(f"스포츠 누적 손익: {st.session_state['sports_balance']}원")
            if st.checkbox("스포츠 기록 보기"):
                st.write(pd.DataFrame(st.session_state["sports_bet_history"]))

            if st.checkbox("스포츠 손익 그래프 보기"):
                balance_changes = [h["balance_change"] for h in st.session_state["sports_bet_history"]]
                cumulative_balance = [sum(balance_changes[:i+1]) for i in range(len(balance_changes))]

                fig, ax = plt.subplots()
                ax.plot(cumulative_balance, marker="o", linestyle="-")
                ax.set_title("스포츠 누적 손익 변화")
                ax.set_xlabel("베팅 횟수")
                ax.set_ylabel("손익 (원)")
                st.pyplot(fig)