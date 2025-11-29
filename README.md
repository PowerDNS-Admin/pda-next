# PDA-Next

A PowerDNS web interface with advanced features.

***WARNING: This project is a work in progress and is NOT ready for production use!***

If you're excited to follow the development progress of the next-generation PDA application, then please wait for
an official release announcement before using this project.

| Branch  | CodeQL                                                                                                                                                                                                         | MegaLinter                                                                                                                                                                                                 | Python Build                                                                                                                                                                                                   | Image Build                                                                                                                                                                                                 |
|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dev`   | [![CodeQL](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/codeql-analysis.yml/badge.svg?branch=dev)](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/codeql-analysis.yml)           | [![MegaLinter](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/mega-linter.yml/badge.svg?branch=dev)](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/mega-linter.yml)           | [![Python Build](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/python-build.yml/badge.svg?branch=dev)](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/python-build.yml)           | [![Image Build](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/image-build.yml/badge.svg?branch=dev)](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/image-build.yml)           |
| `0.1.0` | [![CodeQL](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/codeql-analysis.yml/badge.svg?branch=release/0.1.0)](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/codeql-analysis.yml) | [![MegaLinter](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/mega-linter.yml/badge.svg?branch=release/0.1.0)](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/mega-linter.yml) | [![Python Build](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/python-build.yml/badge.svg?branch=release/0.1.0)](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/python-build.yml) | [![Image Build](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/image-build.yml/badge.svg?branch=release/0.1.0)](https://github.com/PowerDNS-Admin/pda-next/actions/workflows/image-build.yml) |

## Features

- Provides forward and reverse zone management
- Provides zone templating features
- Provides user management with role based access control
- Provides zone specific access control
- Provides activity logging
- Authentication:
    - Local User Support
    - SAML Support
    - LDAP Support: OpenLDAP / Active Directory
    - OAuth Support: Google / GitHub / Azure / OpenID
- Two-factor authentication support (TOTP)
- PowerDNS server configuration & statistics monitoring
- DynDNS2 protocol support
- Easy IPv6 PTR record editing
- Provides an API for zone and record management among other features
- Provides full IDN/Punycode support

For additional information on features, please see the
[Project Features](https://github.com/PowerDNS-Admin/pda-next/blob/main/docs/wiki/project/features.md) document.

## TL;DR

To get started quickly with a simple deployment, execute the following commands on a *nix based system
with `bash` and `git` installed:

```
git clone https://github.com/PowerDNS-Admin/pda-next.git
cd pda-next
deployment/setup.sh
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

This project is released under the Attribution-NonCommercial 4.0 International license. For additional
information, [see the full license](https://github.com/PowerDNS-Admin/pda-next/blob/main/LICENSE).

## Donate

Like my work?

<a href="https://www.buymeacoffee.com/AzorianMatt" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

**Want to sponsor me?** Please visit my organization's [sponsorship page](https://github.com/sponsors/AzorianSolutions).
