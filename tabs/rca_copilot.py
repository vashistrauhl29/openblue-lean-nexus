import streamlit as st
import pandas as pd
import time

def render_rca_copilot():
    st.header("RCA Copilot & Sustainment")
    
    vibration = st.session_state.get('current_vibration', 0.05)
    freq = st.session_state.get('dominant_freq', 'None (Noise Floor)')
    
    if vibration < 0.3:
        st.success(f"Asset #P-101 is operating within normal parameters. Current Vibration: {vibration} in/s. No active anomalies.")
    else:
        st.error(f"⚠️ CRITICAL ALERT: Vibration {vibration} in/s detected on Asset #P-101")
        st.info(f"**Spectral Analysis Result:** Strong peak detected at {freq}.")
        
        st.subheader("Step 1: Automated Diagnostics (FMEA)")
        
        if vibration > 0.5:
            data = [
                ["Mechanical Looseness", "80%", "1x RPM Harmonics", "Check mounting bolts & baseplate"],
                ["Structural Resonance", "15%", "Natural Frequency Match", "Impact test foundation"],
                ["Other", "5%", "Various", "General inspection required"]
            ]
        else:
            data = [
                ["Misalignment", "60%", "2x RPM Radial", "Laser alignment required"],
                ["Bearing Wear", "30%", "High Frequency Noise", "Grease analysis / Replacement"],
                ["Cavitation", "10%", "Random Low Frequency", "Check suction valve & NPSH"]
            ]
            
        df = pd.DataFrame(data, columns=["Potential Failure Mode", "Probability", "Spectral Signature", "Recommended Inspection"])
        st.table(df)
        
        st.subheader("Step 2: AI-Generated Solution")
        if st.button("Generate Sustainment SOP"):
            with st.spinner("Querying OpenBlu Knowledge Base..."):
                time.sleep(2)
                st.markdown("""
                ## **Standard Work: Laser Shaft Alignment (JCMS-M-04)**
                
                ### **Required Tools**
                *   Precision Laser Alignment Kit (e.g., Fluke/Pruftechnik)
                *   Calibrated Torque Wrench
                *   Stainless Steel Shim Pack
                
                ### **Safety (LOTO)**
                1.  Perform Electrical Lock-Out Tag-Out on Pump #P-101 Main Breaker.
                2.  Verify Zero Energy State.
                3.  Secure discharge/suction valves.
                
                ### **Step-by-Step Execution**
                1.  **Rough Alignment:** Perform preliminary visual alignment and check for 'Soft Foot'.
                2.  **Mounting:** Attach laser heads to motor and pump shafts.
                3.  **Measurement:** Rotate shafts 180 degrees to capture vertical and horizontal misalignment.
                4.  **Correction:** Add/Remove shims as calculated by the laser tool.
                5.  **Verification:** Re-measure and ensure tolerance is within ±0.002 inches.
                6.  **Finalize:** Torque bolts to 85 ft-lbs and restore power.
                """)
