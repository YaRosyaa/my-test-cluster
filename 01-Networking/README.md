**Установка компонентов, необходимых для внешнего доступа к кластеру**
# Этапы
## `01-cert-manager`
Установка и создание CA для сертификатов

### Подготовка
1. Для работы  с *GatewayAPI* нужно поставить его *CRD* **перед** установкой *cert-manager*
```bash
kubectl apply -f "https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.4.1/standard-install.yaml"
```

2. Установка *cert-manager* из *helm*-чарта
```bash
helm upgrade --install \
  cert-manager oci://quay.io/jetstack/charts/cert-manager \
  --version v1.19.2 \
  --namespace cert-manager \
  --create-namespace \
  --set crds.enabled=true \
  --set config.apiVersion="controller.config.cert-manager.io/v1alpha1" \
  --set config.kind="ControllerConfiguration" \
  --set config.enableGatewayAPI=true
```

### Создание CA
1. Определение `SelfSigned` `Issuer` для подписания сертификата CA
2. Определение сертификата CA
3. Определение CA с подписанным сертификатом
```bash
kubectl apply -f ./01-cert-manager
```

## `02-metallb`
Установка сервиса `Load Balancer` от *MetalLB* для облегчения доступа к Гейтвею:

1. Установка из helm-чарта
```bash
helm repo add metallb https://metallb.github.io/metallb
helm install metallb metallb/metallb
```

2. Определение пула внешних адресов и метода доступа к сервису
```bash
kubectl apply -f ./02-metallb
```

## `03-gateway`
Установка Traefik и определение Гейтвея

1. Установка Traefik из helm-чарта
```bash
helm repo add traefik https://traefik.github.io/charts
helm upgrade --install traefik traefik/traefik \ 
	-n traefik --create-namespace \
	-f /charts/traefik/my-values.yaml
```
> Файл `my-values.yaml`: настраивает логирование; включает работу с GatewayAPI и автоматическое создание GatewayClass; выключает создание IngressClass

2. Определение Гейтвея Traefik с автоматическим созданием сертификатов от cert-manager, подписанных созданным CA
```bash
kubectl apply -f ./03-gateway
```

## `04-routes`
Определение сервиса для веб-приложения и подключение к нему маршрута из Гейтвея
```bash
kubectl apply -f ./04-routes
```