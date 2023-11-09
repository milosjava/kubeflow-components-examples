


@component(
    base_image="python:3.9",
)
def return_spec(
    experiment_name: str,
    namespace: str,
    runid: str,
    asin: str,
    maxTrialCount: int,
    maxFailedTrialCount: int,
    parallelTrialCount: int,
    image: str,
    output: Output[Artifact]
) :
    import json

    spec = {"algorithm": {"algorithmName": "random"}, "maxFailedTrialCount": maxFailedTrialCount, "maxTrialCount": maxTrialCount,
            "objective": {"objectiveMetricName": "total_prediction_error", "type": "minimize"}, "parallelTrialCount": parallelTrialCount,
            "parameters": [
                {"feasibleSpace": {"max": "239", "min": "0"}, "name": "priors_file_id", "parameterType": "int"}],
            "resumePolicy": "LongRunning", "trialTemplate": {"primaryContainerName": "training-container",
                                                             "trialParameters": [{"description": "priors_file_id",
                                                                                  "name": "priors_file_id",
                                                                                  "reference": "priors_file_id"}],
                                                             "trialSpec": {"apiVersion": "batch/v1", "kind": "Job",
                                                                           "spec": {"template": {"metadata": {
                                                                               "annotations": {
                                                                                   "sidecar.istio.io/inject": "false"}},
                                                                                                 "spec": {
                                                                                                     "containers": [{
                                                                                                                        "name": "training-container",
                                                                                                                        "image": image,
                                                                                                                        "command": [
                                                                                                                            "python3",
                                                                                                                            "model.py",
                                                                                                                            "--artifact_type=amz_sales_experiment_metadata_v1",
                                                                                                                            f"--namespace={namespace}",
                                                                                                                            "--priors_file_id=${trialParameters.priors_file_id}",
                                                                                                                            "--azure_blob_account_url=https://kubeflownonprod94136.blob.core.windows.net",
                                                                                                                            "--container_name=kubeflow-content",
                                                                                                                            f"--asin={asin}",
                                                                                                                            f"--experiment_name={experiment_name}",
                                                                                                                            f"--preprocess_blob_name=v2/artifacts/pipeline/amz-sales-driver-pipeline/{runid}/preprocess-data/preprocess_{asin}.pkl",
                                                                                                                            f"--featureeng_blob_name=v2/artifacts/pipeline/amz-sales-driver-pipeline/{runid}/feature-engineering/featureeng_{asin}.pkl"],
                                                                                                                        "env": [
                                                                                                                            {
                                                                                                                                "name": "SECRET_KEY",
                                                                                                                                "valueFrom": {
                                                                                                                                    "secretKeyRef": {
                                                                                                                                        "name": "mlpipeline-minio-artifact",
                                                                                                                                        "key": "secretkey"}}},
                                                                                                                            {
                                                                                                                                "name": "ACCESS_KEY",
                                                                                                                                "valueFrom": {
                                                                                                                                    "secretKeyRef": {
                                                                                                                                        "name": "mlpipeline-minio-artifact",
                                                                                                                                        "key": "accesskey"}}},
                                                                                                                            {
                                                                                                                                "name": "AZURE_STORAGE_KEY",
                                                                                                                                "valueFrom": {
                                                                                                                                    "secretKeyRef": {
                                                                                                                                        "name": "azcreds",
                                                                                                                                        "key": "AZURE_STORAGE_KEY"}}},
                                                                                                                            {
                                                                                                                                "name": "AZURE_CLIENT_ID",
                                                                                                                                "valueFrom": {
                                                                                                                                    "secretKeyRef": {
                                                                                                                                        "name": "azcreds",
                                                                                                                                        "key": "AZ_CLIENT_ID"}}},
                                                                                                                            {
                                                                                                                                "name": "AZURE_CLIENT_SECRET",
                                                                                                                                "valueFrom": {
                                                                                                                                    "secretKeyRef": {
                                                                                                                                        "name": "azcreds",
                                                                                                                                        "key": "AZ_CLIENT_SECRET"}}},
                                                                                                                            {
                                                                                                                                "name": "AZURE_SUBSCRIPTION_ID",
                                                                                                                                "valueFrom": {
                                                                                                                                    "secretKeyRef": {
                                                                                                                                        "name": "azcreds",
                                                                                                                                        "key": "AZ_SUBSCRIPTION_ID"}}},
                                                                                                                            {
                                                                                                                                "name": "AZURE_TENANT_ID",
                                                                                                                                "valueFrom": {
                                                                                                                                    "secretKeyRef": {
                                                                                                                                        "name": "azcreds",
                                                                                                                                        "key": "AZ_TENANT_ID"}}}],
                                                                                                                        "resources": {
                                                                                                                            "limits": {
                                                                                                                                "cpu": "1",
                                                                                                                                "memory": "4Gi"},
                                                                                                                            "requests": {
                                                                                                                                "cpu": "1",
                                                                                                                                "memory": "4Gi"}}}],
                                                                                                     "restartPolicy": "Never"}}}}}}

    with open(output.path, 'w') as f:
        json.dump(spec, f)