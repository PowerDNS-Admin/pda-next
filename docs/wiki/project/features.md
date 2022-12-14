# PDA Next

## Project Features

The purpose of this document is to provide some explanation about key platform features that really drive the value of
the product.

### Table of Contents

- [Microservice Architecture](#microservice-architecture)
  - [API Server](#api-server)
  - [CLI Application](#cli-application)
  - [Web Application](#web-application)
- [Authentication](#authentication)
- [Role Based Access Control (RBAC)](#role-based-access-control--rbac-)
  - [Examples](#examples)

### Microservice Architecture

The next-gen PDA application makes use of microservice architecture by splitting the project into multiple components
that can be individually deployed as desired. Currently, there are three components, the API server, the CLI
application, and the web application. In the following sections, you will find a brief description of what each of
these components contribute to the solution.

#### API Server

The API server is the core of the platform. It provides a common interface for consuming platform features through the
use of HTTP APIs based on the OpenAPI (formerly Swagger) specification. This is the only component required to use the
platform. All other components are tools to consume resources from the API server.

#### CLI Application

The CLI application is designed to provide basic deployment and administration capabilities. The deployment features
are meant to aid in the environment setup for deploying the application. This would include common tasks such as system
reconfiguration, package installation and validation, and application configuration.

The administration features are meant to provide an easy way to get started with the API server. These features will
provide basic facilities for managing the system level administrator accounts in the application database.

#### Web Application

The web application is designed to provide a modern, standards compliant web browser based administration tool for the
API server. By design, this application is a client-side application that will communicate with the back-end purely
through the API service. For this reason, this component is nothing more than a static JavaScript / HTML
application that can be served up by any choice of web server solution.

### Authentication

Coming soon!

### Role Based Access Control (RBAC)

This is where this next-gen solution really shines. Taking inspiration from the Amazon Web Service (AWS)
[Amazon Resource Name (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) strategy, a
very granular access control system will be achieved.

The idea starts with the concept of giving all application entities a unique but uniform reference format similar to
AWS ARN except known as "PDARN". Here is how that reference is structured:

> pdarn:tenant-id:app-id:resource-type:resource-id:permission-flags

The idea is to provide a reference structure that can target any unique, mutable data point of the application. By
doing this, an administrator can create access control policies that can target just about any user manageable
reference in the application, thus achieving extreme granularity on the RBAC system. This is further complimented by
the fact that this approach should be somewhat friendly to third-party authentication integrations such as LDAP and
OAUTH as examples.

The various app components within the API server application will use a structured definition system that allows for
each app to provide references to PDARN patterns provided by that app as well as what permissions are available for
each PDARN pattern. This essentially makes the RBAC pluggable for new developments as defining new capabilities in app
components becomes very easy and fast. This approach also makes supporting completely fluid permissions structures
possible.

#### Examples

In practice, here is what some PDARNs would look like:

**Tenant Level Reference**

This reference targets the tenant account with an ID of "4321" and references the creation, read, update, and delete
permissions for this entity.

> pdarn:4321:c,r,u,d

**Tenant Settings Reference**

This reference targets the tenant account settings app for tenant "4321" and references all available permissions for
this entity.

> pdarn:4321:settings

**More Specific Tenant Settings Reference**

This reference targets the "auth" area of the settings app for tenant "4321" and references the read permission for the
entity.

> pdarn:4321:settings/sync:r

**Specific Setting Reference**

This reference targets the "ui/web" area of the settings app for tenant "4321" and references the update permission for
the entity.

> pdarn:4321:settings/ui/web:site-title:u

**Specific Zone Record Reference**

This reference targets a specific record set record with the ID "123" for the TXT record set of "example.com" within the
tenant "4321" and references the dynamic DNS update permission for the entity.

> pdarn:4321:zones/example.com/txt/@:123:ddu

**Specific Zone Record Set Reference**

This reference targets the A record set for "stage.example.com" within the tenant "4321" and references the read
permission for the entity.

> pdarn:4321:zones/example.com/a:stage:r
