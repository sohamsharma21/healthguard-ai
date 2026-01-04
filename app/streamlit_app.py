import streamlit as st
import pandas as pd

# Try to connect to Snowflake
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
    DEMO_MODE = False
except:
    # Running outside Snowflake - use demo data
    DEMO_MODE = True
    st.warning("⚠️ Running in DEMO MODE with sample data")

# Page config
st.set_page_config(page_title="HealthGuard AI", page_icon="🏥", layout="wide")

if DEMO_MODE:
    # Demo data for Streamlit Cloud
    st.title("🏥 HealthGuard AI - Demo Version")
    st.subheader("Healthcare Data Quality Monitoring System")
    st.info("This is a demo version with sample data. Full version runs in Snowflake.")
    
    # Create sample dashboard data
    demo_dashboard = pd.DataFrame({
        'METRIC': [
            'Total Patient Records',
            'Records with Missing Data',
            'Age Anomalies',
            'Blood Pressure Anomalies',
            'Heart Rate Anomalies',
            'Duplicate Patient Names',
            'Outdated Records (>1 year)'
        ],
        'COUNT': [200, 45, 3, 2, 2, 12, 15],
        'PERCENTAGE': ['100%', '22.5%', '1.5%', '1.0%', '1.0%', '6.0%', '7.5%']
    })
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", 200)
    with col2:
        st.metric("Incomplete Records", 45, delta="-45 issues")
    with col3:
        st.metric("Critical Anomalies", 7, delta="Urgent")
    
    st.markdown("---")
    st.subheader("📊 Data Quality Dashboard")
    st.dataframe(demo_dashboard, use_container_width=True)
    
    st.bar_chart(demo_dashboard.set_index('METRIC')['COUNT'])
    
    st.markdown("---")
    st.info("""
    **📺 Full Working Version Available:**
    - Runs entirely in Snowflake with real-time processing
    - 8 SQL views for comprehensive quality checks
    - ML-powered anomaly detection (Z-score analysis)
    - Interactive dashboard with 6 pages
    
    **🎥 Watch Full Demo Video:** [Insert your Loom/YouTube link]
    
    **💻 GitHub Repository:** https://github.com/your-username/healthguard-ai
    """)
    
else:
    # Original full Snowflake code
    # [Paste your complete original Streamlit code here]
    pass
# Import snowflake modules
from snowflake.snowpark.context import get_active_session
import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="HealthGuard AI", page_icon="🏥", layout="wide")

# Get Snowflake session
session = get_active_session()

# Header
st.title("🏥 HealthGuard AI")
st.subheader("Healthcare Data Quality Monitoring System")
st.markdown("---")

# Sidebar
st.sidebar.header("📊 Navigation")
page = st.sidebar.radio("Select View", 
    ["Dashboard Overview", "Missing Data Analysis", "Anomaly Detection", 
     "ML Statistical Detection", "Duplicate Records", "Patient Details"])

st.sidebar.markdown("---")
st.sidebar.info("**Built with:** Snowflake + Streamlit\n\n**Dataset:** 200 Patient Records")

# Main Dashboard
if page == "Dashboard Overview":
    st.header("📈 Data Quality Dashboard")
    
    # Fetch dashboard data
    dashboard_query = """
    SELECT * FROM VW_DATA_QUALITY_DASHBOARD
    """
    dashboard_df = session.sql(dashboard_query).to_pandas()
    
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_records = int(dashboard_df[dashboard_df['METRIC'] == 'Total Patient Records']['COUNT'].values[0])
        st.metric("Total Patient Records", total_records)
    
    with col2:
        missing_data = int(dashboard_df[dashboard_df['METRIC'] == 'Records with Missing Data']['COUNT'].values[0])
        st.metric("Incomplete Records", missing_data, delta=f"-{missing_data} issues")
    
    with col3:
        age_anomalies = int(dashboard_df[dashboard_df['METRIC'] == 'Age Anomalies']['COUNT'].values[0])
        st.metric("Age Anomalies", age_anomalies, delta="Critical")
    
    st.markdown("---")
    
    # Display full dashboard table
    st.subheader("📋 Complete Quality Metrics")
    st.dataframe(dashboard_df, use_container_width=True, height=300)
    
    # Bar chart
    st.subheader("📊 Data Quality Issues Breakdown")
    chart_data = dashboard_df[dashboard_df['METRIC'] != 'Total Patient Records']
    st.bar_chart(chart_data.set_index('METRIC')['COUNT'])
    
    # ML Summary section
    st.markdown("---")
    st.subheader("🤖 ML-Based Detection Summary")
    
    ml_summary_query = "SELECT * FROM VW_ML_ANOMALY_SUMMARY"
    ml_summary_df = session.sql(ml_summary_query).to_pandas()
    st.dataframe(ml_summary_df, use_container_width=True)

