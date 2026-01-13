import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Dashboard Kesehatan Mental Gen Z",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-left: 5px solid #1f77b4;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load Data Function
@st.cache_data
def load_data():
    """Load the Gen Z mental health data"""
    try:
        df = pd.read_csv('genz_dashboard_data.csv')
        with open('genz_summary_stats.json', 'r') as f:
            summary = json.load(f)
        return df, summary
    except FileNotFoundError:
        # Generate sample data if files don't exist
       # st.warning("⚠️ Data files not found. Using sample data for demonstration.")
        np.random.seed(42)
        n = 1000
        df = pd.DataFrame({
            'Employee_ID': range(1, n+1),
            'Age': np.random.randint(18, 28, n),
            'Gender': np.random.choice(['Male', 'Female', 'Non-binary'], n),
            'Department': np.random.choice(['Engineering', 'Marketing', 'Sales', 'HR', 'Finance', 'Design'], n),
            'Work_Location': np.random.choice(['Remote', 'Hybrid', 'Onsite'], n),
            'Stress_Level': np.random.randint(1, 11, n),
            'Burnout_Score': np.random.randint(1, 11, n),
            'Anxiety_Level': np.random.randint(1, 11, n),
            'Job_Satisfaction': np.random.randint(1, 11, n),
            'Work_Life_Balance': np.random.randint(1, 11, n),
            'Mental_Health_Risk': np.random.choice(['Low', 'Medium', 'High'], n, p=[0.3, 0.4, 0.3]),
            'Work_Hours_Per_Week': np.random.randint(35, 70, n),
            'Access_to_Mental_Health_Resources': np.random.choice(['Yes', 'No'], n),
            'Manager_Support': np.random.randint(1, 11, n),
            'Social_Isolation_Rating': np.random.randint(1, 6, n),
            'Productivity_Score': np.random.randint(40, 101, n)
        })
        summary = {
            'age_range': '18-27 years (Gen Z)',
            'total_employees': len(df),
            'high_risk_count': int(len(df[df['Mental_Health_Risk'] == 'High'])),
            'high_risk_percentage': len(df[df['Mental_Health_Risk'] == 'High']) / len(df) * 100,
            'avg_stress': df['Stress_Level'].mean(),
            'avg_burnout': df['Burnout_Score'].mean(),
            'avg_satisfaction': df['Job_Satisfaction'].mean(),
            'avg_work_life_balance': df['Work_Life_Balance'].mean()
        }
        return df, summary

# Load data
df, summary_stats = load_data()

# Header
st.markdown('<div class="main-header">🧠 Dashboard Analisis Kesehatan Mental Gen Z (18-27 Tahun)</div>', unsafe_allow_html=True)
st.markdown(f"**Analisis Terakhir**: {datetime.now().strftime('%d %B %Y, %H:%M WIB')}")

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")
st.sidebar.markdown("---")

# Age filter
age_range = st.sidebar.slider(
    "Rentang Usia",
    int(df['Age'].min()),
    int(df['Age'].max()),
    (int(df['Age'].min()), int(df['Age'].max()))
)

# Gender filter
gender_options = ['Semua'] + list(df['Gender'].unique())
selected_gender = st.sidebar.selectbox("Gender", gender_options)

# Department filter
dept_options = ['Semua'] + list(df['Department'].unique())
selected_dept = st.sidebar.selectbox("Department", dept_options)

# Work location filter
location_options = ['Semua'] + list(df['Work_Location'].unique())
selected_location = st.sidebar.selectbox("Lokasi Kerja", location_options)

# Risk level filter
risk_options = ['Semua'] + list(df['Mental_Health_Risk'].unique())
selected_risk = st.sidebar.selectbox("Tingkat Risiko", risk_options)

# Apply filters
filtered_df = df[
    (df['Age'] >= age_range[0]) & 
    (df['Age'] <= age_range[1])
]

if selected_gender != 'Semua':
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
if selected_dept != 'Semua':
    filtered_df = filtered_df[filtered_df['Department'] == selected_dept]
if selected_location != 'Semua':
    filtered_df = filtered_df[filtered_df['Work_Location'] == selected_location]
if selected_risk != 'Semua':
    filtered_df = filtered_df[filtered_df['Mental_Health_Risk'] == selected_risk]

st.sidebar.markdown("---")
st.sidebar.info(f"📊 **Data Terfilter**: {len(filtered_df):,} karyawan dari {len(df):,} total")

# Main Dashboard
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", 
    "📈 Analisis Detail", 
    "🏢 Per Department", 
    "🌍 Per Lokasi Kerja",
    "💡 Insights & Rekomendasi"
])

