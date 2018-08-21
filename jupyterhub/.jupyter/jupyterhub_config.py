import os

c.KubeSpawner.cmd = ['/usr/libexec/s2i/run']

# Override URL prefix for front end instance.

def modify_pod_hook(spawner, pod):
    pod.spec.containers[0].env.append(dict(name='URL_PREFIX',
            value='/user/%s' % spawner.user.name))
    pod.spec.containers[0].env.append(dict(name='BACKEND_SERVICE',
            value='http://wild-west-town-backend:8080/'))

    return pod

c.KubeSpawner.modify_pod_hook = modify_pod_hook

# Setup culling of idle notebooks if timeout parameter is supplied.

idle_timeout = os.environ.get('JUPYTERHUB_IDLE_TIMEOUT')

if idle_timeout and int(idle_timeout):
    c.JupyterHub.services = [
        {
            'name': 'cull-idle',
            'admin': True,
            'command': ['cull-idle-servers', '--timeout=%s' % idle_timeout],
        }
    ]
