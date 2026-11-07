# SAS Customer Onboarding Automation



## Project Overview



This project automates customer onboarding using GitHub Actions, Python, Helm, and Kubernetes.



When a new customer is registered, the workflow accepts a customer ID, company name, and motto. A Python script validates the inputs and uses Helm to deploy a personalized NGINX welcome page into a customer-specific Kubernetes namespace.



## Architecture



GitHub Actions → Windows Self-Hosted Runner → Python → Helm → Kubernetes → NGINX Welcome Page



## Technologies Used



- GitHub Actions — CI/CD workflow automation

- Python — Customer validation and deployment orchestration

- Helm — Kubernetes application packaging and deployment

- Kubernetes — Container orchestration and customer isolation

- Docker Desktop — Local Kubernetes environment

- NGINX — Hosting the personalized customer welcome page

- PowerShell — Windows runner scripting



## Automated Onboarding Process



1. Start the GitHub Actions workflow manually.

2. Enter the customer ID, company name, and motto.

3. Generate a customer purchase JSON file.

4. Validate the customer information using Python.

5. Verify Helm and Kubernetes connectivity.

6. Deploy the customer website using Helm.

7. Create a dedicated Kubernetes namespace for the customer.

8. Run NGINX pods serving the personalized welcome page.



## Example Customer



Customer ID: `test-08`



Company Name: `SAS Automated Customer`



Motto: `Deployed through GitHub Actions`



Kubernetes namespace: `customer-test-08`



Helm release: `site-test-08`



## How to Run



### Prerequisites



- Python 3

- Helm 4

- kubectl

- Docker Desktop with Kubernetes enabled

- Windows self-hosted GitHub Actions runner



### Trigger the Workflow



1. Open the GitHub repository.

2. Navigate to Actions → SAS Customer Onboarding.

3. Select Run workflow.

4. Enter customer details.

5. Start the workflow and monitor the deployment.



### Verify Deployment



```powershell

kubectl get namespaces

kubectl get pods -n customer-test-08

kubectl get svc -n customer-test-08

helm list -n customer-test-08
```



### Access the Customer Website


```powershell

kubectl port-forward svc/site-test-08-nginx 8082:80 -n customer-test-08
```



Open `http://localhost:8082` in a browser.



Expected content:



**Welcome to SAS**



**SAS Automated Customer**



Deployed through GitHub Actions



## Customer Isolation



Each customer receives a dedicated Kubernetes namespace and Helm release.



For example:



- `customer-acme-01`

- `customer-globex-02`

- `customer-test-08`



## Current Limitations



- Deployments run on local Docker Desktop Kubernetes rather than a cloud cluster.

- The application is accessible through local port forwarding.

- Public DNS, HTTPS, and Ingress are not configured.

- The current deployment serves a static NGINX welcome page; a separate backend service is not yet implemented.

- Additional input sanitization, security hardening, and production monitoring are required.



## Future Improvements



- Deploy to a managed Kubernetes service.

- Configure Ingress, DNS, and TLS certificates.

- Implement a backend API.

- Add automated integration tests.

- Improve input sanitization and secrets management.

- Add production monitoring and alerting.

## End-to-End Pipeline Testing

The complete customer onboarding workflow was tested successfully
using GitHub Actions and a Windows self-hosted runner.

### Test Customer

- Customer ID: `demo-04`
- Company Name: `SAS DevOps Solutions`
- Motto: `Automate, Deploy, Scale`
- Kubernetes Namespace: `customer-demo-04`
- Helm Release: `site-demo-04`

### Test Results

1. Triggered the GitHub Actions workflow manually.
2. The workflow completed successfully with a green status.
3. Python validated the customer information.
4. Helm deployed the customer-specific Kubernetes resources.
5. Two NGINX pods reached `1/1 Running` with zero restarts.
6. Verified the personalized customer website in a browser.

### Verification Commands

```powershell

kubectl get pods -n customer-demo-04
kubectl get svc -n customer-demo-04
helm list -n customer-demo-04
```

### Website Access

```powershell

kubectl port-forward svc/site-demo-04-nginx 8086:80 -n customer-demo-04
```

