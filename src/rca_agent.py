import pandas as pd


def get_metric_context(metrics_file, start_time, end_time):
    """
    Tool 1:
    Retrieve metric evidence for a specific incident window.
    """

    df = pd.read_csv(metrics_file)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)

    incident_data = df[
        (df["timestamp"] >= start_time)
        & (df["timestamp"] <= end_time)
    ]

    if incident_data.empty:
        return {
            "max_cpu_pct": None,
            "max_error_rate": None,
            "max_latency_p99_ms": None
        }

    return {
        "max_cpu_pct": round(
            incident_data["cpu_pct"].max(), 2
        ),
        "max_error_rate": round(
            incident_data["error_rate"].max(), 4
        ),
        "max_latency_p99_ms": round(
            incident_data["latency_p99_ms"].max(), 2
        )
    }


def get_log_context(log_file, start_time, end_time):
    """
    Tool 2:
    Retrieve relevant log lines for an incident window.
    """

    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)

    matching_logs = []

    with open(log_file, "r", encoding="utf-8") as f:

        for line in f:

            try:
                timestamp_text = line[:19]
                timestamp = pd.to_datetime(timestamp_text)

                if start_time <= timestamp <= end_time:
                    matching_logs.append(line.strip())

            except Exception:
                continue

    return matching_logs


def generate_rca(metrics_file, log_file, start_time, end_time):
    """
    Simulated RCA agent using two tools:
    1. get_metric_context()
    2. get_log_context()
    """

    metrics = get_metric_context(
        metrics_file,
        start_time,
        end_time
    )

    logs = get_log_context(
        log_file,
        start_time,
        end_time
    )

    database_errors = [
        line for line in logs
        if "database" in line.lower()
        or "connection" in line.lower()
    ]

    timeout_errors = [
        line for line in logs
        if "timeout" in line.lower()
    ]

    if database_errors:
        root_cause = (
            "Database connection pool exhaustion likely caused "
            "application requests to wait for database connections."
        )
    else:
        root_cause = (
            "The exact root cause is uncertain and requires "
            "further investigation."
        )

    evidence = [
        f"Peak CPU: {metrics['max_cpu_pct']}%",
        f"Peak error rate: {metrics['max_error_rate']}",
        f"Peak p99 latency: {metrics['max_latency_p99_ms']} ms",
        f"Relevant log lines: {len(logs)}",
        f"Database-related log events: {len(database_errors)}",
        f"Timeout events: {len(timeout_errors)}"
    ]

    recommendations = [
        "Increase or dynamically scale the database connection pool.",
        "Add monitoring for database connection pool utilization.",
        "Configure timeout and retry limits.",
        "Add alerts before p99 latency reaches a critical level."
    ]

    return {
        "incident_window": f"{start_time} to {end_time}",
        "root_cause": root_cause,
        "evidence": evidence,
        "recommendations": recommendations
    }