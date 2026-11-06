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



## Summary



This project demonstrates an automated, repeatable customer onboarding workflow with GitHub Actions, Python, Helm, and Kubernetes. It provisions customer-specific application resources and deploys personalized welcome pages with minimal manual intervention.

