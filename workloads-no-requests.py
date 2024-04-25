from kubernetes import client, config


def get_kubernetes_api_client():
    # Load kubeconfig from default location
    config.load_kube_config()

    # Create and return Kubernetes API client
    return client.CoreV1Api()


def list_workloads_with_no_cpu_requests(api_instance):
    workloads_with_no_cpu_requests = []

    # List all pods in the cluster
    pods = api_instance.list_pod_for_all_namespaces(watch=False)

    # Iterate through each pod and check if it has no CPU requests
    for pod in pods.items:
        containers = pod.spec.containers
        for container in containers:
            resources = container.resources
            if resources and resources.requests and 'cpu' not in resources.requests:
                workloads_with_no_cpu_requests.append(f"{pod.metadata.namespace}/{pod.metadata.name}")

    return workloads_with_no_cpu_requests


def list_workloads_with_no_memory_requests(api_instance):
    workloads_with_no_memory_requests = []

    # List all pods in the cluster
    pods = api_instance.list_pod_for_all_namespaces(watch=False)

    # Iterate through each pod and check if it has no memory requests
    for pod in pods.items:
        containers = pod.spec.containers
        for container in containers:
            resources = container.resources
            if resources and resources.requests and 'memory' not in resources.requests:
                workloads_with_no_memory_requests.append(f"{pod.metadata.namespace}/{pod.metadata.name}")

    return workloads_with_no_memory_requests


if __name__ == "__main__":
    # Get Kubernetes API client
    api_instance = get_kubernetes_api_client()

    # List workloads with no CPU requests
    no_cpu_request_workloads = list_workloads_with_no_cpu_requests(api_instance)
    print("Workloads with no CPU requests:")
    for workload in no_cpu_request_workloads:
        print(workload)

    # List workloads with no memory requests
    no_memory_request_workloads = list_workloads_with_no_memory_requests(api_instance)
    print("\nWorkloads with no memory requests:")
    for workload in no_memory_request_workloads:
        print(workload)
