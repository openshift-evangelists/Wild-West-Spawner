This repository contains a spawner for the Wild Wild West Way game. Deploy using the supplied template, then access the ``wild-west`` URL, and an instance of the game running in a new pod, will be created for you on demand. Close the browser window, and the pod will be deleted automatically after a period of inactivity. Multiple users can access the site at the same time and they will each get their own instance.

To deploy, run:

```
oc new-app https://raw.githubusercontent.com/openshift-evangelists/Wild-West-Spawner/master/template.json
```
