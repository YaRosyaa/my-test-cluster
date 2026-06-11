**Развёртывание деплоя приложения и настройка автоскейлинга через *HPA***

1. Для работы эндпоинта `metrics.k8s.io`, который *HPA* использует для скалирования по простым метрикам, нужно установить *metric-server*:
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.8.1/components.yaml
```

2. Определение *HPA* для автоскейлинга по проценту от реквестов по CPU
```bash
kubectl apply -f ./00-HPA.yaml
```

3. Определение деплоя веб-приложения с настройкой `podAntiAffinity` для распределения  по нодам
```bash
kubectl apply -f ./01-Deploy.yaml
```
> Данные для работы с базой данных прокидываются в контейнер из секрета `db-credentials` через переменные среды. Пример такого секрета можно посмотреть в файле `99-sampleSecret.yaml`