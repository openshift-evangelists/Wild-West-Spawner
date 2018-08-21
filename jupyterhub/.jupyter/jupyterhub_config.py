import os

c.KubeSpawner.cmd = ['/usr/libexec/s2i/run']

# Setup location for customised template files.

c.JupyterHub.template_paths = ['/opt/app-root/src/templates']

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
