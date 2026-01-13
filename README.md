# 🧠 Dashboard Analisis Kesehatan Mental Gen Z (18-27 Tahun)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![PySpark](https://img.shields.io/badge/PySpark-3.0%2B-orange)](https://spark.apache.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Deskripsi Proyek

Dashboard interaktif berbasis **Streamlit** untuk menganalisis kesehatan mental karyawan **Generasi Z (18-27 tahun)** di tempat kerja. Proyek ini menggunakan **PySpark** untuk big data processing dan visualisasi interaktif untuk memberikan insights actionable kepada HR dan Management.

### 🎯 Tujuan Bisnis

- **Mengidentifikasi** faktor-faktor yang mempengaruhi kesehatan mental Gen Z
- **Membuat keputusan strategis** untuk meningkatkan employee well-being
- **Mengurangi turnover rate** akibat burnout
- **Meningkatkan produktivitas** dan kepuasan kerja
- **Mengoptimalkan ROI** dari program kesehatan mental

## 🌟 Fitur Utama

### 1. 📊 Overview Dashboard
- **Key Metrics**: Total karyawan, stress level, burnout score, risiko tinggi, kepuasan kerja
- **Visualisasi Distribusi**: Pie chart tingkat risiko, bar chart metrik mental health
- **Demografis**: Gender, usia, dan akses sumber daya mental health

### 2. 📈 Analisis Detail
- **Korelasi Faktor**: Heatmap correlation matrix
- **Work Hours Impact**: Scatter plot jam kerja vs stress
- **Manager Support**: Line chart pengaruh dukungan manager
- **Social Isolation**: Analysis untuk remote workers

### 3. 🏢 Analisis per Department
- **Perbandingan Metrik**: Stress, burnout, anxiety antar department
- **Distribusi Risiko**: Stacked bar chart risiko per department
- **Statistik Detail**: Table dengan gradient coloring

### 4. 🌍 Analisis per Lokasi Kerja
- **Remote vs Hybrid vs Onsite**: Perbandingan mental health metrics
- **Work-Life Balance**: Analysis kepuasan berdasarkan lokasi
- **Isolation Rating**: Special focus untuk remote workers

### 5. 💡 Insights & Rekomendasi
- **6 Key Findings**: Temuan utama dengan severity indicators
- **6 Strategic Recommendations**: Prioritas HIGH/MEDIUM/LOW
- **Business Outcomes**: Target dan timeline
- **ROI Calculator**: Interactive calculator untuk menghitung ROI program

## 🛠️ Tech Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Programming Language | 3.8+ |
| **PySpark** | Big Data Processing | 3.0+ |
| **Streamlit** | Dashboard Framework | 1.28+ |
| **Pandas** | Data Manipulation | 2.0+ |
| **Plotly** | Interactive Visualizations | 5.17+ |
| **NumPy** | Numerical Computing | 1.24+ |

## 📁 Struktur Proyek

```
mental-health-dashboard/
│
├── analysis_genz_filtered.ipynb    # Jupyter Notebook analisis PySpark
├── dashboard.py                     # Streamlit dashboard application
├── requirements.txt                 # Python dependencies
├── README.md                        # Dokumentasi proyek (file ini)
│
├── data/                            # Folder data (optional)
│   ├── genz_dashboard_data.csv     # Processed data untuk dashboard
│   └── genz_summary_stats.json     # Summary statistics
│
├── assets/                          # Folder untuk assets (optional)
│   └── images/                      # Screenshots dan images
│
└── docs/                            # Dokumentasi tambahan (optional)
    └── user_guide.md                # User guide lengkap
```

## 🚀 Instalasi dan Setup

### Prerequisites
- Python 3.8 atau lebih baru
- pip (Python package manager)
- Java 8 atau 11 (untuk PySpark)

### Step 1: Clone Repository
```bash
git clone https://github.com/username/mental-health-dashboard.git
cd mental-health-dashboard
```

### Step 2: Buat Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables (Optional)
```bash
# Buat file .env untuk konfigurasi
echo "SPARK_HOME=/path/to/spark" > .env
echo "JAVA_HOME=/path/to/java" >> .env
```

## 📊 Menjalankan Dashboard

### Opsi 1: Generate Data dan Jalankan Analisis PySpark
```bash
# Jalankan Jupyter Notebook untuk analisis dan generate data
jupyter notebook analysis_genz_filtered.ipynb

# Notebook akan menghasilkan:
# - genz_dashboard_data.csv
# - genz_summary_stats.json
```

### Opsi 2: Langsung Jalankan Dashboard (dengan sample data)
```bash
# Dashboard akan generate sample data otomatis jika file tidak ditemukan
streamlit run dashboard.py
```

### Opsi 3: Production Setup
```bash
# Dengan data real dari Kaggle
streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0
```

Dashboard akan terbuka di browser pada **http://localhost:8501**

## 🎨 Cara Menggunakan Dashboard

