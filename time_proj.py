import streamlit as st
import pandas as pd
import json
from datetime import datetime, time
import hashlib
import os
import mongdb

st.set_page_config(
    page_title="College Timetable Management System",
    page_icon="📅",
    layout="wide"
)


DATA_DIR = "timetable_data"
GROUPS_FILE = os.path.join(DATA_DIR, "groups.csv")
SUBJECTS_FILE = os.path.join(DATA_DIR, "subjects.csv")
TEACHERS_FILE = os.path.join(DATA_DIR, "teachers.csv")
ROOMS_FILE = os.path.join(DATA_DIR, "rooms.csv")
TIMETABLE_FILE = os.path.join(DATA_DIR, "timetables.csv")


os.makedirs(DATA_DIR, exist_ok=True)

ADMIN_CREDENTIALS = {
    'admin': 'admin123',
    'principal': 'principal456'
}


TIME_SLOTS = [
    "09:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-1:00",
    "1:00-2:00", "2:00-3:00", "3:00-4:00", "4:00-5:00"
]

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    return username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password


def load_groups():
    """Load groups from CSV file"""
    try:
        if os.path.exists(GROUPS_FILE):
            return pd.read_csv(GROUPS_FILE)
        else:
            return pd.DataFrame(columns=['group_name', 'department', 'semester', 'student_count', 'created_date'])
    except Exception as e:
        st.error(f"Error loading groups: {e}")
        return pd.DataFrame(columns=['group_name', 'department', 'semester', 'student_count', 'created_date'])

