# 2021-ai

## Edit in CodeReady Workspaces

If you are running on a cluster with [CodeReadyWorkspaces](https://developers.redhat.com/products/codeready-workspaces/overview) like [Developer Sandbox](https://developers.redhat.com/developer-sandbox), you can start editing it directly from there.

Run it with [Eclipse Che Factories](https://developers.redhat.com/che/creating-factories):

NOTE: Change the address of Factory with your CRW URL

[![Contribute](https://raw.githubusercontent.com/blues-man/nodejs-mongodb-sample/master/factory-contribute.svg)](https://codeready-openshift-workspaces.apps.cluster-b237.b237.sandbox1343.opentlc.com/factory?url=https://github.com/blues-man/2021-ai.git)

## Create model Image  
```
make build
make push
```

## Deployment  
```
oc create -f https://raw.githubusercontent.com/rhdemo/2021-ai/master/install/deployment.yml
oc new-app --template=demo-2021-ai
```

## cleanup
```
oc delete template demo-2021-ai
oc delete all -l app=demo-2021-ai
oc delete route demo-2021-ai
```


--



## Deploy 
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

## Predict 
```
//1 - MISS
//2 - HIT
//-1 - unplayed
▶ curl -X POST -H "Content-Type: application/json" -d @data.json http://demo-2021-ai-test.apps.rhods-internal.ju9j.p1.openshiftapps.com/prediction
{"prob":[[8,11,12,11,8],[11,14,15,14,11],[12,15,16,15,12],[11,14,15,14,11],[8,11,12,11,8]],"x":2,"y":2}
```

## Update code 
```
▶ oc start-build demo-2021-ai
```

## Cleanup 
```
▶ oc delete all -l name=demo-2021-ai
```