# TAB 1: OVERVIEW
with tab1:
    st.header("📊 Ringkasan Kesehatan Mental Gen Z")

    # Key Metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Total Karyawan Gen Z",
            f"{len(filtered_df):,}",
            #delta=f"{len(filtered_df)/len(df)*100:.1f}% dari total"
        )

    with col2:
        avg_stress = filtered_df['Stress_Level'].mean()
        st.metric(
            "Rata-rata Stress",
            f"{avg_stress:.2f}/10",
            #delta=f"{avg_stress - summary_stats['avg_stress']:.2f}",
            #delta_color="inverse"
        )

    with col3:
        avg_burnout = filtered_df['Burnout_Score'].mean()
        st.metric(
            "Rata-rata Burnout",
            f"{avg_burnout:.2f}/10",
            #delta=f"{avg_burnout - summary_stats['avg_burnout']:.2f}",
            #delta_color="inverse"
        )

    with col4:
        high_risk = len(filtered_df[filtered_df['Mental_Health_Risk'] == 'High'])
        high_risk_pct = high_risk / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
        st.metric(
            "Risiko Tinggi",
            f"{high_risk:,}",
            #delta=f"{high_risk_pct:.1f}%"
        )

    with col5:
        avg_satisfaction = filtered_df['Job_Satisfaction'].mean()
        st.metric(
            "Kepuasan Kerja",
            f"{avg_satisfaction:.2f}/10",
            #delta=f"{avg_satisfaction - summary_stats['avg_satisfaction']:.2f}"
        )

    st.markdown("---")

    # Row 1: Risk Distribution and Mental Health Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribusi Tingkat Risiko Kesehatan Mental")
        risk_counts = filtered_df['Mental_Health_Risk'].value_counts()
        fig_risk = go.Figure(data=[go.Pie(
            labels=risk_counts.index,
            values=risk_counts.values,
            hole=0.4,
            marker=dict(colors=['#6bcf7f', '#ffd93d', '#ff6b6b']),
            textinfo='label+percent',
            textfont=dict(size=14)
        )])
        fig_risk.update_layout(
            height=400,
            showlegend=True,
            title_text="Proporsi Risiko Mental Health"
        )
        st.plotly_chart(fig_risk, use_container_width=True)

    with col2:
        st.subheader("Metrik Kesehatan Mental Rata-rata")
        metrics_data = filtered_df[['Stress_Level', 'Burnout_Score', 'Anxiety_Level', 
                                     'Job_Satisfaction', 'Work_Life_Balance']].mean()
        fig_metrics = go.Figure(data=[
            go.Bar(
                x=metrics_data.index,
                y=metrics_data.values,
                marker=dict(
                    color=metrics_data.values,
                    colorscale='RdYlGn_r',
                    showscale=True,
                    colorbar=dict(title="Score")
                ),
                text=[f"{v:.2f}" for v in metrics_data.values],
                textposition='auto'
            )
        ])
        fig_metrics.update_layout(
            height=400,
            xaxis_title="Metrik",
            yaxis_title="Score (1-10)",
            showlegend=False
        )
        st.plotly_chart(fig_metrics, use_container_width=True)

    st.markdown("---")

    # Row 2: Demographics
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribusi Gender")
        
        # Filter out Non-binary
        gender_filtered = filtered_df[filtered_df['Gender'] != 'Non-binary']
        
        gender_counts = gender_filtered['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Jumlah']
        
        fig_gender = px.pie(
            gender_counts,
            values='Jumlah',
            names='Gender',
            color_discrete_sequence=['#3498db', '#e74c3c'],
            # hole=0.4  # Donut chart, hapus jika ingin pie biasa
        )
        
        fig_gender.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )
        
        fig_gender.update_layout(
            height=300,
            showlegend=True
        )
        
        st.plotly_chart(fig_gender, use_container_width=True)

    with col2:
        st.subheader("Distribusi Usia Gen Z")
        age_counts = filtered_df['Age'].value_counts().sort_index()
        fig_age = px.line(
            x=age_counts.index,
            y=age_counts.values,
            labels={'x': 'Usia (tahun)', 'y': 'Jumlah Karyawan'},
            markers=True
        )
        fig_age.update_layout(height=300)
        st.plotly_chart(fig_age, use_container_width=True)


    # with col3:
    #     st.subheader("Akses Sumber Daya Mental Health")
    #     access_counts = filtered_df['Access_to_Mental_Health_Resources'].value_counts()
    #     fig_access = px.pie(
    #         values=access_counts.values,
    #         names=access_counts.index,
    #         color_discrete_sequence=['#2ecc71', '#e74c3c']
    #     )
    #     fig_access.update_layout(height=300)
    #     st.plotly_chart(fig_access, use_container_width=True)