# Missing Data Analysis
elif page == "Missing Data Analysis":
    st.header("📋 Missing Data Analysis")
    
    completeness_query = """
    SELECT * FROM VW_COMPLETENESS_SCORE WHERE COMPLETENESS_PERCENT < 100 LIMIT 50
    """
    completeness_df = session.sql(completeness_query).to_pandas()
    
    # Summary stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Records with Missing Data", len(completeness_df))
    with col2:
        avg_completeness = completeness_df['COMPLETENESS_PERCENT'].mean()
        st.metric("Average Completeness", f"{avg_completeness:.1f}%")
    with col3:
        min_completeness = completeness_df['COMPLETENESS_PERCENT'].min()
        st.metric("Lowest Completeness", f"{min_completeness:.1f}%")
    
    st.markdown("---")
    
    # Data table
    st.subheader("Incomplete Patient Records")
    st.dataframe(completeness_df, use_container_width=True, height=400)

# Anomaly Detection
elif page == "Anomaly Detection":
    st.header("⚠️ Anomaly Detection")
    
    tab1, tab2, tab3 = st.tabs(["Age Anomalies", "Blood Pressure", "Heart Rate"])
    
    with tab1:
        age_query = "SELECT * FROM VW_AGE_ANOMALIES"
        age_df = session.sql(age_query).to_pandas()
        st.metric("Age Anomalies Found", len(age_df))
        st.dataframe(age_df, use_container_width=True)
    
    with tab2:
        bp_query = "SELECT * FROM VW_BP_ANOMALIES"
        bp_df = session.sql(bp_query).to_pandas()
        st.metric("Blood Pressure Anomalies", len(bp_df))
        st.dataframe(bp_df, use_container_width=True)
    
    with tab3:
        hr_query = "SELECT * FROM VW_HR_ANOMALIES"
        hr_df = session.sql(hr_query).to_pandas()
        st.metric("Heart Rate Anomalies", len(hr_df))
        st.dataframe(hr_df, use_container_width=True)

# ML Statistical Detection
elif page == "ML Statistical Detection":
    st.header("🤖 ML-Based Statistical Anomaly Detection")
    
    st.info("""
    **Advanced Statistical ML Approach:**
    - Uses Z-Score analysis (standard deviations from mean)
    - Z-score > 2: High anomaly (unusual pattern)
    - Z-score > 3: Critical anomaly (very rare occurrence)
    - Industry-standard method used in healthcare AI
    """)
    
    # Summary metrics
    summary_query = "SELECT * FROM VW_ML_ANOMALY_SUMMARY"
    summary_df = session.sql(summary_query).to_pandas()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        total_ml = int(summary_df[summary_df['METRIC'] == 'Statistical ML Anomalies Detected']['COUNT'].values[0])
        st.metric("Total ML Detected Anomalies", total_ml)
    with col2:
        critical = int(summary_df[summary_df['METRIC'] == 'Critical Severity Anomalies']['COUNT'].values[0])
        st.metric("Critical Severity", critical, delta="Urgent")
    with col3:
        high = int(summary_df[summary_df['METRIC'] == 'High Severity Anomalies']['COUNT'].values[0])
        st.metric("High Severity", high)
    
    st.markdown("---")
    
    # Detailed anomalies
    st.subheader("📊 Detected Anomalies with ML Scores")
    
    anomaly_query = """
    SELECT * FROM VW_STATISTICAL_ANOMALIES 
    WHERE IS_HR_ANOMALY = 'YES' OR IS_BP_ANOMALY = 'YES' OR IS_AGE_ANOMALY = 'YES'
    ORDER BY ANOMALY_SEVERITY DESC, HR_ZSCORE DESC
    """
    anomaly_df = session.sql(anomaly_query).to_pandas()
    
    st.dataframe(anomaly_df, use_container_width=True, height=400)
    
    # Breakdown by type
    st.markdown("---")
    st.subheader("📈 Anomaly Breakdown")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        hr_count = len(anomaly_df[anomaly_df['IS_HR_ANOMALY'] == 'YES'])
        st.metric("Heart Rate Anomalies", hr_count)
        
    with col2:
        bp_count = len(anomaly_df[anomaly_df['IS_BP_ANOMALY'] == 'YES'])
        st.metric("Blood Pressure Anomalies", bp_count)
        
    with col3:
        age_count = len(anomaly_df[anomaly_df['IS_AGE_ANOMALY'] == 'YES'])
        st.metric("Age Anomalies", age_count)
    
    # Severity distribution
    st.subheader("⚠️ Severity Distribution")
    severity_query = """
    SELECT ANOMALY_SEVERITY, COUNT(*) AS COUNT 
    FROM VW_STATISTICAL_ANOMALIES 
    WHERE ANOMALY_SEVERITY != 'NORMAL'
    GROUP BY ANOMALY_SEVERITY
    ORDER BY COUNT DESC
    """
    severity_df = session.sql(severity_query).to_pandas()
    
    if len(severity_df) > 0:
        st.bar_chart(severity_df.set_index('ANOMALY_SEVERITY'))
    else:
        st.info("No severity data to display")
    
    # Explanation expandable
    with st.expander("ℹ️ How does ML Statistical Detection work?"):
        st.write("""
        **Z-Score (Standard Score) Method:**
        
        1. **Calculate Mean & Standard Deviation** for each vital sign across all patients
        2. **Z-Score Formula:** `(Value - Mean) / Standard Deviation`
        3. **Interpretation:**
           - Z-score 0-1: Normal range (within 1 std dev)
           - Z-score 1-2: Slightly unusual
           - Z-score 2-3: **High Anomaly** (only 5% of data falls here)
           - Z-score > 3: **Critical Anomaly** (only 0.3% of data)
        
        **Why this is ML:**
        - Statistical machine learning technique
        - Used in healthcare AI systems globally
        - Automatically adapts to your dataset distribution
        - No manual threshold setting required
        
        **Real-world Application:**
        - FDA-approved medical devices use similar algorithms
        - Hospital ICU monitoring systems employ Z-score analysis
        - Clinical decision support systems rely on this method
        """)

