# 라이브러리

import streamlit as st
from streamlit_folium import folium_static
import folium

from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

import openrouteservice
from openrouteservice import convert




# 사이드바

st.sidebar.header("공원특성 입력")
# 변수 1
my_select_X = st.sidebar.selectbox("누구와 함께 가나요?", ["혼자", "친구", "가족(아이 포함)", "반려견", "부모님", "동아리원"])

# 변수 2
my_select_Y = st.sidebar.multiselect("어떤 목적으로 가나요?(중복 선택 가능)", ["산책", "운동", "피크닉", "구기 운동", "놀이터", "정자", "벤치"])

# 변수 3 _ ver 1
my_select_Z = st.sidebar.selectbox("얼마나 머물 수 있나요?", ["1시간 이내", "1~2시간", "2~3시간", "3시간 이상"])


my_select_a = st.sidebar.selectbox("어떻게 가실건가요?", ["도보", "버스", "자차"])

# 변수 3 _ ver 2
# my_select_Z = st.sidebar.slider("얼마나 머물 수 있나요? (시간)", min_value = 1, max_value = 6, value = 6)


# 메인

st.title("당신에게 맞는 공원 추천")

st.write("")
st.write("")

# 현재 위치정보 파악 (외부소스)
loc_button = Button(label="내 위치 기반 공원 추천 받기")

loc_button.js_on_event("button_click", CustomJS(code="""
    navigator.geolocation.getCurrentPosition(
        (loc) => {
            document.dispatchEvent(new CustomEvent("GET_LOCATION", {detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}}))
        }
    )
    """))
result = streamlit_bokeh_events(
    loc_button,
    events="GET_LOCATION",
    key="get_location",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_LOCATION" in result:

        a = float(result.get("GET_LOCATION")['lat']) # 위도
        b = float(result.get("GET_LOCATION")['lon']) # 경도

        print(a, b)

        st.header("공원 정보")

        st.write("")
        st.write("공원 이름 : 광주 시민의 숲")
        st.write("공원 정보 : [list]")
        st.write("공원 시설 : [list]")
        st.write("기타 정보 : [list]")
        st.write("공원 사진 : <사진이 있으면 좋지 않을까요?(스크래핑?)>") # 고민

        st.write("")
        st.write("")
        # 공원 위치 정보 및 루트 확인

        st.header("공원 위치")
        st.write("")

        client = openrouteservice.Client(key='5b3ce3597851110001cf624859867a29ba314369ba8af6b9e41dd880')

        coords = ((b, a), (126.8687814, 35.2370841))  # b,a(현재위치) - 추천되는 공원의 위치


        res = client.directions(coords)

        geometry = client.directions(coords)['routes'][0]['geometry']
        decoded = convert.decode_polyline(geometry)

        distance_txt = "<h5> <b>거리 :&nbsp" + "<strong>" + str(
            round(res['routes'][0]['summary']['distance'] / 1000, 1)) + " Km </strong>" + "</h5></b>"



        m = folium.Map(location=[35.2370841, 126.8687814], zoom_start=15, control_scale=True, # 추천되는 공원의 위치
                       tiles="openstreetmap")
        folium.GeoJson(decoded).add_child(folium.Popup(distance_txt, max_width=500)).add_to(m)


        folium.Marker(
            location=list(coords[0][::-1]),
            popup="your location",
            icon=folium.Icon(color="green"),
        ).add_to(m)

        folium.Marker(
            location=list(coords[1][::-1]),
            popup="park location",
            icon=folium.Icon(color="red"),
        ).add_to(m)

        folium_static(m)

        st.write("")
        st.write("")


        # 추천 공원
        c = 35.2370841
        d = 126.8687814

        st.header("공원 길 찾기(링크)")
        st.write("")
        st.write("네이버 : 안되는것 같은디?")
        st.write("카카오 : https://map.kakao.com/link/to/park,{},{}".format(c,d))



        # st.header("공원 정보")
        #
        # st.write("공원 이름 : 광주 시민의 숲")
        # st.write("공원 정보 : [list]")
        # st.write("공원 시설 : [list]")
        #
        # st.header("공원 위치")
        #
        # # center on Liberty Bell
        # m = folium.Map(location=[35.22835136646543, 126.86179035625973], zoom_start=16)
        #
        # # add marker for Liberty Bell
        # tooltip = "Liberty Bell"
        # folium.Marker(
        # [35.22835136646543, 126.86179035625973], popup="Liberty Bell", tooltip=tooltip
        # ).add_to(m)
        #
        # # call to render Folium map in Streamlit
        # folium_static(m)