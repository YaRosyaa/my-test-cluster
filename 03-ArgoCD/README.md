# ArgoCD

ArgoCD для GitOps контроля за конфигурацией устанавливаемых компонентов кластера.

Внешний доступ к UI происходит через Gateway, указанный в `argocd-values.yaml`.

```bash
helm install argocd https://argoproj.github.io/argo-helm/argo-cd -f argocd-values.yaml -n argocd --create-namespace
```