def save_groups(df):
    """Save groups to CSV file"""
    try:
        df.to_csv(GROUPS_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving groups: {e}")
        return False

def load_subjects():
    """Load subjects from CSV file"""
    try:
        if os.path.exists(SUBJECTS_FILE):
            return pd.read_csv(SUBJECTS_FILE)
        else:
            return pd.DataFrame(columns=['subject_code', 'subject_name', 'subject_type', 'department'])
    except Exception as e:
        st.error(f"Error loading subjects: {e}")
        return pd.DataFrame(columns=['subject_code', 'subject_name', 'subject_type', 'department'])

def save_subjects(df):
    """Save subjects to CSV file"""
    try:
        df.to_csv(SUBJECTS_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving subjects: {e}")
        return False

def load_teachers():
    """Load teachers from CSV file"""
    try:
        if os.path.exists(TEACHERS_FILE):
            return pd.read_csv(TEACHERS_FILE)
        else:
            return pd.DataFrame(columns=['teacher_id', 'teacher_name', 'department', 'email', 'phone'])
    except Exception as e:
        st.error(f"Error loading teachers: {e}")
        return pd.DataFrame(columns=['teacher_id', 'teacher_name', 'department', 'email', 'phone'])

def save_teachers(df):
    """Save teachers to CSV file"""
    try:
        df.to_csv(TEACHERS_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving teachers: {e}")
        return False

def load_rooms():
    """Load rooms from CSV file"""
    try:
        if os.path.exists(ROOMS_FILE):
            return pd.read_csv(ROOMS_FILE)
        else:
            return pd.DataFrame(columns=['room_number', 'room_type', 'capacity', 'building', 'equipment'])
    except Exception as e:
        st.error(f"Error loading rooms: {e}")
        return pd.DataFrame(columns=['room_number', 'room_type', 'capacity', 'building', 'equipment'])

def save_rooms(df):
    """Save rooms to CSV file"""
    try:
        df.to_csv(ROOMS_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving rooms: {e}")
        return False

def load_timetables():
    """Load timetables from CSV file"""
    try:
        if os.path.exists(TIMETABLE_FILE):
            return pd.read_csv(TIMETABLE_FILE)
        else:
            return pd.DataFrame(columns=['group_name', 'day', 'time_slot', 'subject_code', 'teacher_id', 'room_number'])
    except Exception as e:
        st.error(f"Error loading timetables: {e}")
        return pd.DataFrame(columns=['group_name', 'day', 'time_slot', 'subject_code', 'teacher_id', 'room_number'])

def save_timetables(df):
    """Save timetables to CSV file"""
    try:
        df.to_csv(TIMETABLE_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving timetables: {e}")
        return False

def login_page():
    st.title("🏫 College Timetable Management System")
    st.subheader("Administrator Login")
    
   
    st.info("""
    **Demo Credentials:**
    - Username: `admin` | Password: `admin123`
    - Username: `principal` | Password: `principal456`
    """)
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if username and password: 
                if authenticate_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials! Please check username and password.")
            else:
                st.error("Please enter both username and password.")
    
   
    with st.expander("Need Help?"):
        st.write("""
        **For testing purposes, use:**
        - Username: admin, Password: admin123
        - Username: principal, Password: principal456
        
        Make sure there are no extra spaces in your input.
        """)

def sidebar_navigation():
    st.sidebar.title(f"Welcome, {st.session_state.username}!")
    st.sidebar.markdown("---")
    
    menu_options = [
        "📊 Dashboard",
        "📅 View Timetables",
        "➕ Create/Edit Timetable", 
        "👥 Manage Groups",
        "📚 Manage Subjects",
        "👨‍🏫 Manage Teachers",
        "🏢 Manage Rooms",
        "📋 Data Tables",
        "🔧 System Settings"
    ]
    
    
    selected = st.sidebar.radio("Navigation", menu_options, index=0)
    
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()
    
    return selected

def dashboard():
    st.header("📊 System Dashboard")
    
   
    groups_df = load_groups()
    subjects_df = load_subjects()
    teachers_df = load_teachers()
    rooms_df = load_rooms()
    timetables_df = load_timetables()
    

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Groups", len(groups_df))
    with col2:
        st.metric("Total Subjects", len(subjects_df))
    with col3:
        st.metric("Total Teachers", len(teachers_df))
    with col4:
        st.metric("Total Rooms", len(rooms_df))
    
    st.markdown("---")
    
   
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Groups by Department")
        if not groups_df.empty:
            dept_counts = groups_df['department'].value_counts()
            st.bar_chart(dept_counts)
        else:
            st.info("No groups data available")
    
    with col2:
        st.subheader("Room Types Distribution")
        if not rooms_df.empty:
            room_counts = rooms_df['room_type'].value_counts()
            st.bar_chart(room_counts)
        else:
            st.info("No rooms data available")

def manage_groups():
    st.header("👥 Group Management")
    
  
    groups_df = load_groups()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add New Group")
        with st.form("add_group"):
            group_name = st.text_input("Group Name (e.g., CS-1A, EE-2B)")
            department = st.selectbox("Department", 
                ["Computer Science", "Electrical Engineering", "Mechanical Engineering", 
                 "Civil Engineering", "Electronics", "Information Technology"])
            semester = st.selectbox("Semester", list(range(1, 9)))
            student_count = st.number_input("Number of Students", min_value=1, value=30)
            
            if st.form_submit_button("Add Group"):
                if group_name:
                    
                    if not groups_df.empty and group_name in groups_df['group_name'].values:
                        st.error("Group already exists!")
                    else:
                        new_group = pd.DataFrame({
                            'group_name': [group_name],
                            'department': [department],
                            'semester': [semester],
                            'student_count': [student_count],
                            'created_date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                        })
                        
                        groups_df = pd.concat([groups_df, new_group], ignore_index=True)
                        
                        if save_groups(groups_df):
                            st.success(f"Group '{group_name}' added successfully!")
                            st.rerun()
    
    with col2:
        st.subheader("Existing Groups")
        if not groups_df.empty:
           
            for index, row in groups_df.iterrows():
                with st.expander(f"📋 {row['group_name']} ({row['department']})"):
                    st.write(f"**Department:** {row['department']}")
                    st.write(f"**Semester:** {row['semester']}")
                    st.write(f"**Students:** {row['student_count']}")
                    st.write(f"**Created:** {row['created_date']}")
                    
                    if st.button(f"Delete {row['group_name']}", key=f"del_group_{index}"):
                      
                        groups_df = groups_df.drop(index).reset_index(drop=True)
                        
                       
                        timetables_df = load_timetables()
                        if not timetables_df.empty:
                            timetables_df = timetables_df[timetables_df['group_name'] != row['group_name']]
                            save_timetables(timetables_df)
                        
                        if save_groups(groups_df):
                            st.success(f"Group '{row['group_name']}' deleted!")
                            st.rerun()
            
           
            csv = groups_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Groups Data",
                data=csv,
                file_name="groups_data.csv",
                mime="text/csv"
            )
        else:
            st.info("No groups created yet.")

def manage_subjects():
    st.header("📚 Subject Management")
    
    subjects_df = load_subjects()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add New Subject")
        with st.form("add_subject"):
            subject_code = st.text_input("Subject Code (e.g., CS101)")
            subject_name = st.text_input("Subject Name")
            subject_type = st.selectbox("Type", ["Theory", "Practical", "Tutorial"])
            department = st.selectbox("Department", 
                ["Computer Science", "Electrical Engineering", "Mechanical Engineering", 
                 "Civil Engineering", "Electronics", "Information Technology"])
            
            if st.form_submit_button("Add Subject"):
                if subject_code and subject_name:
                   
                    if not subjects_df.empty and subject_code in subjects_df['subject_code'].values:
                        st.error("Subject code already exists!")
                    else:
                        new_subject = pd.DataFrame({
                            'subject_code': [subject_code],
                            'subject_name': [subject_name],
                            'subject_type': [subject_type],
                            'department': [department]
                        })
                        
                        subjects_df = pd.concat([subjects_df, new_subject], ignore_index=True)
                        
                        if save_subjects(subjects_df):
                            st.success("Subject added successfully!")
                            st.rerun()
    
    with col2:
        st.subheader("Existing Subjects")
        if not subjects_df.empty:
           
            st.dataframe(
                subjects_df,
                use_container_width=True,
                hide_index=True
            )
            
           
            if len(subjects_df) > 0:
                subject_to_delete = st.selectbox(
                    "Select subject to delete:", 
                    subjects_df['subject_code'].tolist()
                )
                
                if st.button("Delete Selected Subject"):
                    subjects_df = subjects_df[subjects_df['subject_code'] != subject_to_delete]
                    if save_subjects(subjects_df):
                        st.success(f"Subject '{subject_to_delete}' deleted!")
                        st.rerun()
            
            
            csv = subjects_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Subjects Data",
                data=csv,
                file_name="subjects_data.csv",
                mime="text/csv"
            )
        else:
            st.info("No subjects created yet.")

def manage_teachers():
    st.header("👨‍🏫 Teacher Management")
    
    teachers_df = load_teachers()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add New Teacher")
        with st.form("add_teacher"):
            teacher_id = st.text_input("Teacher ID")
            teacher_name = st.text_input("Teacher Name")
            department = st.selectbox("Department", 
                ["Computer Science", "Electrical Engineering", "Mechanical Engineering", 
                 "Civil Engineering", "Electronics", "Information Technology"])
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            
            if st.form_submit_button("Add Teacher"):
                if teacher_id and teacher_name:
                   
                    if not teachers_df.empty and teacher_id in teachers_df['teacher_id'].values:
                        st.error("Teacher ID already exists!")
                    else:
                        new_teacher = pd.DataFrame({
                            'teacher_id': [teacher_id],
                            'teacher_name': [teacher_name],
                            'department': [department],
                            'email': [email],
                            'phone': [phone]
                        })
                        
                        teachers_df = pd.concat([teachers_df, new_teacher], ignore_index=True)
                        
                        if save_teachers(teachers_df):
                            st.success("Teacher added successfully!")
                            st.rerun()
    
    with col2:
        st.subheader("Existing Teachers")
        if not teachers_df.empty:
            st.dataframe(
                teachers_df,
                use_container_width=True,
                hide_index=True
            )
            
          
            if len(teachers_df) > 0:
                teacher_to_delete = st.selectbox(
                    "Select teacher to delete:", 
                    teachers_df['teacher_id'].tolist()
                )
                
                if st.button("Delete Selected Teacher"):
                    teachers_df = teachers_df[teachers_df['teacher_id'] != teacher_to_delete]
                    if save_teachers(teachers_df):
                        st.success(f"Teacher '{teacher_to_delete}' deleted!")
                        st.rerun()
            
           
            csv = teachers_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Teachers Data",
                data=csv,
                file_name="teachers_data.csv",
                mime="text/csv"
            )
        else:
            st.info("No teachers added yet.")

def manage_rooms():
    st.header("🏢 Room Management")
    
    rooms_df = load_rooms()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add New Room")
        with st.form("add_room"):
            room_number = st.text_input("Room Number")
            room_type = st.selectbox("Room Type", ["Lecture Hall", "Laboratory", "Tutorial Room", "Auditorium"])
            capacity = st.number_input("Capacity", min_value=1, value=50)

            # 🔹 Department options from existing data
            existing_departments = rooms_df['department'].dropna().unique().tolist() if not rooms_df.empty and 'department' in rooms_df.columns else []
            department = st.selectbox("Select Department", ["Computer Science", "Electrical Engineering", "Mechanical Engineering", 
                 "Civil Engineering", "Electronics", "Information Technology"] + existing_departments)

            # 🔹 If user selects new department, show text input
            new_department = ""
            if department == "--New Department--":
                new_department = st.text_input("Enter New Department Name")

            equipment = st.text_area("Equipment/Facilities")
            
            if st.form_submit_button("Add Room"):
                if room_number:
                    # Final department value
                    final_department = new_department if department == "--New Department--" else department

                    # If department column doesn't exist in dataframe, create it
                    if 'department' not in rooms_df.columns:
                        rooms_df['department'] = None

                    if not rooms_df.empty and room_number in rooms_df['room_number'].values:
                        st.error("Room number already exists!")
                    else:
                        new_room = pd.DataFrame({
                            'room_number': [room_number],
                            'room_type': [room_type],
                            'capacity': [capacity],
                            'department': [final_department],
                            'equipment': [equipment]
                        })
                        
                        rooms_df = pd.concat([rooms_df, new_room], ignore_index=True)
                        
                        if save_rooms(rooms_df):
                            st.success("Room added successfully!")
                            st.rerun()
    
    with col2:
        st.subheader("Existing Rooms")
        if not rooms_df.empty:
            st.dataframe(
                rooms_df,
                use_container_width=True,
                hide_index=True
            )
            
            if len(rooms_df) > 0:
                room_to_delete = st.selectbox(
                    "Select room to delete:", 
                    rooms_df['room_number'].tolist()
                )
                
                if st.button("Delete Selected Room"):
                    rooms_df = rooms_df[rooms_df['room_number'] != room_to_delete]
                    if save_rooms(rooms_df):
                        st.success(f"Room '{room_to_delete}' deleted!")
                        st.rerun()
            
            csv = rooms_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Rooms Data",
                data=csv,
                file_name="rooms_data.csv",
                mime="text/csv"
            )
        else:
            st.info("No rooms added yet.")


def create_edit_timetable():
    st.header("📅 Create/Edit Timetable")
    
   
    groups_df = load_groups()
    subjects_df = load_subjects()
    teachers_df = load_teachers()
    rooms_df = load_rooms()
    timetables_df = load_timetables()
    
    if groups_df.empty:
        st.warning("Please create groups first before creating timetables.")
        return
    
    selected_group = st.selectbox("Select Group", groups_df['group_name'].tolist())
    
    # Get lists of IDs/Names for dropdowns
    subject_code_options = [""] + subjects_df['subject_code'].tolist()
    teacher_id_options = [""] + teachers_df['teacher_id'].tolist()
    room_number_options = [""] + rooms_df['room_number'].tolist()
    
    
    if selected_group:
        st.subheader(f"Timetable for {selected_group}")
        
        
        day_tabs = st.tabs(DAYS)
        
        for i, day in enumerate(DAYS):
            with day_tabs[i]:
                st.subheader(f"{day} Schedule")
                
                
                existing_schedule = timetables_df[
                    (timetables_df['group_name'] == selected_group) & 
                    (timetables_df['day'] == day)
                ]
                
                for slot in TIME_SLOTS:
                    with st.expander(f"⏰ {slot}", expanded=False):
                        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                        
                      
                        current_entry = existing_schedule[existing_schedule['time_slot'] == slot]

                        # **FIX:** timetables_df only has 'subject_code', not 'subject_name'.
                        current_subject_code = current_entry['subject_code'].iloc[0] if not current_entry.empty else ""
                        current_teacher = current_entry['teacher_id'].iloc[0] if not current_entry.empty else ""
                        current_room = current_entry['room_number'].iloc[0] if not current_entry.empty else ""
                        
                        with col1:
                            # Use subject_code for the selection
                            subject_index = subject_code_options.index(current_subject_code) if current_subject_code in subject_code_options else 0
                            subject = st.selectbox(
                                "Subject Code", # Changed label for clarity
                                subject_code_options,
                                index=subject_index,
                                key=f"subj_{day}_{slot}"
                            )
                        
                        with col2:
                            teacher_index = teacher_id_options.index(current_teacher) if current_teacher in teacher_id_options else 0
                            teacher = st.selectbox(
                                "Teacher ID", # Changed label for clarity
                                teacher_id_options,
                                index=teacher_index,
                                key=f"teach_{day}_{slot}"
                            )
                        
                        with col3:
                            room_index = room_number_options.index(current_room) if current_room in room_number_options else 0
                            room = st.selectbox(
                                "Room Number", # Changed label for clarity
                                room_number_options,
                                index=room_index,
                                key=f"room_{day}_{slot}"
                            )
                        
                        with col4:
                            if st.button("Save", key=f"save_{day}_{slot}"):
                               
                                timetables_df = timetables_df[
                                    ~((timetables_df['group_name'] == selected_group) & 
                                      (timetables_df['day'] == day) & 
                                      (timetables_df['time_slot'] == slot))
                                ]
                                
                                
                                if subject: # 'subject' now holds the subject_code
                                    new_entry = pd.DataFrame({
                                        'group_name': [selected_group],
                                        'day': [day],
                                        'time_slot': [slot],
                                        'subject_code': [subject], # Save the subject code
                                        'teacher_id': [teacher],
                                        'room_number': [room]
                                    })
                                    
                                    timetables_df = pd.concat([timetables_df, new_entry], ignore_index=True)
                                
                                if save_timetables(timetables_df):
                                    st.success("Saved!")
                                    st.rerun()

def view_timetables():
    st.header("📅 View Timetables")
    
  
    groups_df = load_groups()
    subjects_df = load_subjects()
    teachers_df = load_teachers()
    rooms_df = load_rooms()
    timetables_df = load_timetables()
    
    if timetables_df.empty:
        st.info("No timetables created yet.")
        return
    
    selected_group = st.selectbox("Select Group to View", timetables_df['group_name'].unique())
    
    if selected_group:
        st.subheader(f"Timetable for {selected_group}")
        
       
        group_timetable = timetables_df[timetables_df['group_name'] == selected_group].copy()
        
        if not group_timetable.empty:
           
            if not subjects_df.empty:
                group_timetable = group_timetable.merge(
                    subjects_df[['subject_code', 'subject_name']], 
                    on='subject_code', 
                    how='left'
                )
            
            if not teachers_df.empty:
                group_timetable = group_timetable.merge(
                    teachers_df[['teacher_id', 'teacher_name']], 
                    on='teacher_id', 
                    how='left'
                )
            
         
            display_columns = ['day', 'time_slot', 'subject_code', 'subject_name', 'teacher_id', 'teacher_name', 'room_number']
            available_columns = [col for col in display_columns if col in group_timetable.columns]
            
            st.dataframe(
                group_timetable[available_columns].sort_values(['day', 'time_slot']),
                use_container_width=True,
                hide_index=True
            )
            
            
            csv = group_timetable[available_columns].to_csv(index=False)
            st.download_button(
                label="📥 Download Timetable",
                data=csv,
                file_name=f"{selected_group}_timetable.csv",
                mime="text/csv"
            )
        else:
            st.info("No classes scheduled for this group yet.")

def data_tables():
    st.header("📋 Data Tables")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Groups", "Subjects", "Teachers", "Rooms", "Timetables"])
    
    with tab1:
        st.subheader("Groups Table")
        groups_df = load_groups()
        if not groups_df.empty:
            st.dataframe(groups_df, use_container_width=True, hide_index=True)
        else:
            st.info("No groups data available")
    
    with tab2:
        st.subheader("Subjects Table")
        subjects_df = load_subjects()
        if not subjects_df.empty:
            st.dataframe(subjects_df, use_container_width=True, hide_index=True)
        else:
            st.info("No subjects data available")
    
    with tab3:
        st.subheader("Teachers Table")
        teachers_df = load_teachers()
        if not teachers_df.empty:
            st.dataframe(teachers_df, use_container_width=True, hide_index=True)
        else:
            st.info("No teachers data available")
    
    with tab4:
        st.subheader("Rooms Table")
        rooms_df = load_rooms()
        if not rooms_df.empty:
            st.dataframe(rooms_df, use_container_width=True, hide_index=True)
        else:
            st.info("No rooms data available")
    
    with tab5:
        st.subheader("Timetables Table")
        timetables_df = load_timetables()
        if not timetables_df.empty:
            st.dataframe(timetables_df, use_container_width=True, hide_index=True)
        else:
            st.info("No timetables data available")

def system_settings():
    st.header("🔧 System Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Data Export")
        
        
        if st.button("📤 Export Groups Data"):
            groups_df = load_groups()
            if not groups_df.empty:
                csv = groups_df.to_csv(index=False)
                st.download_button(
                    label="💾 Download Groups CSV",
                    data=csv,
                    file_name="groups_export.csv",
                    mime="text/csv"
                )
        
        if st.button("📤 Export All Data"):
           
            import zipfile
            import io
            
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
               
                tables = {
                    'groups.csv': load_groups(),
                    'subjects.csv': load_subjects(),
                    'teachers.csv': load_teachers(),
                    'rooms.csv': load_rooms(),
                    'timetables.csv': load_timetables()
                }
                
                for filename, df in tables.items():
                    if not df.empty:
                        csv_data = df.to_csv(index=False)
                        zip_file.writestr(filename, csv_data)
            
            st.download_button(
                label="💾 Download All Data (ZIP)",
                data=zip_buffer.getvalue(),
                file_name="timetable_system_data.zip",
                mime="application/zip"
            )
    
    with col2:
        st.subheader("System Statistics")
        
        groups_df = load_groups()
        subjects_df = load_subjects()
        teachers_df = load_teachers()
        rooms_df = load_rooms()
        timetables_df = load_timetables()
        
        st.metric("Total Groups", len(groups_df))
        st.metric("Total Subjects", len(subjects_df))
        st.metric("Total Teachers", len(teachers_df))
        st.metric("Total Rooms", len(rooms_df))
        st.metric("Total Timetable Entries", len(timetables_df))
        
       
        st.subheader("Storage Information")
        st.info(f"Data stored in: {DATA_DIR}/")
        
       
        if st.button("🗑️ Clear All Data", type="secondary"):
            if st.session_state.get('confirm_clear', False):
              
                for file_path in [GROUPS_FILE, SUBJECTS_FILE, TEACHERS_FILE, ROOMS_FILE, TIMETABLE_FILE]:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                st.success("All data cleared!")
                st.session_state.confirm_clear = False
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("Click again to confirm clearing all data!")

def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        selected_page = sidebar_navigation()
        
        if selected_page == "📊 Dashboard":
            dashboard()
        elif selected_page == "📅 View Timetables":
            view_timetables()
        elif selected_page == "➕ Create/Edit Timetable":
            create_edit_timetable()
        elif selected_page == "👥 Manage Groups":
            manage_groups()
        elif selected_page == "📚 Manage Subjects":
            manage_subjects()
        elif selected_page == "👨‍🏫 Manage Teachers":
            manage_teachers()
        elif selected_page == "🏢 Manage Rooms":
            manage_rooms()
        elif selected_page == "📋 Data Tables":
            data_tables()
        elif selected_page == "🔧 System Settings":
            system_settings()

if __name__ == "__main__":
    main()