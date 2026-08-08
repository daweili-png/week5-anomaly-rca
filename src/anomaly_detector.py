import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score


def detect_anomalies(
    metrics_file,
    contamination=0.04
):
    """
    Detect anomalies in CPU, error rate,
    and p99 latency using Isolation Forest.
    """

    df = pd.read_csv(metrics_file)

    features = df[
        [
            "cpu_pct",
            "error_rate",
            "latency_p99_ms"
        ]
    ]

    scaler = StandardScaler()
    X = scaler.fit_transform(features)

    model = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=42
    )

    model.fit(X)

    df["anomaly_score"] = model.decision_function(X)

    df["is_anomaly"] = (
        model.predict(X) == -1
    )

    return df


def evaluate_detector(df):
    """
    Evaluate predictions against the known
    synthetic anomaly window: indices 200–215.
    """

    ground_truth = [
        1 if 200 <= i <= 215 else 0
        for i in range(len(df))
    ]

    predictions = (
        df["is_anomaly"]
        .astype(int)
        .tolist()
    )

    precision = precision_score(
        ground_truth,
        predictions
    )

    recall = recall_score(
        ground_truth,
        predictions
    )

    f1 = f1_score(
        ground_truth,
        predictions
    )

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "detected_anomalies": int(
            df["is_anomaly"].sum()
        )
    }


if __name__ == "__main__":

    result_df = detect_anomalies(
        "metrics_sample.csv",
        contamination=0.04
    )

    metrics = evaluate_detector(result_df)

    print("Anomaly Detection Results")
    print(metrics)