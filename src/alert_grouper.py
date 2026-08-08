import pandas as pd


def create_alerts(df):
    """
    Convert detected anomalies into alert records.
    """

    alerts = []

    anomaly_rows = df[df["is_anomaly"]].copy()

    for _, row in anomaly_rows.iterrows():

        alerts.append({
            "timestamp": row["timestamp"],
            "cpu_pct": row["cpu_pct"],
            "error_rate": row["error_rate"],
            "latency_p99_ms": row["latency_p99_ms"]
        })

    return pd.DataFrame(alerts)


def group_alerts(alerts_df, window_minutes=5):
    """
    Group alerts that occur within a specified time window
    into the same incident.
    """

    alerts_df = alerts_df.sort_values("timestamp").reset_index(drop=True)

    incident_ids = []

    current_incident = 1
    previous_time = None

    for _, row in alerts_df.iterrows():

        current_time = pd.to_datetime(row["timestamp"])

        if previous_time is None:
            incident_ids.append(current_incident)

        else:
            time_difference = (
                current_time - previous_time
            ).total_seconds() / 60

            if time_difference > window_minutes:
                current_incident += 1

            incident_ids.append(current_incident)

        previous_time = current_time

    alerts_df["incident_id"] = incident_ids

    return alerts_df


if __name__ == "__main__":

    df = pd.read_csv("metrics_sample.csv")

    print("This module provides alert grouping functions.")