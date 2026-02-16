import streamlit as st
import pandas as pd
import time

def render_strategy():
    st.header("Hoshin Kanri: Strategy-to-Action Cascade")
    
    pillar = st.selectbox("Select Strategic Pillar", ["Sustainability (Net Zero)", "Operational Excellence (JCMS)", "Safety (Zero Harm)"])
    
    # Retrieve Data
    waste = st.session_state.get('carbon_waste', 0.0)
    vibration = st.session_state.get('current_vibration', 0.05)
    
    # Dynamic Logic Block
    l1_goal = ""
    l1_metric = ""
    l2_goal = ""
    deviation_msg = ""
    
    if pillar == "Sustainability (Net Zero)":
        l1_goal = "Achieve Net Zero Scope 1 & 2 by 2040"
        l1_metric = "Target: 0 Emissions"
        l2_goal = "Reduce Energy Intensity by 15%"
        deviation_msg = f"{waste:.2f} lbs/hr excess carbon from Assets"
    
    elif pillar == "Operational Excellence (JCMS)":
        l1_goal = "Top Decile Reliability & Margins"
        l1_metric = "Target: >95% OEE"
        l2_goal = "Optimize Asset Uptime & Maintenance Cost"
        # Cost Calc: waste / 0.85 = excess_kw. excess_kw * $0.12 * 24 * 365
        excess_kw = waste / 0.85 if waste > 0 else 0
        annual_cost = excess_kw * 0.12 * 24 * 365
        deviation_msg = f"${annual_cost:,.0f} / yr excess energy waste"
        
    elif pillar == "Safety (Zero Harm)":
        l1_goal = "Zero Harm / Zero Recordables"
        l1_metric = "Target: 0 TRIR"
        l2_goal = "Eliminate Process Safety Events (LOPC)"
        risk_level = "High" if vibration > 0.3 else "Low"
        deviation_msg = f"{risk_level} Risk of Mechanical Seal Failure (Leakage)"
        
    # Status Logic
    if vibration > 0.3:
        status = "AT RISK"
        color = "red"
    else:
        status = "ON TRACK"
        color = "green"
        
    st.divider()
    
    # Visualization (3 Columns)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("L1: Corporate Goal")
        st.info(f"**{l1_goal}**")
        st.metric("Target", l1_metric)
        st.caption("Owner: CEO / Board")
        
    with col2:
        st.subheader("L2: Plant Level")
        st.info(f"**{l2_goal}**")
        st.markdown(f"**Status:** :{color}[{status}]")
        if vibration > 0.3:
            st.warning(f"⚠️ Deviation Detected: {deviation_msg}")
        st.caption("Owner: Plant Manager - Milwaukee")
        
    with col3:
        st.subheader("L3: Daily Standard Work")
        st.info("**Maintain Rotary Asset Efficiency**")
        if st.button("View Live Asset Health"):
            st.info("Navigate to 'Operational Digital Twin' to view details.")
        st.caption("Owner: Maintenance Supervisor / Shop Floor")

    st.divider()
    
    # The "AI" Element
    if st.button("Generate Monthly X-Matrix"):
        with st.spinner("AI Agent aligning KPIs..."):
            time.sleep(1.5)
            st.success("X-Matrix Updated: Linked P-101 Reliability to Business Impact Targets.")
            
            # Create a Mock X-Matrix Data Structure
            data = {
                "Strategic Goal (L1)": ["Net Zero Scope 1", "Reduce OpEx 10%", "Zero Harm"],
                "Tactical Project (L2)": ["P-101 Optimization", "Energy Audit", "Safety Interlocks"],
                "Shop Floor Action (L3)": ["Laser Alignment", "VFD Tuning", "Seal Guard Install"],
                "Correlation": ["Strong (●)", "Medium (○)", "Strong (●)"],
                "Owner": ["R. Vashisht", "Plant Mgr", "EHS Lead"]
            }
            df_matrix = pd.DataFrame(data)
            
            # Display it cleanly
            st.markdown("### 📋 Generated Policy Deployment Matrix (X-Matrix)")
            st.dataframe(df_matrix, use_container_width=True, hide_index=True)
            st.caption("✅ AI Agent has correlated 'P-101 Reliability' to 'Net Zero Scope 1' with Strong Correlation (●).")
            st.info("ℹ️ Note: This output is simulated for prototype speed. In production, this would call the OpenBlu GenAI API.")
