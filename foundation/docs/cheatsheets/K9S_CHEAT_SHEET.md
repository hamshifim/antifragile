# K9s Cheat Sheet

Kubernetes cluster control without leaving the keyboard.

Use this when you need to look, understand, and act quickly.


## Launch

```bash
k9s
k9s -n model-binding
k9s --context dev--aws_model_binding--gid--default_conf--0
k9s --readonly
k9s -c pod
```

| Need | Command |
| --- | --- |
| Start normally | `k9s` |
| Open a namespace | `k9s -n <namespace>` |
| Open a context | `k9s --context <context>` |
| Read-only mode | `k9s --readonly` |
| Start on a resource view | `k9s -c pod` |
| Find config paths | `k9s info` |


## The Whole Game

| Key | Move |
| --- | --- |
| `?` | Show live help and active bindings |
| `:` | Jump to a resource view |
| `/` | Filter the current view |
| `Esc` | Back out, clear filter, close prompt |
| `Ctrl-a` | Show resource aliases |
| `:q` or `Ctrl-c` | Quit |

K9s is modal. If it feels stuck, press `Esc`, then `?`.


## Jump Views

Type `:` then one of these.

| View | Aliases |
| --- | --- |
| Pods | `:pod`, `:po`, `:pods` |
| Deployments | `:deploy`, `:deployment`, `:dp` |
| StatefulSets | `:sts`, `:statefulset` |
| Services | `:svc`, `:service` |
| Ingresses | `:ing`, `:ingress` |
| Namespaces | `:ns`, `:namespace` |
| Nodes | `:no`, `:node` |
| Events | `:ev`, `:event` |
| Secrets | `:secret` |
| ConfigMaps | `:cm`, `:configmap` |
| Contexts | `:ctx` |
| Pulses | `:pulses`, `:pu` |


## Filters

| Pattern | Meaning |
| --- | --- |
| `/workspace` | Names matching `workspace` |
| `/err|fail|crash` | Regex filter |
| `/!completed` | Inverse filter |
| `/-l app=workflow-wielder` | Label selector |
| `/-f wield` | Fuzzy filter |

You can also jump straight in:

```text
:pod model-binding
:pod /workspace
:pod app=workflow-wielder
:pod @my-context
```


## Pod Triage Loop

1. `:po`
2. `/app-or-pod-fragment`
3. `Enter` to drill in
4. `l` for logs
5. `d` to describe
6. `Esc` back up
7. `:ev` if the reason is not obvious

Read symptoms in this order:

```text
STATUS -> READY -> RESTARTS -> AGE -> EVENTS -> LOGS
```


## Logs

| Key | Use |
| --- | --- |
| `l` | Open logs for selected pod |
| `0` | Show all log lines |
| `1` | Tail recent log lines |
| `f` | Toggle follow |
| `/` | Filter inside logs |
| `Esc` | Back to the pod |


## Common Actions

| Key | Action |
| --- | --- |
| `d` | Describe selected resource |
| `v` | View YAML |
| `e` | Edit resource |
| `l` | Logs |
| `s` | Shell into container |
| `y` | Copy YAML |
| `Ctrl-d` | Delete with confirmation |
| `Ctrl-k` | Kill/delete now |

Treat `e`, `Ctrl-d`, and `Ctrl-k` as production tools.


## Service To Pod Trace

```text
:ing       find host/path
Enter      inspect ingress
:svc       find backend service
Enter      inspect selectors
:po        filter by selector labels
l          read logs
d          read events and probes
```


## Deployment Rollout Check

```text
:deploy
/name
Enter
d
:rs
/name
:po
/name
```

Look for desired/current/ready mismatch, new ReplicaSets with zero ready pods,
and pods stuck in image pull, scheduling, or probe failure.


## Node Pressure Check

```text
:no
Enter
d
:po
/-l <workload-label>
```

Look for:

```text
DiskPressure
MemoryPressure
PIDPressure
NetworkUnavailable
Taints
Unschedulable
```


## Workspace Bootstrap Path

For the AWS bootstrap POC:

```text
:ctx      dev--aws_model_binding--gid--default_conf--0
:ns       model-binding
:po       /workflow-wielder
:svc      /workflow-wielder
:ing      /workflow-wielder
:ev       /workflow-wielder|alb|ingress
```

Expected first win:

```text
pod Running
service has endpoints
ingress gets an ALB hostname
logs show the tiny HTTP server alive
```


## When In Doubt

Use read-only first:

```bash
k9s --readonly --context <context>
```

Then:

```text
?      learn current keys
:ev    read cluster truth
d      inspect selected thing
l      read workload truth
Esc    breathe
```


## References

- K9s commands: https://k9scli.io/topics/commands/
- K9s hotkeys: https://k9scli.io/topics/hotkeys/
