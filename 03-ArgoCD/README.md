# ArgoCD

ArgoCD для GitOps контроля за конфигурацией устанавливаемых компонентов кластера.

Внешний доступ к UI происходит через Gateway, указанный в `argocd-values.yaml`.

```bash
helm install argocd https://argoproj.github.io/argo-helm/argo-cd -f argocd-values.yaml -n argocd --create-namespace
```

## Установка приложения из helm-чарта
Теперь приложение удобнее контролировать не через отдельные манифеста, а через Application ArgoCD.
Для этого приложение обёрнуто в helm-чарт - `/charts/my-static-app`, в values-файле по-умолчанию уже записаны предпочтительные значения, для удобства.
```bash
kubectl apply -f static-app-app.yaml
```
- *HPA* назначен для автоскейлинга по проценту от реквестов по CPU
- Деплой веб-приложения настройкен с `podAntiAffinity` для распределения по нодам