# Duplicate Records
elif page == "Duplicate Records":
    st.header("👥 Duplicate Patient Names")
    
    dup_query = "SELECT * FROM VW_DUPLICATE_NAMES"
    dup_df = session.sql(dup_query).to_pandas()
    
    st.metric("Duplicate Name Groups Found", len(dup_df))
    
    if len(dup_df) > 0:
        total_dupes = int((dup_df['DUPLICATE_COUNT'] - 1).sum())
        st.metric("Total Duplicate Records", total_dupes)
    else:
        st.metric("Total Duplicate Records", 0)
    
    st.markdown("---")
    st.dataframe(dup_df, use_container_width=True)

# Patient Details
elif page == "Patient Details":
    st.header("🔍 Patient-wise Issues Summary")
    
    patient_query = """
    SELECT 
        P.PATIENT_ID,
        P.NAME,
        P.AGE,
        C.COMPLETENESS_PERCENT,
        CASE WHEN A.PATIENT_ID IS NOT NULL THEN 'Yes' ELSE 'No' END AS HAS_AGE_ISSUE,
        CASE WHEN B.PATIENT_ID IS NOT NULL THEN 'Yes' ELSE 'No' END AS HAS_BP_ISSUE,
        CASE WHEN H.PATIENT_ID IS NOT NULL THEN 'Yes' ELSE 'No' END AS HAS_HR_ISSUE
    FROM PATIENT_RECORDS P
    LEFT JOIN VW_COMPLETENESS_SCORE C ON P.PATIENT_ID = C.PATIENT_ID
    LEFT JOIN VW_AGE_ANOMALIES A ON P.PATIENT_ID = A.PATIENT_ID
    LEFT JOIN VW_BP_ANOMALIES B ON P.PATIENT_ID = B.PATIENT_ID
    LEFT JOIN VW_HR_ANOMALIES H ON P.PATIENT_ID = H.PATIENT_ID
    WHERE C.COMPLETENESS_PERCENT < 100 
       OR A.PATIENT_ID IS NOT NULL 
       OR B.PATIENT_ID IS NOT NULL 
       OR H.PATIENT_ID IS NOT NULL
    LIMIT 100
    """
    patient_df = session.sql(patient_query).to_pandas()
    
    st.metric("Patients with Data Quality Issues", len(patient_df))
    
    # Search functionality
    search = st.text_input("🔍 Search Patient by ID or Name")
    if search:
        patient_df = patient_df[
            (patient_df['PATIENT_ID'].str.contains(search, case=False)) | 
            (patient_df['NAME'].str.contains(search, case=False, na=False))
        ]
    
    st.dataframe(patient_df, use_container_width=True, height=500)

# Footer
st.markdown("---")
st.markdown("**HealthGuard AI** | Built for Hack2skill - AI for Everywhere | Powered by Snowflake")
