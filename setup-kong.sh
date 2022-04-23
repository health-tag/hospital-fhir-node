#!/bin/bash

echo -e "Creating service FHIR..."
curl --location -g -s -k --request POST 'http://localhost:8001/services' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "name": "fhir-api",
    "url": "http://hapi-fhir-jpaserver-start:8080/fhir"
  }'

echo -e "\nCreating FHIR API route..."
curl --location -g -s -k --request POST 'http://localhost:8001/routes' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "name": "fhir-api-route",
    "service": {
      "name": "fhir-api"
    },
    "paths": ["/fhir-api"]
  }'

echo -e "\nEnabling plugin basic auth plugin on FHIR API"
curl --location -g -s -k --request POST 'http://localhost:8001/services/fhir-api/plugins' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "name": "basic-auth",
    "protocols": ["http", "https"],
    "config": {
      "hide_credentials": true
    }
  }'

echo -e "\nEnabling plugin cors plugin on FHIR API"
curl --location -g -s -k --request POST 'http://localhost:8001/services/fhir-api/plugins' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "name": "cors",
    "config": {
      "origins": ["*"],
      "headers": ["*"],
      "exposed_headers": ["*"]
    }
  }'

echo -e "Creating service Admin..."
curl --location -g -s -k --request POST 'http://localhost:8001/services' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "name": "admin-api",
    "url": "http://kong:8001"
  }'

echo -e "\nCreating route..."
curl --location -g -s -k --request POST 'http://localhost:8001/routes' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "name": "admin-api-route",
    "service": {
      "name": "admin-api"
    },
    "paths": ["/admin-api"]
  }'

echo -e "\nEnabling plugin basic auth plugin"
curl --location -g -s -k --request POST 'http://localhost:8001/services/admin-api/plugins' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "name": "basic-auth",
    "protocols": ["http", "https"],
    "config": {
      "hide_credentials": true
    }
  }'

echo -e "\nEnabling plugin cors plugin"
curl --location -g -s -k --request POST 'http://localhost:8001/services/admin-api/plugins' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "name": "cors",
    "config": {
      "origins": ["*"],
      "headers": ["*"],
      "exposed_headers": ["*"]
    }
  }'

echo -e "Creating service FHIR..."
curl --location -g -s -k --request POST 'http://localhost:8001/services' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "name": "fhir-api-key-auth",
    "url": "http://hapi-fhir-jpaserver-start:8080/fhir"
  }'

echo -e "\nCreating FHIR API route..."
curl --location -g -s -k --request POST 'http://localhost:8001/routes' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "name": "fhir-api-key-auth-route",
    "service": {
      "name": "fhir-api-key-auth"
    },
    "paths": ["/fhir-api-key-auth"]
  }'

echo -e "\nEnabling plugin key auth plugin on FHIR API"
curl --location -g -s -k --request POST 'http://localhost:8001/services/fhir-api-key-auth/plugins' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "name": "key-auth",
    "protocols": ["http", "https"]
  }'
