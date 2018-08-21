import os

# Override image details with that of the front end.

spawner_name = os.environ.get('SPAWNER_NAME')

c.KubeSpawner.hub_connect_ip = spawner_name

c.KubeSpawner.singleuser_image_spec = os.environ.get(
        'FRONTEND_IMAGE', 'wild-west-frontend:latest')

c.KubeSpawner.cmd = ['/usr/libexec/s2i/run']

c.KubeSpawner.pod_name_template = '%s-frontend-{username}' % (
        c.KubeSpawner.hub_connect_ip)

c.KubeSpawner.common_labels = { 'app': spawner_name }

c.Spawner.mem_limit = convert_size_to_bytes('256Mi')

# Override URL prefix for front end instance and link to the back end.

from openshift import client, config

with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace') as fp:
    namespace = fp.read().strip()

config.load_incluster_config()
oapi = client.OapiApi()

routes = oapi.list_namespaced_route(namespace)

def extract_hostname(routes, name):
    for route in routes.items:
        if route.metadata.name == name:
            return route.spec.host

route_hostname = extract_hostname(routes, '%s-backend' % spawner_name)

def modify_pod_hook(spawner, pod):
    pod.spec.containers[0].env.append(dict(name='URL_PREFIX',
            value='/user/%s' % spawner.user.name))
    pod.spec.containers[0].env.append(dict(name='BACKEND_SERVICE',
            value='http://%s' % route_hostname))

    return pod

c.KubeSpawner.modify_pod_hook = modify_pod_hook

# Setup culling of front end instance if timeout parameter is supplied.

idle_timeout = os.environ.get('IDLE_TIMEOUT')

if idle_timeout and int(idle_timeout):
    c.JupyterHub.services = [
        {
            'name': 'cull-idle',
            'admin': True,
            'command': ['cull-idle-servers', '--timeout=%s' % idle_timeout],
        }
    ]