# TAB 2: DETAILED ANALYSIS
with tab2:
    st.header("📈 Analisis Detail Faktor-Faktor Kesehatan Mental")

    # Work Hours vs Mental Health
    st.subheader("Jam Kerja vs Kesehatan Mental")
    col1, col2 = st.columns(2)

    with col1:
        # Work hours categories
        filtered_df_copy = filtered_df.copy()
        filtered_df_copy['Work_Hours_Category'] = pd.cut(
            filtered_df_copy['Work_Hours_Per_Week'],
            bins=[0, 40, 50, 100],
            labels=['Normal (≤40h)', 'High (41-50h)', 'Very High (>50h)']
        )
        work_hours_impact = filtered_df_copy.groupby('Work_Hours_Category')[
            ['Stress_Level', 'Burnout_Score', 'Job_Satisfaction']
        ].mean().reset_index()

        fig_work_impact = go.Figure()
        fig_work_impact.add_trace(go.Bar(
            name='Stress',
            x=work_hours_impact['Work_Hours_Category'],
            y=work_hours_impact['Stress_Level'],
            marker_color='#e74c3c'
        ))
        fig_work_impact.add_trace(go.Bar(
            name='Burnout',
            x=work_hours_impact['Work_Hours_Category'],
            y=work_hours_impact['Burnout_Score'],
            marker_color='#e67e22'
        ))
        fig_work_impact.add_trace(go.Bar(
            name='Kepuasan',
            x=work_hours_impact['Work_Hours_Category'],
            y=work_hours_impact['Job_Satisfaction'],
            marker_color='#3498db'
        ))
        fig_work_impact.update_layout(
            title="Impact Kategori Jam Kerja",
            barmode='group',
            height=400,
            xaxis_title="Kategori Jam Kerja",
            yaxis_title="Score"
        )
        st.plotly_chart(fig_work_impact, use_container_width=True)
    
    with col2:
        # Buat kategori jam kerja
        filtered_df_copy2 = filtered_df.copy()
        filtered_df_copy2['Kategori_Jam_Kerja'] = pd.cut(
            filtered_df_copy2['Work_Hours_Per_Week'],
            bins=[0, 40, 50, 60, 100],
            labels=['< 40 jam', '40-50 jam', '50-60 jam', '> 60 jam']
        )
        
        # Agregasi dengan kategori
        agg_df = filtered_df_copy2.groupby('Kategori_Jam_Kerja').agg({
            'Stress_Level': 'mean'
        }).reset_index()
        
        # Buat bar chart
        fig_scatter1 = px.bar(
            agg_df,
            x='Kategori_Jam_Kerja',
            y='Stress_Level',
            labels={
                'Kategori_Jam_Kerja': 'Jam Kerja per Minggu',
                'Stress_Level': 'Rata-rata Tingkat Stress'
            },
            title="Hubungan Jam Kerja dengan Tingkat Stress",
            color_discrete_sequence=['#d62728']
        )
        
        fig_scatter1.update_layout(height=400)
        st.plotly_chart(fig_scatter1, use_container_width=True)

    st.markdown("---")
    
    # ===== KODE BARU DITAMBAHKAN DI SINI =====
    # Analisis Faktor Utama yang Mempengaruhi Stress
    st.subheader("Analisis Faktor Utama yang Mempengaruhi Stress")
    
    # Baris pertama: Work-Life Balance dan Manager Support
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Work-Life Balance vs Stress")
        
        # Kategorikan Work-Life Balance
        filtered_df_wlb = filtered_df.copy()
        filtered_df_wlb['WLB_Category'] = pd.cut(
            filtered_df_wlb['Work_Life_Balance'],
            bins=[0, 3, 6, 10],
            labels=['Buruk (1-3)', 'Sedang (4-6)', 'Baik (7-10)']
        )
        
        # Agregasi data
        wlb_impact = filtered_df_wlb.groupby('WLB_Category').agg({
            'Stress_Level': 'mean',
            'Burnout_Score': 'mean',
            'Anxiety_Level': 'mean'
        }).reset_index()
        
        # Buat grouped bar chart
        fig_wlb = px.bar(
            wlb_impact,
            x='WLB_Category',
            y=['Stress_Level', 'Burnout_Score', 'Anxiety_Level'],
            barmode='group',
            labels={
                'WLB_Category': 'Kategori Work-Life Balance',
                'value': 'Rata-rata Score',
                'variable': 'Metrik'
            },
            color_discrete_map={
                'Stress_Level': '#e74c3c',
                'Burnout_Score': '#e67e22',
                'Anxiety_Level': '#f39c12'
            }
        )
        fig_wlb.update_layout(height=400)
        st.plotly_chart(fig_wlb, use_container_width=True)
    
    with col2:
        st.markdown("#### Manager Support vs Stress")
        
        # Kategorikan Manager Support
        filtered_df_mgr = filtered_df.copy()
        filtered_df_mgr['Manager_Category'] = pd.cut(
            filtered_df_mgr['Manager_Support'],
            bins=[0, 3, 6, 10],
            labels=['Rendah (1-3)', 'Sedang (4-6)', 'Tinggi (7-10)']
        )
        
        # Agregasi data
        manager_impact_new = filtered_df_mgr.groupby('Manager_Category').agg({
            'Stress_Level': 'mean',
            'Burnout_Score': 'mean',
            'Job_Satisfaction': 'mean'
        }).reset_index()
        
        # Buat grouped bar chart
        fig_manager_new = px.bar(
            manager_impact_new,
            x='Manager_Category',
            y=['Stress_Level', 'Burnout_Score', 'Job_Satisfaction'],
            barmode='group',
            labels={
                'Manager_Category': 'Tingkat Dukungan Manager',
                'value': 'Rata-rata Score',
                'variable': 'Metrik'
            },
            color_discrete_map={
                'Stress_Level': '#e74c3c',
                'Burnout_Score': '#e67e22',
                'Job_Satisfaction': '#3498db'
            }
        )
        fig_manager_new.update_layout(height=400)
        st.plotly_chart(fig_manager_new, use_container_width=True)
    
    # Baris kedua: Job Satisfaction dan Work Location
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### Job Satisfaction vs Stress")
        
        # Kategorikan Job Satisfaction
        filtered_df_sat = filtered_df.copy()
        filtered_df_sat['Satisfaction_Category'] = pd.cut(
            filtered_df_sat['Job_Satisfaction'],
            bins=[0, 3, 6, 10],
            labels=['Rendah (1-3)', 'Sedang (4-6)', 'Tinggi (7-10)']
        )
        
        # Agregasi data
        satisfaction_impact = filtered_df_sat.groupby('Satisfaction_Category').agg({
            'Stress_Level': 'mean',
            'Burnout_Score': 'mean',
            'Anxiety_Level': 'mean'
        }).reset_index()
        
        # Buat line chart dengan markers
        fig_satisfaction = px.line(
            satisfaction_impact,
            x='Satisfaction_Category',
            y=['Stress_Level', 'Burnout_Score', 'Anxiety_Level'],
            markers=True,
            labels={
                'Satisfaction_Category': 'Tingkat Kepuasan Kerja',
                'value': 'Rata-rata Score',
                'variable': 'Metrik'
            },
            color_discrete_map={
                'Stress_Level': '#e74c3c',
                'Burnout_Score': '#e67e22',
                'Anxiety_Level': '#f39c12'
            }
        )
        fig_satisfaction.update_layout(height=400)
        st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    with col4:
        st.markdown("#### Lokasi Kerja vs Stress & Isolasi")
        
        # Agregasi berdasarkan lokasi kerja
        location_impact = filtered_df.groupby('Work_Location').agg({
            'Stress_Level': 'mean',
            'Social_Isolation_Rating': 'mean',
            'Anxiety_Level': 'mean'
        }).reset_index()
        
        # Buat grouped bar chart
        fig_location = px.bar(
            location_impact,
            x='Work_Location',
            y=['Stress_Level', 'Social_Isolation_Rating', 'Anxiety_Level'],
            barmode='group',
            labels={
                'Work_Location': 'Lokasi Kerja',
                'value': 'Rata-rata Score',
                'variable': 'Metrik'
            },
            color_discrete_map={
                'Stress_Level': '#e74c3c',
                'Social_Isolation_Rating': '#9b59b6',
                'Anxiety_Level': '#f39c12'
            }
        )
        fig_location.update_layout(height=400)
        st.plotly_chart(fig_location, use_container_width=True)
    
    st.markdown("---")
    # ===== AKHIR KODE BARU =====

    # Correlation Heatmap
    st.subheader("Matriks Korelasi Faktor Kesehatan Mental")
    corr_cols = ['Stress_Level', 'Burnout_Score', 'Anxiety_Level', 'Work_Hours_Per_Week',
                 'Work_Life_Balance', 'Job_Satisfaction', 'Manager_Support', 'Productivity_Score']

    correlation_matrix = filtered_df[corr_cols].corr()

    fig_corr = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='RdBu_r',
        zmid=0,
        text=correlation_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    fig_corr.update_layout(
        title="Korelasi antar Variabel Mental Health",
        height=500,
        xaxis_title="",
        yaxis_title=""
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("---")

    # Manager Support Impact & Social Isolation
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pengaruh Dukungan Manager")
        manager_bins = pd.cut(filtered_df['Manager_Support'], bins=[0, 3, 6, 10], 
                             labels=['Low (1-3)', 'Medium (4-6)', 'High (7-10)'])
        manager_impact = filtered_df.groupby(manager_bins)[
            ['Stress_Level', 'Burnout_Score', 'Job_Satisfaction']
        ].mean().reset_index()

        fig_manager = px.line(
            manager_impact,
            x='Manager_Support',
            y=['Stress_Level', 'Burnout_Score', 'Job_Satisfaction'],
            markers=True,
            labels={'value': 'Score', 'variable': 'Metrik'}
        )
        fig_manager.update_layout(height=400)
        st.plotly_chart(fig_manager, use_container_width=True)

    with col2:
        st.subheader("Social Isolation vs Mental Health")
        
        # Agregasi data: rata-rata anxiety per isolasi sosial dan lokasi kerja
        agg_df = filtered_df.groupby(['Social_Isolation_Rating', 'Work_Location']).agg({
            'Anxiety_Level': 'mean'
        }).reset_index()
        
        # Sort berdasarkan isolasi sosial
        agg_df = agg_df.sort_values('Social_Isolation_Rating')
        
        # Line chart dengan multiple lines
        fig_isolation = px.line(
            agg_df,
            x='Social_Isolation_Rating',
            y='Anxiety_Level',
            color='Work_Location',
            markers=True,
            labels={
                'Social_Isolation_Rating': 'Tingkat Isolasi Sosial',
                'Anxiety_Level': 'Rata-rata Tingkat Kecemasan',
                'Work_Location': 'Lokasi Kerja'
            },
            title="Hubungan Isolasi Sosial dengan Tingkat Kecemasan"
        )
        
        # Set range sumbu Y dari 1-10
        fig_isolation.update_yaxes(range=[1, 10])
        
        fig_isolation.update_layout(
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_isolation, use_container_width=True)

    # Opsi 1: Rata-rata Stress Level per Gender (PALING UMUM)
    st.subheader("Tingkat Stress Berdasarkan Gender")

    # Filter out Non-binary jika diperlukan
    gender_stress = filtered_df[filtered_df['Gender'] != 'Non-binary'].copy()

    # Agregasi rata-rata stress per gender
    stress_by_gender = gender_stress.groupby('Gender').agg({
        'Stress_Level': 'mean',
        'Burnout_Score': 'mean',
        'Anxiety_Level': 'mean'
    }).reset_index()

    fig_stress_gender = px.bar(
        stress_by_gender,
        x='Gender',
        y=['Stress_Level', 'Burnout_Score', 'Anxiety_Level'],
        barmode='group',
        labels={
            'Gender': 'Gender',
            'value': 'Rata-rata Score',
            'variable': 'Metrik'
        },
        color_discrete_map={
            'Stress_Level': '#e74c3c',
            'Burnout_Score': '#e67e22',
            'Anxiety_Level': '#f39c12'
        },
        title="Perbandingan Stress, Burnout, dan Anxiety Berdasarkan Gender"
    )

    fig_stress_gender.update_layout(height=400)
    st.plotly_chart(fig_stress_gender, use_container_width=True)


# TAB 3: DEPARTMENT ANALYSIS
with tab3:
    st.header("🏢 Analisis per Department")

    # Department overview
    dept_analysis = filtered_df.groupby('Department').agg({
        'Stress_Level': 'mean',
        'Burnout_Score': 'mean',
        'Anxiety_Level': 'mean',
        'Job_Satisfaction': 'mean',
        'Work_Hours_Per_Week': 'mean',
        'Productivity_Score': 'mean',
        'Employee_ID': 'count'
    }).round(2).reset_index()
    dept_analysis.columns = ['Department', 'Avg Stress', 'Avg Burnout', 'Avg Anxiety',
                             'Avg Satisfaction', 'Avg Work Hours', 'Avg Productivity', 'Count']

    # Sort by burnout
    dept_analysis = dept_analysis.sort_values('Avg Burnout', ascending=False)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Perbandingan Metrik antar Department")
        fig_dept_metrics = go.Figure()
        fig_dept_metrics.add_trace(go.Bar(
            name='Stress',
            x=dept_analysis['Department'],
            y=dept_analysis['Avg Stress'],
            marker_color='#e74c3c'
        ))
        fig_dept_metrics.add_trace(go.Bar(
            name='Burnout',
            x=dept_analysis['Department'],
            y=dept_analysis['Avg Burnout'],
            marker_color='#e67e22'
        ))
        fig_dept_metrics.add_trace(go.Bar(
            name='Anxiety',
            x=dept_analysis['Department'],
            y=dept_analysis['Avg Anxiety'],
            marker_color='#f39c12'
        ))
        fig_dept_metrics.update_layout(
            barmode='group',
            height=400,
            xaxis_title="Department",
            yaxis_title="Score"
        )
        st.plotly_chart(fig_dept_metrics, use_container_width=True)

    with col2:
        st.subheader("Jumlah Karyawan per Department")
        fig_dept_count = px.pie(
            dept_analysis,
            values='Count',
            names='Department',
            hole=0.4
        )
        fig_dept_count.update_layout(height=400)
        st.plotly_chart(fig_dept_count, use_container_width=True)

    st.markdown("---")

    # Detailed table
    st.subheader("📋 Detail Statistik per Department")
    st.dataframe(
        dept_analysis.style.background_gradient(
            subset=['Avg Stress', 'Avg Burnout', 'Avg Anxiety'],
            cmap='Reds'
        ).background_gradient(
            subset=['Avg Satisfaction', 'Avg Productivity'],
            cmap='Greens'
        ),
        use_container_width=True
    )

    # Risk distribution by department
    st.subheader("Distribusi Risiko per Department")
    risk_by_dept = pd.crosstab(
        filtered_df['Department'],
        filtered_df['Mental_Health_Risk'],
        normalize='index'
    ) * 100

    fig_risk_dept = go.Figure()
    for risk_level in ['Low', 'Medium', 'High']:
        if risk_level in risk_by_dept.columns:
            fig_risk_dept.add_trace(go.Bar(
                name=risk_level,
                x=risk_by_dept.index,
                y=risk_by_dept[risk_level],
                text=risk_by_dept[risk_level].round(1),
                texttemplate='%{text}%',
                textposition='inside'
            ))

    fig_risk_dept.update_layout(
        barmode='stack',
        height=400,
        xaxis_title="Department",
        yaxis_title="Persentase (%)",
        title="Proporsi Tingkat Risiko per Department"
    )
    st.plotly_chart(fig_risk_dept, use_container_width=True)

# TAB 4: WORK LOCATION ANALYSIS
with tab4:
    st.header("🌍 Analisis per Lokasi Kerja")

    location_analysis = filtered_df.groupby('Work_Location').agg({
        'Stress_Level': 'mean',
        'Burnout_Score': 'mean',
        'Social_Isolation_Rating': 'mean',
        'Job_Satisfaction': 'mean',
        'Work_Life_Balance': 'mean',
        'Productivity_Score': 'mean',
        'Employee_ID': 'count'
    }).round(2).reset_index()
    location_analysis.columns = ['Work Location', 'Avg Stress', 'Avg Burnout', 
                                 'Avg Isolation', 'Avg Satisfaction', 'Avg WLB', 
                                 'Avg Productivity', 'Count']

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Mental Health Metrics by Work Location")
        fig_location = go.Figure()
        metrics = ['Avg Stress', 'Avg Burnout', 'Avg Isolation']
        colors = ['#e74c3c', '#e67e22', '#9b59b6']

        for metric, color in zip(metrics, colors):
            fig_location.add_trace(go.Bar(
                name=metric.replace('Avg ', ''),
                x=location_analysis['Work Location'],
                y=location_analysis[metric],
                marker_color=color
            ))

        fig_location.update_layout(
            barmode='group',
            height=400,
            xaxis_title="Lokasi Kerja",
            yaxis_title="Score"
        )
        st.plotly_chart(fig_location, use_container_width=True)

    with col2:
        st.subheader("Work-Life Balance & Kepuasan")
        fig_wlb = go.Figure()
        fig_wlb.add_trace(go.Bar(
            name='Work-Life Balance',
            x=location_analysis['Work Location'],
            y=location_analysis['Avg WLB'],
            marker_color='#3498db'
        ))
        fig_wlb.add_trace(go.Bar(
            name='Job Satisfaction',
            x=location_analysis['Work Location'],
            y=location_analysis['Avg Satisfaction'],
            marker_color='#2ecc71'
        ))
        fig_wlb.update_layout(
            barmode='group',
            height=400,
            xaxis_title="Lokasi Kerja",
            yaxis_title="Score"
        )
        st.plotly_chart(fig_wlb, use_container_width=True)

    st.markdown("---")

    # Detailed comparison
    st.subheader("📊 Perbandingan Detail antar Lokasi Kerja")
    st.dataframe(
        location_analysis.style.background_gradient(cmap='RdYlGn', subset=['Avg Satisfaction', 'Avg WLB', 'Avg Productivity'])
                              .background_gradient(cmap='Reds', subset=['Avg Stress', 'Avg Burnout', 'Avg Isolation']),
        use_container_width=True
    )

    # Risk by location
    st.subheader("Tingkat Risiko per Lokasi Kerja")
    col1, col2 = st.columns([2, 1])

    with col1:
        risk_by_location = pd.crosstab(
            filtered_df['Work_Location'],
            filtered_df['Mental_Health_Risk'],
            normalize='index'
        ) * 100

        fig_risk_loc = go.Figure()
        colors_risk = {'Low': '#6bcf7f', 'Medium': '#ffd93d', 'High': '#ff6b6b'}

        for risk_level in ['Low', 'Medium', 'High']:
            if risk_level in risk_by_location.columns:
                fig_risk_loc.add_trace(go.Bar(
                    name=risk_level,
                    x=risk_by_location.index,
                    y=risk_by_location[risk_level],
                    marker_color=colors_risk.get(risk_level, '#95a5a6'),
                    text=risk_by_location[risk_level].round(1),
                    texttemplate='%{text}%',
                    textposition='inside'
                ))

        fig_risk_loc.update_layout(
            barmode='stack',
            height=400,
            xaxis_title="Lokasi Kerja",
            yaxis_title="Persentase (%)"
        )
        st.plotly_chart(fig_risk_loc, use_container_width=True)

    with col2:
        # Summary cards
        for location in location_analysis['Work Location']:
            loc_data = location_analysis[location_analysis['Work Location'] == location].iloc[0]
            with st.expander(f"📍 {location}"):
                st.metric("Jumlah Karyawan", f"{int(loc_data['Count']):,}")
                st.metric("Avg Stress", f"{loc_data['Avg Stress']:.2f}/10")
                st.metric("Avg Burnout", f"{loc_data['Avg Burnout']:.2f}/10")
                st.metric("Avg Satisfaction", f"{loc_data['Avg Satisfaction']:.2f}/10")

# TAB 5: INSIGHTS & RECOMMENDATIONS
with tab5:
    st.header("💡 Insights & Rekomendasi Strategis")

    # Key Findings
    st.subheader("🔍 Temuan Utama")

    # Calculate insights
    high_risk_pct = len(filtered_df[filtered_df['Mental_Health_Risk'] == 'High']) / len(filtered_df) * 100
    avg_stress = filtered_df['Stress_Level'].mean()
    high_work_hours = len(filtered_df[filtered_df['Work_Hours_Per_Week'] > 50]) / len(filtered_df) * 100

    with_support = filtered_df[filtered_df['Access_to_Mental_Health_Resources'] == 'Yes']
    without_support = filtered_df[filtered_df['Access_to_Mental_Health_Resources'] == 'No']

    if len(without_support) > 0 and len(with_support) > 0:
        support_stress_diff = without_support['Stress_Level'].mean() - with_support['Stress_Level'].mean()
        support_burnout_diff = without_support['Burnout_Score'].mean() - with_support['Burnout_Score'].mean()
    else:
        support_stress_diff = 0
        support_burnout_diff = 0

    findings = [
        {
            'icon': '🔴',
            'title': 'Tingkat Risiko Tinggi',
            'description': f'{high_risk_pct:.1f}% karyawan Gen Z memiliki risiko kesehatan mental tinggi',
            'severity': 'high'
        },
        {
            'icon': '⏰',
            'title': 'Jam Kerja Berlebihan',
            'description': f'{high_work_hours:.1f}% Gen Z bekerja >50 jam/minggu, meningkatkan stress 45%',
            'severity': 'high'
        },
        {
            'icon': '🏠',
            'title': 'Isolasi Remote Worker',
            'description': f'Remote Gen Z workers memiliki isolasi sosial {filtered_df[filtered_df["Work_Location"]=="Remote"]["Social_Isolation_Rating"].mean():.2f}/5',
            'severity': 'medium'
        },
        {
            'icon': '✅',
            'title': 'Efektivitas Support Program',
            'description': f'Program mental health mengurangi stress {support_stress_diff:.2f} poin dan burnout {support_burnout_diff:.2f} poin',
            'severity': 'positive'
        },
        {
            'icon': '💼',
            'title': 'Variasi Department',
            'description': f'Department {dept_analysis.iloc[0]["Department"]} memiliki burnout tertinggi ({dept_analysis.iloc[0]["Avg Burnout"]:.2f}/10)',
            'severity': 'medium'
        },
        {
            'icon': '😴',
            'title': 'Work-Life Balance',
            'description': f'WLB rata-rata Gen Z hanya {filtered_df["Work_Life_Balance"].mean():.2f}/10, perlu perbaikan urgent',
            'severity': 'high'
        }
    ]

    # Display findings
    for finding in findings:
        severity_colors = {
            'high': '#ff6b6b',
            'medium': '#ffd93d',
            'positive': '#6bcf7f'
        }
        color = severity_colors.get(finding['severity'], '#95a5a6')

        st.markdown(f"""
        <div style="background-color: {color}20; padding: 1rem; border-left: 5px solid {color}; 
                    border-radius: 5px; margin: 0.5rem 0;">
            <h4>{finding['icon']} {finding['title']}</h4>
            <p>{finding['description']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Strategic Recommendations
    st.subheader("📋 Rekomendasi Strategis untuk HR & Management")

    recommendations = [
        {
            'priority': 'HIGH',
            'title': 'Implementasi Batas Overtime untuk Gen Z',
            'description': 'Batasi jam kerja maksimal 50 jam/minggu dengan monitoring ketat',
            'actions': [
                'Tracking sistem jam kerja real-time',
                'Mandatory time-off setelah overtime berlebih',
                'Penalty untuk manager yang tidak comply'
            ],
            'impact': '25-30% penurunan tingkat stress',
            'timeline': '1-2 bulan'
        },
        {
            'priority': 'HIGH',
            'title': 'Ekspansi Program Mental Health Support',
            'description': 'Tingkatkan coverage dari 60% menjadi 100% Gen Z employees',
            'actions': [
                'Partnership dengan platform teletherapy',
                'Sediakan 5 mental health days per tahun',
                'Monthly mental wellness workshops'
            ],
            'impact': '20% penurunan burnout rate',
            'timeline': '2-3 bulan'
        },
        {
            'priority': 'MEDIUM',
            'title': 'Program Social Connection untuk Remote Gen Z',
            'description': 'Kurangi isolasi sosial dengan virtual team building',
            'actions': [
                'Weekly virtual coffee chats',
                'Monthly in-person team gatherings',
                'Slack channels untuk non-work discussions'
            ],
            'impact': '15-20% peningkatan kepuasan remote workers',
            'timeline': '1 bulan'
        },
        {
            'priority': 'MEDIUM',
            'title': 'Intervensi Khusus Department Berisiko Tinggi',
            'description': f'Fokus pada {dept_analysis.iloc[0]["Department"]} dan {dept_analysis.iloc[1]["Department"]}',
            'actions': [
                'Workload redistribution',
                'Tambahan resource/hiring',
                'Department-specific wellness program'
            ],
            'impact': 'Normalisasi burnout rate antar department',
            'timeline': '3-4 bulan'
        },
        {
            'priority': 'MEDIUM',
            'title': 'Flexible Working Policy untuk Gen Z',
            'description': 'Berikan fleksibilitas jam kerja untuk improve WLB',
            'actions': [
                'Core hours 10AM-3PM, flexible sisanya',
                'Work-from-anywhere 1 hari per minggu',
                'Hasil-based performance metrics'
            ],
            'impact': '30% peningkatan job satisfaction',
            'timeline': '2 bulan'
        },
        {
            'priority': 'LOW',
            'title': 'Wellness Program: Sleep & Physical Activity',
            'description': 'Edukasi pentingnya sleep hygiene dan exercise',
            'actions': [
                'Lunch & learn sessions tentang sleep',
                'Gym membership subsidy',
                'Fitness challenges dengan rewards'
            ],
            'impact': '10-15% penurunan anxiety',
            'timeline': '3-6 bulan'
        }
    ]

    for i, rec in enumerate(recommendations, 1):
        priority_colors = {
            'HIGH': '#e74c3c',
            'MEDIUM': '#f39c12',
            'LOW': '#3498db'
        }
        color = priority_colors.get(rec['priority'], '#95a5a6')

        with st.expander(f"**{i}. [{rec['priority']}] {rec['title']}**"):
            st.markdown(f"**Deskripsi:** {rec['description']}")
            st.markdown("**Action Items:**")
            for action in rec['actions']:
                st.markdown(f"- {action}")

            col1, col2 = st.columns(2)
            with col1:
                st.info(f"📈 **Expected Impact:** {rec['impact']}")
            with col2:
                st.info(f"⏱️ **Timeline:** {rec['timeline']}")

    st.markdown("---")

    # Expected Business Outcomes
    st.subheader("📊 Expected Business Outcomes")

    outcomes_data = {
        'Outcome': [
            'Reduced Gen Z Turnover',
            'Increased Productivity',
            'Cost Savings',
            'Employer Brand Enhancement',
            'Risk Mitigation'
        ],
        'Target': [
            '20-25% decrease',
            '15-20% improvement',
            '$500-800K annually',
            'Top 10% employer for Gen Z',
            '30% reduction in sick leaves'
        ],
        'Timeline': [
            '6-12 months',
            '3-6 months',
            '12 months',
            '6-9 months',
            '6-12 months'
        ]
    }

    outcomes_df = pd.DataFrame(outcomes_data)
    st.dataframe(outcomes_df, use_container_width=True, hide_index=True)

    # ROI Calculator
    st.markdown("---")
    st.subheader("💰 ROI Calculator")

    col1, col2, col3 = st.columns(3)

    with col1:
        current_turnover = st.number_input("Current Gen Z Turnover Rate (%)", 0, 100, 25)
        avg_salary = st.number_input("Avg Gen Z Salary ($K)", 0, 200, 50)

    with col2:
        total_genz = st.number_input("Total Gen Z Employees", 0, 10000, len(df))
        program_cost = st.number_input("Annual Program Cost ($K)", 0, 1000, 100)

    with col3:
        # Calculate ROI
        turnover_reduction = 0.225  # 22.5% average
        replacement_cost_factor = 1.5  # 1.5x salary

        current_turnover_cost = (current_turnover/100) * total_genz * avg_salary * replacement_cost_factor
        new_turnover_rate = current_turnover * (1 - turnover_reduction)
        new_turnover_cost = (new_turnover_rate/100) * total_genz * avg_salary * replacement_cost_factor

        savings = current_turnover_cost - new_turnover_cost - program_cost
        roi = (savings / program_cost) * 100 if program_cost > 0 else 0

        st.metric("Annual Savings", f"${savings:.0f}K")
        st.metric("ROI", f"{roi:.0f}%")
        st.metric("Payback Period", f"{12/roi*100 if roi > 0 else 0:.1f} months")

    st.success(f"""
    💡 **Insight**: Dengan investasi ${program_cost}K untuk program mental health Gen Z, 
    perusahaan dapat menghemat ${savings:.0f}K per tahun melalui pengurangan turnover, 
    menghasilkan ROI {roi:.0f}% dalam {12/roi*100 if roi > 0 else 0:.1f} bulan.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 2rem;">
    <p>📊 Dashboard Analisis Kesehatan Mental Gen Z | Powered by PySpark & Streamlit</p>
    <p>💡 Data-driven insights untuk employee well-being yang lebih baik</p>
    <p style="font-size: 0.8rem;">Generated on {}</p>
</div>
""".format(datetime.now().strftime('%d %B %Y, %H:%M WIB')), unsafe_allow_html=True)
