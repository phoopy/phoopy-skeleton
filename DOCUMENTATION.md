# DOCUMENTATION

## Usage


### parameters.yml

It is where you can place all the env vars, and application config vars in order to do not hard code in the codebase.

It is yaml coded

You can also import a resource file like:

```yaml
imports:
    - { resource: parameters_puppet.yml }
```

### config.yml (config_dev.yml, config_prod.yml, config_test.yml)

Config is based in enviroments, that you can create your own or use the default ones that is (dev, prod, test), you can place there all the difference variables between envs.

And by running `bin/console` with `--env={ENV}` flag you can choose the one you want, by default the env is 'dev'

### services.yml

In services you can describe by yaml syntax like bellow all the top services of your application and its own dependencies:

```yaml
services:
    logger:
        class: logging.getLogger
        args:
            - app
        calls:
            - ['setLevel', {args: ['<const:logging.DEBUG>']}]
            - ['addHandler', {args:['@logger_handler']}]
```

In the services tag you have some modifiers you can use to grab other services, python constants, and kernel variables.

### Services modifiers

You have 3 kind of services modifiers:

- Variables that are surrounded by % like `%kernel.root_path%`
- Code constants/attributes/functions that you can access by using: `<const:sys.version>`
- Services that you can access by using: `@service_name`

### Kernel variables available in the services

- '%kernel.root_path%'
- '%kernel.app_path%'
- '%kernel.var_path%'

### Registering a service

In your bundle `services.yml` you can register a service like bellow:

```yaml
services:
    google_cloud_storage_client:
        class: google.cloud.storage.client.Client
        factory_method: from_service_account_json
        args:
            - '%kernel.root_path%/resources/%google_cloud.credentials_path%'

    storage_google_provider:
        class: src.app_bundle.source.provider.StorageGoogleProvider
        kwargs:
            client: '@google_cloud_storage_client'

    run_video_converter_command:
        class: src.app_bundle.source.command.RunVideoConverterCommand
        args:
            - '@logger'
        kwargs:
            mailer_provider: '@mailer_provider'
            app_url: '%app_url%'
        calls:
            - ['set_google_provider', {args: ['@storage_google_provider']}]
        tag:
            - command
```

### services::factory_method

With `factory_method` we are assuming that in the `class` x we have a static `factory_method` that will return us a instance to use, we also can use `args` and `kwargs` to send to this static method.
```yaml
services:
    google_cloud_storage_client:
        class: google.cloud.storage.client.Client
        factory_method: from_service_account_json
        args:
            - '%kernel.root_path%/resources/%google_cloud.credentials_path%'
```

### services::calls

With `calls` we can make sure that after the instantiation the Phoopy::kernel will make these calls before return us the service.

```yaml
services:
    clickbait_controller:
        class: src.app_bundle.source.controller.ClickbaitController
        kwargs:
            kernel: '@kernel'
            clickbait_service: '@clickbait_service'
        calls:
            - ['add_input_handler_factory', {args: ['title', '@clickbait_handler_factory']}]
        tag:
            - controller
```

### services::tag

With `tag` we are grouping in a container bundle a group of something, it is really usefull when constructing a bundle that has some specific behavior with some kind of object (like controllers, commands), then we can grab this group by calling `container.get_tagged_entries('tag_name')`

```
services:
    clickbait_controller:
        class: src.app_bundle.source.controller.ClickbaitController
        tag:
            - controller
```

### Bundle

A bundle is a non dependent part of a system that is responsable for only one thing.
We can create a bundle by extending the `phoopy.kernel.Bundle`, its Bundle can have your own `services`. Check out the example bellow

```python
from phoopy.kernel import Bundle
from os import path


class AppBundle(Bundle):
    def service_path(self):
        return path.join(self.get_bundle_dir(), 'config', 'services.yml')  # defines the full path of your services.yml

    def boot():
        pass  # here you can boot your bundle if needed

```
