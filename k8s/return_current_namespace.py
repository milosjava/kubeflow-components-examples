def get_current_namespace():
    """Returns current namespace if available, else kubeflow"""
    try:
        namespace = "/var/run/secrets/kubernetes.io/serviceaccount/namespace"
        current_namespace = open(namespace).read()
    except FileNotFoundError:
        current_namespace = "kubeflow"
    return current_namespace