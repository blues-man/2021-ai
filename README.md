# MLOps: AI Model 

## Setup

* Get an OpenShift 4.7+ cluster.
* Install **OpenShift Pipelines**, **OpenShift GitOps** and **CodeReady Workspaces** operators from OperatorHub.

### Setup CI

CI is implemented via OpenShift Pipelines. We also use Gogs are Git server for storing source code and Kubernetes manifests controlled by OpenShift GitOps.


```
oc new-project mlops-ci
oc create -f openshift/tekton/tasks
oc create -f openshift/tekton/pipelines
oc create -f openshift/tekton/triggers
oc create -f openshift/gogs/gogs.yaml
GOGS_HOSTNAME=$(oc get route gogs -o template --template='{{.spec.host}}')
sed "s/@HOSTNAME/$GOGS_HOSTNAME/g" openshift/gogs/gogs-configmap.yaml | oc create -f -
oc rollout status deployment/gogs
oc create -f openshift/gogs/gogs-init-taskrun.yaml
```

#### Setup Quay.io

Create a repository on Quay.io and add your credentials to the `mlops-ci` project as follow:

1. Get credentials

* Login to quay.io in the web user interface and click on your username in the top right corner.
* Select **account settings**.
* Click the blue hyperlink **Generate Encrypted Password**.
* Re-enter your password when prompted.
* Copy the password

2. Create a Secret with your Quay.io credentials with the encrypted password you copied before:

```bash
oc create secret docker-registry quay-secret --docker-server=quay.io --docker-username=<QUAY_USERNAME> --docker-password=<ENCRYPTED_PASSWORD>
```


3. Link Secret to pipeline Service Account.

NOTE: Pipelines Operator installs by default a `pipeline` Service Account in all projects. This service account is used to run non-privileged containers and builds across the cluster.  

```bash
oc secret link pipeline quay-secret
```

### Setup CD

Give permissions to Argo CD to control cluster:

```
oc adm policy add-cluster-role-to-user cluster-admin -z openshift-gitops-argocd-application-controller -n openshift-gitops
```

Install AI Model Application into `mlops` project, syncing the Gogs repo:
```
GOGS_HOSTNAME=$(oc get route gogs -o template --template='{{.spec.host}}')
curl -s https://raw.githubusercontent.com/blues-man/2021-ai-gitops/main/argo/ai-model.yaml | sed -E 's/repoURL:(.*)/repoURL: https:\/\/'$GOGS_HOSTNAME'\/gogs\/2021-ai-gitops/'   | oc apply -f -
```

## Start Pipeline

Download `tkn` CLI or start the pipeline from OpenShift Web Console with these parameters:

* **APP_GIT_REPO**: Gogs app repo
* **APP_GIT_MANIFESTS_EPO**: Gogs manifests repo
* **workspace**: Select PVC, then **app-source-pvc**

```
tkn pipeline start ml-pipeline -w name=workspace,claimName=app-source-pvc -p APP_GIT_REPO=https://$GOGS_HOSTNAME/gogs/2021-ai -p APP_GIT_MANIFESTS_REPO=https://$GOGS_HOSTNAME/gogs/2021-ai-gitops --showlog

```


## Edit in CodeReady Workspaces

If you are running on a cluster with [CodeReady Workspaces](https://developers.redhat.com/products/codeready-workspaces/overview) like [Developer Sandbox](https://developers.redhat.com/developer-sandbox), you can start editing it directly from there.

Run it with [Eclipse Che Factories](https://developers.redhat.com/che/creating-factories):

NOTE: Change the address of Factory with your CRW URL

[![Contribute](https://raw.githubusercontent.com/blues-man/nodejs-mongodb-sample/master/factory-contribute.svg)](https://codeready-openshift-workspaces.apps.cluster-b237.b237.sandbox1343.opentlc.com/factory?url=https://github.com/blues-man/2021-ai.git)

## Development 

### Create model Image  
```
make build
make push
```

### Deployment  
```
oc create -f https://raw.githubusercontent.com/rhdemo/2021-ai/master/install/deployment.yml
oc new-app --template=demo-2021-ai
```

### cleanup
```
oc delete template demo-2021-ai
oc delete all -l app=demo-2021-ai
oc delete route demo-2021-ai
```


--



### Deploy 
```
▶ oc new-app https://github.com/rhdemo/2021-ai.git -l name=demo-2021-ai --name=demo-2021-ai
```

```
▶ oc expose svc/demo-2021-ai -l name=demo-2021-ai
route.route.openshift.io/demo-2021-ai exposed
```

```
▶ oc get routes
NAME     HOST/PORT                                                   PATH   SERVICES   PORT       TERMINATION   WILDCARD
demo-2021-ai   demo-2021-ai-test.apps.rhods-internal.openshiftapps.com          demo-2021-ai     8080-tcp                 None
```

```
▶ curl http://demo-2021-ai-test.apps.rhods-internal.ju9j.p1.openshiftapps.com/status
{"status":"ok"}
```

### Predict 
```
//1 - MISS
//2 - HIT
//-1 - unplayed
▶ curl -X POST -H "Content-Type: application/json" -d @data.json http://demo-2021-ai-test.apps.rhods-internal.ju9j.p1.openshiftapps.com/prediction
{"prob":[[8,11,12,11,8],[11,14,15,14,11],[12,15,16,15,12],[11,14,15,14,11],[8,11,12,11,8]],"x":2,"y":2}
```

### Update code 
```
▶ oc start-build demo-2021-ai
```

### Cleanup 
```
▶ oc delete all -l name=demo-2021-ai
```