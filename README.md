# Week 5 — Intelligent Anomaly Detection and RCA

## Overview

This project implements a small end-to-end anomaly detection and root cause analysis system.

The system:

1. Detects anomalies in application metrics using Isolation Forest.
2. Evaluates anomaly detection using precision, recall, and F1 score.
3. Groups related alerts into incidents using a time-window rule.
4. Uses an RCA agent with two tools to analyze metrics and logs.
5. Emits OpenTelemetry GenAI spans for agent observability.

---

## Project Structure

```text
data/
    logs_sample.txt

src/
    anomaly_detector.py
    alert_grouper.py
    rca_agent.py
    telemetry.py

output/
    rca_report.md
    spans_sample.json

analysis.ipynb
metrics_sample.csv
metrics_overview.png
detected_anomalies.png
contamination_comparison.png
README.md