Open `http://localhost:8086` in a browser.


## Summary



This project demonstrates an automated, repeatable customer onboarding workflow with GitHub Actions, Python, Helm, and Kubernetes. It provisions customer-specific application resources and deploys personalized welcome pages with minimal manual intervention.

## Selected SAS Challenge Objectives

This solution focuses on three objectives from the SAS Interview Challenge.

### Objective 2 - Data Deployment to Web Servers

Customer-specific information is deployed to Kubernetes using Helm and ConfigMaps.

Each customer receives a dedicated namespace, NGINX Deployment, and Kubernetes Service. The ConfigMap provides a personalized HTML welcome page containing the company name, company motto, and "Welcome to SAS" message.

Two NGINX replicas provide basic availability.

### Objective 5 - Pipeline Orchestration

GitHub Actions coordinates the customer onboarding process using a Windows self-hosted runner.

The workflow accepts customer details, generates a JSON payload, validates the information using Python, verifies Kubernetes connectivity, and deploys the application through Helm.

The current demonstration uses manual workflow dispatch. In a production environment, a purchase system could trigger onboarding automatically through a webhook or event queue.

### Objective 8 - Configuration Management

Helm templates provide a reusable approach to customer-specific Kubernetes configurations.

Customer details are passed into Helm and used to generate the ConfigMap, Deployment, and Service. Each customer has an independent Helm release, allowing deployments to be managed separately.

## Scalability Considerations

The solution is designed to support multiple customers through dedicated Kubernetes namespaces and Helm releases.

To scale toward 10-100 customers, production improvements would include resource quotas, automated capacity management, ingress-based routing, and monitoring.

The current implementation has not been load-tested for 100 customers.

## Safe Customer Configuration Handling

The Python onboarding script validates customer details before deployment.

Customer-specific configuration is written to a temporary JSON values file
and passed to Helm using the `--values` option.

This avoids parsing issues with special characters such as commas,
equals signs, and ampersands in customer names and mottos.

The temporary configuration file is deleted using a Python
`try/finally` block, even if the Helm deployment fails.

The implementation was tested using:

- Customer ID: `demo-03`
- Company Name: `Cloud & Data`
- Motto: `Innovate, Build, Grow`

The Helm deployment completed successfully, and both NGINX replicas
reached the Running state.

Customer-provided HTML content is also escaped in the Helm ConfigMap
template to prevent it from being interpreted as HTML markup.


## Configuration Updates and Rolling Deployments

Customer website content is managed through a Kubernetes ConfigMap.

The Helm Deployment template includes a checksum annotation
(`checksum/web-content`) calculated from the ConfigMap template.

When customer details change, Helm updates the ConfigMap and
the checksum annotation changes. Kubernetes then performs a
rolling update of the NGINX pods.

This behavior was verified using customer `demo-03`:

- Initial deployment: Helm revision 1
- Updated customer motto: `Innovate, Build, Grow - Version 2`
- Helm upgrade: revision 2
- Kubernetes replaced the existing NGINX pods with new pods.
- Both new replicas reached `1/1 Running` with zero restarts.
- The updated welcome page was verified in the browser.

This ensures that customer content updates are reflected in
the running application without requiring manual pod deletion.


## Error Handling and Recovery

Python validates customer input before deployment.

Helm waits for Kubernetes resources to become ready and uses rollback-on-failure to recover from unsuccessful upgrades.

For production use, additional improvements would include retry policies, structured logging, alerting, and automated recovery procedures.

## Security Considerations

Customer namespaces provide a logical separation of Kubernetes resources but are not a complete security boundary.

A production implementation should include Kubernetes RBAC, network policies, input sanitization, TLS, and secure secrets management.

The self-hosted GitHub Actions runner should be restricted to trusted workflows and repositories.

## Production Architecture - Future Enhancement

Purchase Completed -> Purchase Webhook -> Event Queue -> Onboarding Pipeline -> Python Validation -> Helm Deployment -> Kubernetes -> Customer Website

This is a proposed production architecture, not functionality currently implemented in the demonstration.
