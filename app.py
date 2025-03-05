import random
import streamlit as st
from yt_extractor import get_info
import database_service as dbs

# Cache workout data retrieval
@st.cache_resource
def get_workouts():
    return dbs.get_all_workouts()

# Convert duration from seconds to HH:MM:SS or MM:SS format
def get_duration_text(duration_s):
    seconds = duration_s % 60
    minutes = int((duration_s / 60) % 60)
    hours = int((duration_s / (60 * 60)) % 24)
    
    if hours > 0:
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    return f'{minutes:02d}:{seconds:02d}'

# Streamlit UI
st.title("🏋️‍♂️ Workout APP")

menu_options = ("Today's workout", "All workouts", "Add workout")
selection = st.sidebar.selectbox("Menu", menu_options)

# Display all workouts
if selection == "All workouts":
    st.markdown("## 📋 All Workouts")

    workouts = get_workouts()
    if workouts:
        for wo in workouts:
            url = f"https://youtu.be/{wo['video_id']}"
            st.text(f"📌 {wo['title']}")
            st.text(f"🎥 {wo['channel']} - ⏱ {get_duration_text(wo['duration'])}")
            st.video(url)

            if st.button('🗑 Delete workout', key=wo["video_id"]):
                dbs.delete_workout(wo["video_id"])
                st.cache_resource.clear()  # Clear cached data properly
                st.rerun()  # Rerun Streamlit app
    else:
        st.text("❌ No workouts in Database!")

# Add a new workout
elif selection == "Add workout":
    st.markdown("## ➕ Add Workout")

    url = st.text_input('🔗 Enter the YouTube video URL')

    if url:
        workout_data = get_info(url)  # Extract workout data

        if workout_data is None:
            st.text("⚠️ Could not find video. Please check the URL.")
        else:
            st.text(f"🎬 Title: {workout_data.get('title', 'Unknown')}")
            st.text(f"📺 Channel: {workout_data.get('channel', 'Unknown')}")
            st.video(url)

            if st.button("✅ Add Workout"):
                dbs.insert_workout(workout_data)
                st.success("Workout Added Successfully! ✅")
                st.cache_resource.clear()

# Display today's workout
else:
    st.markdown("## 🎯 Today's Workout")

    workouts = get_workouts()

    if not workouts:
        st.text("❌ No workouts in Database!")
    else:
        wo = dbs.get_workout_today()

        if not wo:
            idx = random.randint(0, len(workouts) - 1)
            wo = workouts[idx]
            dbs.update_workout_today(wo, insert=True)
        else:
            wo = wo[0]

        if st.button("🔄 Choose Another Workout"):
            idx = random.randint(0, len(workouts) - 1)
            wo_new = workouts[idx]

            while wo_new['video_id'] == wo['video_id']:  # Avoid selecting the same workout
                idx = random.randint(0, len(workouts) - 1)
                wo_new = workouts[idx]

            wo = wo_new
            dbs.update_workout_today(wo)

        url = f"https://youtu.be/{wo['video_id']}"
        st.text(f"📌 {wo['title']}")
        st.text(f"🎥 {wo['channel']} - ⏱ {get_duration_text(wo['duration'])}")
        st.video(url)
