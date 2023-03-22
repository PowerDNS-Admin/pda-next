# PDA Next

## Configuration Guide

### Getting Started

The application provides a lot of fluidity in how it can be configured. This remains true for both environment
and runtime configuration. The application is designed to be flexible and allow for a wide variety of
deployment scenarios which include bare metal, virtual machines, containers, and cloud environments.

There is a plethora of environment configuration settings that can be used to bootstrap the application for
varying environments. All of these settings can be set using environment variables or by creating a
`.env` file in the root directory of the application that contains one or more environment variables to be
loaded at application startup. For more information on these settings, see the
[Environment Configuration Guide](https://github.com/PowerDNS-Admin/pda-next/blob/main/docs/wiki/configuration/settings/environment-settings.md)
section.

If you want to change the default path of the `.env` file, you can set the `PDA_ENV_FILE` environment variable
to the path of the file you want to use. If a relative path is provided, it will be relative to the
root directory of the application. Furthermore, if you want to use a different file encoding other than `UTF-8`,
you may do so by setting the `PDA_ENV_FILE_ENCODING` environment variable to the encoding you want to use.

#### Secrets Support

Additionally, there is support for secure settings to be kept in a filesystem location using a convention
similar to Docker-style secrets. To use this feature, you simply create a file with the same name as the
application setting you want to set and store it in the directory specified by the `env_secrets_dir` setting
or the `PDA_ENV_SECRETS_DIR` environment variable.

So for example, say you want to set the value of an application setting named `example_option`.
Assuming that `env_secrets_dir` or `PDA_ENV_SECRETS_DIR` is set to `/var/run/secrets`, one would create a file
named `example_option` and store it in the `/run/secrets` directory. The contents of the file would be
the value of the `example_option` setting. The application will automatically detect the file and use its
contents as the value of the setting.

### [Application Settings](https://github.com/PowerDNS-Admin/pda-next/blob/main/docs/wiki/configuration/settings/README.md)

To get an in-depth understanding of the many application settings available, see the
[Application Settings Guide](https://github.com/PowerDNS-Admin/pda-next/blob/main/docs/wiki/configuration/settings/README.md).

#### [Environment Configuration](https://github.com/PowerDNS-Admin/pda-next/blob/main/docs/wiki/configuration/settings/environment-settings.md)

To view the alphabetical list of environment configuration settings, see the
[Environment Configuration Guide](https://github.com/PowerDNS-Admin/pda-next/blob/main/docs/wiki/configuration/settings/environment-settings.md).

#### [Runtime Configuration](https://github.com/PowerDNS-Admin/pda-next/blob/main/docs/wiki/configuration/settings/runtime-settings.md)

To view the alphabetical list of environment configuration settings, see the
[Runtime Configuration Guide](https://github.com/PowerDNS-Admin/pda-next/blob/main/docs/wiki/configuration/settings/runtime-settings.md).
