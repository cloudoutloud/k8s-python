from kubernetes import client, config

def has_pod_anti_affinity(pod_spec):
    # Check if pod anti-affinity is defined for the pod
    return (
        pod_spec.affinity
        and pod_spec.affinity.pod_anti_affinity
        and (
            pod_spec.affinity.pod_anti_affinity.required_during_scheduling_ignored_during_execution
            or pod_spec.affinity.pod_anti_affinity.preferred_during_scheduling_ignored_during_execution
        )
    )

def get_workloads_with_anti_affinity(api_instance):
    workloads_with_anti_affinity = []

    try:
        # Retrieve all deployments across all namespaces
        all_namespaces_deployments = api_instance.list_deployment_for_all_namespaces()

        for deployment in all_namespaces_deployments.items:
            # Check if any pod in the deployment has anti-affinity
            for container in deployment.spec.template.spec.containers:
                if has_pod_anti_affinity(deployment.spec.template.spec):
                    workloads_with_anti_affinity.append(deployment.metadata.name)
                    break  # No need to check other containers in the same deployment

    except Exception as e:
        # Handle exceptions and print an error message
        print(f"Error while retrieving workloads: {e}")

    return workloads_with_anti_affinity

def main():
    try:
        # Load Kubernetes configuration from default location
        config.load_kube_config()

        # Create an instance of the Kubernetes API client
        api_instance = client.AppsV1Api()

        # Get workloads with pod anti-affinity across all namespaces
        workloads_with_anti_affinity = get_workloads_with_anti_affinity(api_instance)

        if workloads_with_anti_affinity:
            print("Workloads with Pod Anti-Affinity:")
            for workload in workloads_with_anti_affinity:
                print(f"- {workload}")
        else:
            print("No workloads with Pod Anti-Affinity found in any namespace.")

    except Exception as e:
        # Handle exceptions and print an error message
        print(f"Error: {e}")

if __name__ == "__main__":
    main()