### 1. **Sidebar Filters**
   - Pilih rentang usia (18-27 tahun)
   - Filter berdasarkan gender
   - Pilih department spesifik
   - Filter lokasi kerja (Remote/Hybrid/Onsite)
   - Pilih tingkat risiko

### 2. **Tab Navigation**
   - **Overview**: Lihat ringkasan high-level metrics
   - **Analisis Detail**: Deep dive ke correlations dan patterns
   - **Per Department**: Compare metrics antar department
   - **Per Lokasi Kerja**: Analyze remote vs onsite impact
   - **Insights & Rekomendasi**: Strategic recommendations & ROI

### 3. **Interactive Elements**
   - Hover pada charts untuk detail data
   - Klik legend untuk hide/show series
   - Zoom dan pan pada scatter plots
   - Export charts sebagai PNG

## 📖 Data Schema

### Dataset: `genz_dashboard_data.csv`

| Column | Type | Description |
|--------|------|-------------|
| `Employee_ID` | int | Unique employee identifier |
| `Age` | int | Usia karyawan (18-27) |
| `Gender` | string | Male/Female/Non-binary |
| `Department` | string | Engineering/Marketing/Sales/HR/Finance/Design |
| `Work_Location` | string | Remote/Hybrid/Onsite |
| `Stress_Level` | int | Tingkat stress (1-10) |
| `Burnout_Score` | int | Skor burnout (1-10) |
| `Anxiety_Level` | int | Tingkat kecemasan (1-10) |
| `Job_Satisfaction` | int | Kepuasan kerja (1-10) |
| `Work_Life_Balance` | int | Work-life balance (1-10) |
| `Mental_Health_Risk` | string | Low/Medium/High |
| `Work_Hours_Per_Week` | int | Jam kerja per minggu |
| `Access_to_Mental_Health_Resources` | string | Yes/No |
| `Manager_Support` | int | Dukungan manager (1-10) |
| `Social_Isolation_Rating` | int | Tingkat isolasi (1-5) |
| `Productivity_Score` | int | Skor produktivitas (40-100) |

## 🔍 Key Insights dari Analisis

### 🔴 Critical Findings
1. **~30% Gen Z** memiliki risiko mental health tinggi
2. **45% peningkatan stress** pada Gen Z yang bekerja >50 jam/minggu
3. **Remote Gen Z workers** memiliki 35% lebih tinggi social isolation

### ✅ Positive Findings
4. **Mental health resources** mengurangi burnout ~20%
5. **Strong manager support** berkorelasi positif dengan job satisfaction
6. **Flexible working** meningkatkan work-life balance

### 📊 Recommendations Priority
- **HIGH**: Batas overtime & ekspansi mental health programs
- **MEDIUM**: Social initiatives & department-specific interventions
- **LOW**: Wellness programs dengan sleep education

## 💰 Expected Business Impact

| Metric | Expected Improvement | Timeline |
|--------|---------------------|----------|
| **Turnover Reduction** | 20-25% decrease | 6-12 months |
| **Productivity** | 15-20% improvement | 3-6 months |
| **Cost Savings** | $500-800K annually | 12 months |
| **Sick Leaves** | 30% reduction | 6-12 months |

## 🤝 Contributing

Contributions are welcome! Untuk contribute:

1. Fork repository ini
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 To-Do List

- [ ] Integrasi dengan real-time data sources
- [ ] Machine learning model untuk prediksi burnout
- [ ] Export reports ke PDF
- [ ] Multi-language support (EN/ID)
- [ ] Mobile responsive design
- [ ] Email alert system untuk high-risk employees
- [ ] Integration dengan HRMS systems

## 🐛 Troubleshooting

### Issue: PySpark tidak bisa start
**Solution**: 
```bash
# Install Java 8 atau 11
# Set JAVA_HOME environment variable
export JAVA_HOME=/path/to/java
```

### Issue: Streamlit error "No module named 'plotly'"
**Solution**:
```bash
pip install plotly --upgrade
```

### Issue: Data tidak load
**Solution**:
Dashboard akan otomatis generate sample data. Pastikan:
- File `genz_dashboard_data.csv` ada di folder yang sama
- Atau jalankan notebook untuk generate data

## 📚 Resources

- [Dokumentasi PySpark](https://spark.apache.org/docs/latest/api/python/)
- [Dokumentasi Streamlit](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [Mental Health at Work - WHO](https://www.who.int/news-room/fact-sheets/detail/mental-health-at-work)

## 👥 Authors

- **Your Name** - Initial work - [GitHub Profile](https://github.com/username)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dataset dari Kaggle: Mental Health & Burnout in the Workplace
- Inspired by research tentang Gen Z mental health trends
- Built with ❤️ for better employee well-being

## 📧 Contact

Untuk pertanyaan atau feedback:
- Email: your.email@example.com
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- GitHub Issues: [Create an issue](https://github.com/username/repo/issues)

---

**⭐ Jika project ini membantu, jangan lupa berikan star!**

**Last Updated**: January 2026
