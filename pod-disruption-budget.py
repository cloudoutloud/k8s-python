from kubernetes import client, config

def get_pdb_names(api_instance):

    try:
        ##  Retrieve all pdb across all namespaces
        all_pdb_across_all_namespaces  = api_instance.list_pod_disruption_budget_for_all_namespaces()

        # Extracting the 'name' field from each PodDisruptionBudget
        pdb_names = [item.metadata.name for item in all_pdb_across_all_namespaces.items]

        return pdb_names

    except Exception as e:
        # Handle exceptions and print an error message
        print(f"Error while retrieving workloads: {e}")

def main():
    try:
        # Load Kubernetes configuration from default location
        config.load_kube_config()

        # Create an instance of the Kubernetes API client
        api_instance = client.PolicyV1Api()

        pod_disruption_budget_names = get_pdb_names(api_instance)

        if pod_disruption_budget_names:
            print("PodDisruptionBudget Names:")
            for name in pod_disruption_budget_names:
                print(f"- {name}")
        else:
            print("No PodDisruptionBudgets found.")

    except Exception as e:
        # Handle exceptions and print an error message
        print(f"Error: {e}")

if __name__ == "__main__":
    main()