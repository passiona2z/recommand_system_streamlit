import streamlit as st

st.sidebar.header("공원특성 입력")
# 변수 1
my_select_X = st.sidebar.selectbox("누구와 함께 가나요?", ["혼자", "친구", "가족(아이 포함)", "부모님", "동아리", "반려견"])

# 변수 2
my_select_Y = st.sidebar.selectbox("어떤 목적으로 가나요?", ["산책", "달리기", "피크닉", "구기 운동", "놀이터", "정자"])

# 변수 3
my_select_Y_2 = st.sidebar.multiselect("어떤 목적으로 가나요?(중복 선택 가능)", ["산책", "달리기", "피크닉", "구기 운동", "놀이터", "정자"])

# 변수 3
my_select_Z = st.sidebar.selectbox("얼마나 머물 수 있나요?", ["30분", "1~2시간", "2~3시간", "3시간 이상"])



st.title("당신에게 맞는 공원 추천")

