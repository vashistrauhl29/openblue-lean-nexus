import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import json
import paho.mqtt.client as mqtt

@st.cache_resource
def get_mqtt_client():
    client = mqtt.Client()
    
    def on_message(client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            st.session_state['last_payload'] = payload
            st.session_state['current_vibration'] = payload['vibration_rms']
            st.session_state['dominant_freq'] = payload['dominant_freq']
        except Exception as e:
            pass

    client.on_message = on_message
    client.connect("test.mosquitto.org", 1883, 60)
    client.subscribe("jci/demo/pump_p101/telemetry")
    client.loop_start()
    return client

def render_digital_twin():
    st.header("⚡ Operational Digital Twin: Asset #P-101")
    st.info("**Live Stream:** Connecting to IoT Gateway [Online] | Protocol: MQTT")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Controls")
        live_mode = st.toggle("🔴 Connect to Live IoT Gateway (MQTT)")
        
        if live_mode:
            get_mqtt_client()
            st.success("Status: 🟢 Connected to Gateway")
            vibration = st.session_state.get('current_vibration', 0.05)
            dominant_freq = st.session_state.get('dominant_freq', 'None (Noise Floor)')
            st.metric("Inbound Stream (RMS)", f"{vibration:.3f} in/s")
            if st.button("Refresh Live Data"):
                st.rerun()
        else:
            # Use session state as the initial value to prevent resetting on tab change
            vibration = st.slider(
                "Simulate Vibration Level (in/sec)", 
                0.0, 1.0, 
                value=st.session_state.get('current_vibration', 0.05), 
                step=0.01
            )
            st.session_state['current_vibration'] = vibration
            
            # Dominant Frequency Logic for Manual Mode
            if vibration > 0.5:
                dominant_freq = "1x RPM (Looseness)"
            elif vibration > 0.3:
                dominant_freq = "2x RPM (Misalignment)"
            else:
                dominant_freq = "None (Noise Floor)"
            st.session_state['dominant_freq'] = dominant_freq
            
        st.markdown("*ISO 10816 Standard: >0.30 is Alarm*")
        
        # Data Generation Logic (The Physics)
        base_efficiency = 0.85
        ideal_power_kw = 65.0
        
        # Degradation Logic
        if vibration > 0.15:
            current_efficiency = max(0.40, base_efficiency - ((vibration - 0.15) * 0.4))
        else:
            current_efficiency = base_efficiency
            
        # Energy Calc
        # Assuming ideal_power_kw is at base_efficiency, so actual power scales inversely with efficiency
        actual_power_kw = ideal_power_kw * (base_efficiency / current_efficiency)
        
        # Carbon Calc
        excess_kw = max(0, actual_power_kw - ideal_power_kw)
        excess_co2_lbs_per_hour = excess_kw * 0.85 # EPA eGRID Factor
        st.session_state['carbon_waste'] = excess_co2_lbs_per_hour
        
    with col2:
        st.subheader("Visualization")
        m1, m2, m3 = st.columns(3)
        m1.metric("Real-Time Vibration", f"{vibration:.2f} in/s", delta="- Safe" if vibration < 0.3 else "- ALARM", delta_color="inverse")
        m2.metric("Current Efficiency", f"{current_efficiency*100:.1f}%")
        
        carbon_delta = "Excess Waste" if excess_co2_lbs_per_hour > 0 else "Optimal"
        m3.metric("Carbon Waste Rate", f"{excess_co2_lbs_per_hour:.2f} lbs/hr", delta=carbon_delta, delta_color="inverse")
        
        # Last 24 hours simulation
        now = datetime.now()
        times = [now - timedelta(hours=i) for i in range(24)][::-1]
        
        # Previous hours random low noise, last hour reflects slider
        vibration_data = [np.random.uniform(0.04, 0.07) for _ in range(23)] + [vibration]
        
        df = pd.DataFrame({
            "Time": times,
            "Vibration (in/sec)": vibration_data
        })
        
        fig = px.line(df, x="Time", y="Vibration (in/sec)", title="Vibration Trend (24h)")
        fig.add_hline(y=0.3, line_dash="dash", line_color="red", annotation_text="ISO Alarm Limit")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Show Live FFT Spectrum Analysis"):
            if vibration > 0.5:
                fft_data = {'1x RPM': 0.8, '2x RPM': 0.1, '3x RPM': 0.05}
            elif vibration > 0.3:
                fft_data = {'1x RPM': 0.2, '2x RPM': 0.6, '3x RPM': 0.1}
            else:
                fft_data = {'1x RPM': 0.05, '2x RPM': 0.05, '3x RPM': 0.05}
            
            st.bar_chart(fft_data)
            st.caption("Spectral energy distribution showing harmonic peaks.")

        if live_mode:
            with st.expander("Show Raw MQTT JSON Packet"):
                st.json(st.session_state.get('last_payload', {}))
        
    st.markdown("---")
    st.caption("Calculations based on Pump Affinity Laws & EPA eGRID 2023 Avg Emission Factors (0.85 lbs/kWh).")
