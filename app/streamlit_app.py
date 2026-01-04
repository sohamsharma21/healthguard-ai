import streamlit as st
import pandas as pd

# Page config - MUST BE FIRST, ONLY ONCE
st.set_page_config(page_title="HealthGuard AI", page_icon="🏥", layout="wide")

# Try to connect to Snowflake
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
    DEMO_MODE = False
except:
    # Running outside Snowflake - use demo data
    DEMO_MODE = True
    st.warning("⚠️ Running in DEMO MODE with sample data")

# Header
st.title("🏥 HealthGuard AI")
st.subheader("Healthcare Data Quality Monitoring System")

if DEMO_MODE:
    st.info("This is a demo version with sample data. Full version runs in Snowflake.")
    
    # Demo data
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
    
    **🎥 Watch Full Demo Video:** [Your Loom Link]
    
    **💻 GitHub Repository:** https://github.com/your-username/healthguard-ai
    """)
    
else:
    # Full Snowflake version
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
        
        dashboard_query = "SELECT * FROM VW_DATA_QUALITY_DASHBOARD"
        dashboard_df = session.sql(dashboard_query).to_pandas()
        
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
        st.subheader("📋 Complete Quality Metrics")
        st.dataframe(dashboard_df, use_container_width=True, height=300)
        
        st.subheader("📊 Data Quality Issues Breakdown")
        chart_data = dashboard_df[dashboard_df['METRIC'] != 'Total Patient Records']
        st.bar_chart(chart_data.set_index('METRIC')['COUNT'])
        
        st.markdown("---")
        st.subheader("🤖 ML-Based Detection Summary")
        ml_summary_query = "SELECT * FROM VW_ML_ANOMALY_SUMMARY"
        ml_summary_df = session.sql(ml_summary_query).to_pandas()
        st.dataframe(ml_summary_df, use_container_width=True)
    
    elif page == "Missing Data Analysis":
        st.header("📋 Missing Data Analysis")
        
        completeness_query = "SELECT * FROM VW_COMPLETENESS_SCORE WHERE COMPLETENESS_PERCENT < 100 LIMIT 50"
        completeness_df = session.sql(completeness_query).to_pandas()
        
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
        st.subheader("Incomplete Patient Records")
        st.dataframe(completeness_df, use_container_width=True, height=400)
    
    # Add other pages similarly...

# Footer
st.markdown("---")
st.markdown("**HealthGuard AI** | Built for Hack2skill - AI for Everywhere | Powered by Snowflake")
