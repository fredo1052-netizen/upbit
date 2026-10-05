import streamlit as st
import requests

# 💡 스티브의 투자 정보 세팅 (화면 분석 기반)
AVG_PRICE = 26.86  # 매수평균가
PRINCIPAL = 22481894  # 원금 (평가금액 16,323,772 - 평가손익 -6,158,122)
COIN_AMOUNT = PRINCIPAL / AVG_PRICE  # 보유 수량 (약 837,002 개)
TICKER = "KRW-BOUNTY"

st.set_page_config(page_title="BOUNTY 실시간 현황", page_icon="📈", layout="centered")

def get_current_price(ticker):
    url = f"https://api.upbit.com/v1/ticker?markets={ticker}"
    headers = {"accept": "application/json"}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            return res.json()[0]['trade_price']
    except:
        return None
    return None

st.title("📈 나의 체인바운티(BOUNTY) 현황")

# 자동 새로고침 버튼 (누를 때마다 실시간 가격 반영)
if st.button("🔄 실시간 시세로 새로고침", use_container_width=True):
    pass 

current_price = get_current_price(TICKER)

if current_price:
    # 실시간 계산 로직
    eval_amount = current_price * COIN_AMOUNT
    profit_loss = eval_amount - PRINCIPAL
    profit_rate = (profit_loss / PRINCIPAL) * 100

    # 화면 출력 (모바일 친화적 큰 글씨)
    st.metric(label="현재가", value=f"{current_price:,.2f} 원", delta=f"내 평단({AVG_PRICE}원) 대비")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="평가금액", value=f"{int(eval_amount):,} 원", delta=f"{int(profit_loss):,} 원")
    with col2:
        st.metric(label="수익률", value=f"{profit_rate:.2f} %")
    
    st.divider()
    st.info(f"**총 매수금액 (원금):** {PRINCIPAL:,} 원\n\n**보유 수량:** {COIN_AMOUNT:,.2f} BOUNTY")
else:
    st.error("업비트 서버에서 시세를 가져오지 못했습니다. 종목 코드를 확인해주세요.")