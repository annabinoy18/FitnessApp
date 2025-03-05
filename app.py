import streamlit as st
from database_service import add_user, check_user, get_all_workouts, insert_workout, delete_workout, get_workout_today, update_workout_today
from yt_extractor import get_info
import random

# Initialize session state for authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Convert duration from seconds to MM:SS or HH:MM:SS format
def get_duration_text(duration_s):
    seconds = duration_s % 60
    minutes = (duration_s // 60) % 60
    hours = duration_s // 3600
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours > 0 else f"{minutes:02d}:{seconds:02d}"

# **SIGNUP PAGE**
def signup_page():
    st.title("🔑 Sign Up to Fitness App")
    email = st.text_input("📧 Enter your Email:")
    password = st.text_input("🔒 Enter Password:", type="password")

    if st.button("✅ Sign Up"):
        if email and password:
            if add_user(email, password):
                st.success("🎉 Signup successful! Please Sign In.")
                st.rerun()
            else:
                st.error("❌ Email already registered!")
        else:
            st.error("⚠️ Please enter valid credentials!")

# **SIGN-IN PAGE**
def signin_page():
    st.title("🔑 Sign In to Fitness App")
    email = st.text_input("📧 Enter your Email:")
    password = st.text_input("🔒 Enter Password:", type="password")

    if st.button("🔓 Sign In"):
        if email and password:
            if check_user(email, password):
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid email or password!")
        else:
            st.error("⚠️ Please enter valid credentials!")

# **MAIN APP PAGE**
def main_app():
    st.title("🏋️‍♂️ Workout App")

    menu_options = ("Today's workout", "All workouts", "Add workout", "Logout")
    selection = st.sidebar.selectbox("📌 Menu", menu_options)

    if selection == "Logout":
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.rerun()

    elif selection == "All workouts":
        st.markdown("## 📋 All Workouts")
        workouts = get_all_workouts()

        if workouts:
            for wo in workouts:
                url = f"https://youtu.be/{wo['video_id']}"
                st.text(f"📌 {wo['title']}")
                st.text(f"🎥 {wo['channel']} - ⏱ {get_duration_text(wo['duration'])}")
                st.video(url)

                if st.button('🗑 Delete workout', key=wo["video_id"]):
                    delete_workout(wo["video_id"])
                    st.rerun()
        else:
            st.text("❌ No workouts in Database!")

    elif selection == "Add workout":
        st.markdown("## ➕ Add Workout")
        url = st.text_input('🔗 Enter the YouTube video URL')

        if url:
            workout_data = get_info(url)
            if workout_data is None:
                st.text("⚠️ Could not find video. Please check the URL.")
            else:
                st.text(f"🎬 Title: {workout_data.get('title', 'Unknown')}")
                st.text(f"📺 Channel: {workout_data.get('channel', 'Unknown')}")
                st.video(url)

                if st.button("✅ Add Workout"):
                    insert_workout(workout_data)
                    st.success("Workout Added Successfully! ✅")
                    st.rerun()

    else:  # "Today's workout"
        st.markdown("## 🎯 Today's Workout")
        workouts = get_all_workouts()

        if not workouts:
            st.text("❌ No workouts in Database!")
        else:
            wo = get_workout_today()
            if not wo:
                wo = random.choice(workouts)
                update_workout_today(wo, insert=True)
            else:
                wo = wo[0]

            if st.button("🔄 Choose Another Workout"):
                new_wo = random.choice([w for w in workouts if w["video_id"] != wo["video_id"]])
                update_workout_today(new_wo)
                st.rerun()

            url = f"https://youtu.be/{wo['video_id']}"
            st.text(f"📌 {wo['title']}")
            st.text(f"🎥 {wo['channel']} - ⏱ {get_duration_text(wo['duration'])}")
            st.video(url)

# **SHOW SIGNUP OR SIGNIN PAGE IF NOT LOGGED IN**
if not st.session_state.logged_in:
    choice = st.radio("👤 Select an option:", ["Sign In", "Sign Up"])
    if choice == "Sign In":
        signin_page()
    else:
        signup_page()
else:
    main_app()
