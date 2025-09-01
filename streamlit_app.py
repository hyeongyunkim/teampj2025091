import streamlit as st
from datetime import datetime

# ===================== 기본 설정 =====================
st.set_page_config(
    page_title="무지개다리 | 반려동물 추모 서비스",
    page_icon="🌈",
    layout="wide",
)

# ===================== 간단 스타일 =====================
st.markdown(
    """
    <style>
      :root{--bg:#F7F1E8; --ink:#2E2722; --muted:#5C534B; --brand:#B08A6E; --line:#E4D8CB; --card:#FFFDF9;}
      html, body, [data-testid="stAppViewContainer"]{background:var(--bg); color:var(--ink); font-family:'Pretendard Variable','Noto Sans KR',Apple SD Gothic Neo,Malgun Gothic,Segoe UI,Roboto,sans-serif; font-size:16.5px; line-height:1.6;} 
      .top{position:sticky; top:0; z-index:100; backdrop-filter:saturate(180%) blur(8px); background:rgba(250,247,242,.85); border-bottom:1px solid var(--line);}
      .top .inner{max-width:1200px; margin:0 auto; padding:12px 16px; display:flex; align-items:center; justify-content:space-between;}
      .brand{font-weight:800; letter-spacing:.2px;}
      .muted{color:var(--muted);}
      .h1{font-size:46px; line-height:1.15; font-weight:800; letter-spacing:-.01em;}
      .kicker{font-size:12px; letter-spacing:.22em; text-transform:uppercase; color:#5E8F99; font-weight:700;}
      .card{background:white; border:1px solid var(--line); border-radius:16px; padding:18px; box-shadow:0 10px 24px rgba(0,0,0,.04)}
      .grid{display:grid; gap:16px}
      .g2{grid-template-columns:repeat(2, minmax(0,1fr))}
      .g3{grid-template-columns:repeat(3, minmax(0,1fr))}
      @media (max-width:900px){.g2,.g3{grid-template-columns:1fr}}
      .btn{display:inline-block; padding:10px 14px; border-radius:10px; border:1px solid var(--line);}
      .btn-primary{background:var(--brand); color:#fff; border-color:var(--brand);}
    </style>
    """,
    unsafe_allow_html=True,
)

# ===================== 상태 초기화 =====================
if "guestbook" not in st.session_state:
    st.session_state.guestbook = []  # {name, message, ts}
if "gallery" not in st.session_state:
    st.session_state.gallery = []    # [(bytes, filename)]

# ===================== 헤더/네비 =====================
st.markdown(
    """
    <div class="top"><div class="inner">
      <div class="brand">🌈 무지개다리</div>
      <div class="muted">부고장 · 방명록 · 추모관 | 스트리밍 | 조의·헌화</div>
    </div></div>
    """,
    unsafe_allow_html=True,
)

st.write("")  # spacing

# ===================== 네비게이션 =====================
page = st.radio(
    "",
    ["추모 공간", "장례식 스트리밍", "조의·헌화"],
    horizontal=True,
    label_visibility="collapsed",
)

# ======================================================
# 페이지 1: 부고장 / 방명록 / 추모관
# ======================================================

