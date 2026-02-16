# OpenBlu Lean Nexus

A Streamlit-based operational dashboard for Johnson Controls, bridging the gap between high-level **Net Zero** strategies and **Shop Floor** execution.

## Features

*   **Strategy Deployment (Hoshin Kanri):** Visualize the cascade of corporate goals (L1) to shop floor actions (L3).
*   **Operational Digital Twin:** Real-time monitoring of asset health (e.g., Pump #P-101) with simulated or live MQTT data.
*   **RCA Copilot:** AI-assisted root cause analysis and sustainment workflows.

## Getting Started

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application:**
    ```bash
    streamlit run app.py
    ```

3.  **Simulate IoT Data (Optional):**
    Open a separate terminal and run:
    ```bash
    python mock_sensor.py
    ```
    Then, toggle "Connect to Live IoT Gateway" in the Digital Twin module.

## Project Structure

*   `app.py`: Main entry point.
*   `tabs/`: Contains the module logic (`digital_twin.py`, `strategy.py`, `rca_copilot.py`).
*   `mock_sensor.py`: Script to simulate MQTT data for the Digital Twin.
