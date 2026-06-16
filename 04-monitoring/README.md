# Мониторинг
Установка контура мониторинга.

Каждый компонент устанавливается, как ArgoCD Application. В манифестах определено **несколько источников** для удобной работы с values-файлами:
- *Helm*-чарты устанавливаются из официальных репозиториев;
- values-файл для каждого чарта берутся из этого репозитория по пути `04-monitoring/helm`.


## Компоненты
- `01-app-ksm` - *kube-state-metrics* - сбор метрик общего состояния Kubernetes кластера;
- `02-app-nodeexporter` - *Prometheus NodeExporter* - сбор метрик каждой ноды;
- `03-app-vm` - *Victoria Metrics Single* - в данном варианте, используется как легковесное хранилище метрик, а также, как эндпоинт для *remoteWrite* VMAgent'а и источника данных для Grafana;
- `04-app-vmagent` - *Victoria Metrics Agent* - *DaemonSet* для сбора метрик со всех подов на ноде и пуша в БД;
- `05-app-grafana` - *Grafana* - визуализация метрик. Внешний доступ к дашбордам происходит через Gateway.
> Дашборды для Графаны автоматически подгружаются из ConfigMap с лейблом `grafana_dashboard`

---
## Скейлинг приложения по количеству запросов
`06-app-prometheus-adapter` - *Prometheus Adapter* - Делает метрики доступными через Metrics API. Полученные метрики можно использовать в HPA для скейлинга деплоя по ним.
> В данном случае используется метрика `flask_http_requests_total` (counter) из *flask exporter*. В правиле *Prometheus Adapter* метрики агрегируются внутри пода и суммируются.

Новую метрику нужно применить в HPA, написанный helm-чарт позволяет сделать это коротким изменением values через Application ArgoCD
```bash
kubectl apply -f 07-app-new-static-app.yaml
```