def render_page1():
    st.markdown("<div class='kicker'>Memorial</div>", unsafe_allow_html=True)
    st.markdown("<div class='h1'>함께한 시간을 가장 평온하게 기억합니다</div>", unsafe_allow_html=True)
    st.caption("부고장 · 방명록 · 추모관")

    # 섹션: 부고장
    st.subheader("부고장")
    with st.container(border=True):
        col1, col2 = st.columns([1,2])
        with col1:
            pet_name = st.text_input("반려동물 이름", placeholder="예: 보리")
            birth = st.date_input("생년월일", format="YYYY-MM-DD")
            passed = st.date_input("무지개 날짜", format="YYYY-MM-DD")
            short_msg = st.text_area("짧은 문구", placeholder="따뜻한 한 문장을 남겨보세요.")
            share = st.text_input("공유용 링크(선택)", placeholder="예: https://...")
        with col2:
            st.markdown("**미리보기**")
            st.markdown(
                f"""
                <div class='card'>
                  <h3 style='margin:0 0 8px 0'>{pet_name or '이름 미정'}</h3>
                  <div class='muted'>
                    {birth.strftime('%Y-%m-%d') if birth else '---- -- --'}
                    ~
                    {passed.strftime('%Y-%m-%d') if passed else '---- -- --'}
                  </div>
                  <p style='margin-top:10px'>{short_msg or '짧은 문구가 여기에 표시됩니다.'}</p>
                  <div class='muted'>{share or '공유 링크(선택)'}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # 섹션: 방명록
    st.subheader("방명록")
    with st.form("guestbook_form", clear_on_submit=True, border=True):
        gb_name = st.text_input("이름 또는 닉네임", placeholder="이름")
        gb_msg = st.text_area("메시지", placeholder="따뜻한 한마디를 남겨주세요.")
        submit = st.form_submit_button("남기기")
    if submit and gb_name and gb_msg:
        st.session_state.guestbook.append({
            "name": gb_name,
            "message": gb_msg,
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
    if st.session_state.guestbook:
        for item in reversed(st.session_state.guestbook[-30:]):
            st.markdown(
                f"""
                <div class='card'>
                  <div style='font-weight:700'>{item['name']}</div>
                  <div class='muted' style='font-size:12px'>{item['ts']}</div>
                  <p style='margin:8px 0 0 0'>{item['message']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("아직 방명록이 없습니다. 첫 메시지를 남겨보세요.")

    st.divider()

    # 섹션: 추모관(사진 그리드)
    st.subheader("추모관")
    uploads = st.file_uploader("사진 업로드 (여러 장 가능)", type=["png","jpg","jpeg"], accept_multiple_files=True)
    if uploads:
        for f in uploads:
            st.session_state.gallery.append((f.read(), f.name))
    if st.session_state.gallery:
        cols = st.columns(6)
        for idx, (data, name) in enumerate(reversed(st.session_state.gallery[-24:])):
            with cols[idx % 6]:
                st.image(data, use_column_width=True, caption=name)
    else:
        st.caption("올려진 사진이 없습니다.")

# ======================================================
# 페이지 2: 장례식 스트리밍
# ======================================================

def render_page2():
    st.markdown("<div class='kicker'>Streaming</div>", unsafe_allow_html=True)
    st.markdown("<div class='h1'>장례식 실시간 스트리밍</div>", unsafe_allow_html=True)
    st.caption("YouTube Live/Zoom/RTMP 등 임베드 링크를 연결하세요.")

    with st.container(border=True):
        url = st.text_input("스트리밍 링크(YouTube/동영상 URL)", placeholder="https://www.youtube.com/watch?v=...")
        if url:
            st.video(url)
        else:
            st.info("아직 스트리밍 링크가 없습니다. 링크를 입력하면 플레이어가 표시됩니다.")

    st.divider()
    with st.expander("참여 안내 텍스트(옵션)"):
        st.write("일시: 0000-00-00 00:00 | 접속 방법: 링크 클릭 → 플레이 ▶︎")

# ======================================================
# 페이지 3: 조의금 기부 / 꽃바구니
# ======================================================

def render_page3():
    st.markdown("<div class='kicker'>Condolence</div>", unsafe_allow_html=True)
    st.markdown("<div class='h1'>조의 · 헌화 참여</div>", unsafe_allow_html=True)
    st.caption("초기에는 간단한 안내 위주로, 추후 결제/주문 연동을 추가합니다.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("조의금 기부")
        with st.container(border=True):
            bank = st.text_input("계좌 안내 텍스트", value="카카오뱅크 3333-00-000000 (예금주 무지개다리)")
            st.write("\n")
            st.write("**QR/결제 연동(추후)** 카카오페이/토스 결제 버튼으로 확장 가능")
            st.code(bank, language="text")
            st.button("계좌 복사", type="secondary")

    with col2:
        st.subheader("꽃바구니 주문")
        with st.container(border=True):
            st.write("제휴 꽃집 연결 또는 문의 버튼으로 시작합니다.")
            st.text_input("문의 전화번호", value="010-0000-0000")
            st.text_area("간단한 요청사항 안내문", value="예: 화이트/아이보리 위주, 리본 문구 '평안히 쉬어요' 등")
            st.button("전화 걸기 / 카톡 문의", type="primary")

    st.divider()
    with st.expander("개인정보/결제 관련 주의(표준 안내문 예시)"):
        st.write("직접 이체 시 송금 전 계좌번호 재확인을 권장합니다. 결제 연동 도입 전까지는 개인정보 최소 수집 원칙을 따르고, 문의 시 필수 정보 외 입력을 요구하지 않습니다.")

# ===================== 라우팅 =====================
if page == "추모 공간":
    render_page1()
elif page == "장례식 스트리밍":
    render_page2()
else:
    render_page3()
