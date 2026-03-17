# 📅 College Timetable Management System

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)

> A web-based application for managing college class timetables with secure admin login and real-time data management.

---

## 🌐 Live Demo

[![Live Demo](https://img.shields.io/badge/🗓️_Live_Demo-FF4B4B?style=for-the-badge)](https://huggingface.co/spaces/SiddXiao/Time_Table_Management_System)

---

## ✨ Features

- 📌 Add, update, and delete timetable entries
- 🔐 Secure admin authentication
- 📊 Real-time data with MongoDB Atlas
- 📤 Export timetable data
- 🖥️ Clean and interactive UI with Streamlit

---

## 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python | Backend Logic |
| Streamlit | Frontend UI |
| MongoDB Atlas | Cloud Database |
| pymongo | Database Connection |

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install streamlit pymongo dnspython
```

### Setup
1. Clone the repository
```bash
git clone https://github.com/SIDDXIAO/Time_Table_Management_System.git
cd Time_Table_Management_System
```

2. Add your MongoDB URI in `.env`
```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

3. Run the app
```bash
streamlit run time_proj.py
```

---

## 📁 Project Structure
```
Time_Table_Management_System/
│
├── time_proj.py        # Main Streamlit app
├── mongdb.py           # MongoDB connection
├── requirements.txt    # Dependencies
└── README.md           # Project documentation
```

---

## 👨‍💻 Developer

**Siddhant Kumar Patel**  
BCA Student — AI & Data Science  
Babu Banarasi Das University, Lucknow

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/siddhant-kumar-patel-521239324)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/SIDDXIAO)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
