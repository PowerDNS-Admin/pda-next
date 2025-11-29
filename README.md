# PDA-Next

An advanced management and monitoring tool for the PowerDNS software suite.

***WARNING: This project is a work in progress and is NOT ready for production use!***

If you're excited to follow the development progress of the next-generation PDA application, then please wait for
an official release announcement before using this project.

| Branch  | CodeQL                                                                                                                                                                                                         | MegaLinter                                                                                                                                                                                                 | Python Build                                                                                                                                                                                                   | Image Build                                                                                                                                                                                                 |
|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dev`   | [![CodeQL](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/codeql-analysis.yml/badge.svg?branch=dev)](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/codeql-analysis.yml)           | [![MegaLinter](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/mega-linter.yml/badge.svg?branch=dev)](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/mega-linter.yml)           | [![Python Build](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/python-build.yml/badge.svg?branch=dev)](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/python-build.yml)           | [![Image Build](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/image-build.yml/badge.svg?branch=dev)](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/image-build.yml)           |
| `0.1.0` | [![CodeQL](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/codeql-analysis.yml/badge.svg?branch=release/0.1.0)](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/codeql-analysis.yml) | [![MegaLinter](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/mega-linter.yml/badge.svg?branch=release/0.1.0)](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/mega-linter.yml) | [![Python Build](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/python-build.yml/badge.svg?branch=release/0.1.0)](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/python-build.yml) | [![Image Build](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/image-build.yml/badge.svg?branch=release/0.1.0)](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/image-build.yml) |

## Features

- Full Featured API
  - Provides a full API that drives browser-based client application.
  - All functionality provided directly through API allowing service providers to build their own client applications.
  - OpenAPI / Swagger UI support baked in for all API endpoints.
  - Python SDK in the works to ease automation and integration with the API.
- Multi-Tenancy
  - Allows service providers to provide shared access to PowerDNS server instances.
  - Allows service providers to provide shared access of DNS zones to allow for offerings such as dynamic DNS.
  - Allows tenants to bring their own DNS servers and external OAuth authentication services.
  - Allows tenants to use configure stopgap and custom domains for API and browser client application white labeling.
- Multi-Server Management
  - Provides the ability to manage multiple PowerDNS authoritative servers in all modes.
  - Provides the ability to manage multiple PowerDNS recursive servers.
  - Planned support for managing the PowerDNS dnsdist proxy server.
- Zone Management
  - Supports forward and reverse zone management.
  - Supports catalog zone management.
  - Supports management of experimental zone views feature.
  - Supports zone templating for easy zone set up.
  - Supports assigning zones to specific servers.
  - DynDNS2 protocol support
- Advanced Authentication & Permissions System
  - API supports authentication by OAuth clients and traditional user sessions.
  - Supports OAuth client registrations at system, tenant, and user levels.
  - Supports both role-based permissions assignment as well as granular resource based permission assignment.
  - Planned support for authenticating users via third-party OAuth services.
- User / API Security
  - Supports all standard multifactor authentication (MFA) mechanisms including WebAuthn (hardware keys),
  TOTP (software authenticators), and OTP (SMS / Email).
  - Supports locking API sessions to originating IP addresses to mitigate session / OAuth token hijacking.
- Auditing
  - Detailed auditing baked in to every action taken.
- Monitoring
  - Supports extraction and monitoring of server configuration, statistics, and cache metrics.
  - Provides Prometheus-style metrics via the API including direct relay of DNS server metrics.
  - Provides Zabbix Sender reporting capabilities for task execution monitoring.
- Easy IPv6 PTR record editing
- Provides IDN/Punycode support

For additional information on features, please see the
[Project Features](https://github.com/PowerDNS-Admin/pda-next/blob/main/docs/wiki/project/features.md) document.

## TL;DR

To get started quickly with a simple local development deployment, execute the following commands on a *nix based
system with `bash` and `git` installed:

```
git clone https://github.com/PowerDNS-Admin/pda-next.git
cd pda-next
deploy/start.sh
```

## Project Documentation

### Project Information

For information about the project such as feature planning, the roadmap, and milestones, then please see the
[Project Information](https://github.com/PowerDNS-Admin/pda-next/blob/main/docs/wiki/project/README.md) section of the
wiki.

### Contributing

If you're interested in participating in the project design discussions, or you want to actively submit work to the
project then you should check out the
[Contribution Guide](https://github.com/PowerDNS-Admin/pda-next/blob/main/docs/wiki/contributing/README.md)!

### Application Configuration

For information about all the ways this application can be configured and what each setting does, please visit the
[Configuration Guide](https://github.com/PowerDNS-Admin/pda-next/blob/main/docs/wiki/configuration/README.md) section of
the wiki.

### Application Deployment

For information about how to deploy the application in various environments, please visit the
[Deployment Guides](https://github.com/PowerDNS-Admin/pda-next/blob/main/docs/wiki/deployment/README.md) section of the
wiki.

### Application Testing

For information on how to create and execute automated application tests, please visit the
[Testing Guide](https://github.com/PowerDNS-Admin/pda-next/blob/main/docs/wiki/testing/README.md) section of the wiki.

## Security Policy

Please see our
[Security Policy](https://github.com/PowerDNS-Admin/pda-next/blob/main/.github/SECURITY.md).

## Support Policy

Please see our
[Support Policy](https://github.com/PowerDNS-Admin/pda-next/blob/main/docs/wiki/support/README.md).

Looking to chat with someone? Join our [Discord Server](https://discord.powerdnsadmin.org).

## Code of Conduct

Please see our
[Code of Conduct](https://github.com/PowerDNS-Admin/pda-next/blob/main/.github/CODE_OF_CONDUCT.md).

## License

This project is released under the Attribution-NonCommercial 4.0 International license. Don't worry though, we're working on provisions for both free and paid
commercial licensing as well!

For additional
information, [see the full license](https://github.com/PowerDNS-Admin/pda-next/blob/main/LICENSE).

## Donate

Like my work?

<a href="https://www.buymeacoffee.com/AzorianMatt" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

**Want to sponsor me?** Please visit my organization's [sponsorship page](https://github.com/sponsors/AzorianSolutions).
