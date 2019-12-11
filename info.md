# Configuration options

| Key          | Type     | Required | Default              | Description                                                                                          |
| ------------ | -------- | -------- | -------------------- | ---------------------------------------------------------------------------------------------------- |
| `api_key`    | `string` | `True`   | None                 | Starling Bank API token (see insturctions below)                                                     |
| `name`       | `string` | False    | sensor.hasslingbank  | Custom name for the sensor                                                                           |

## Example default configuration.yaml

```yaml
hasslingbank:
  api_key: <api_key_here>
```

## Example: configuration.yaml with options

```yaml
hasslingbak:
  api_key: <api_key_here>
  name: "My Starling Account"
```

## Generate Starling Bank API key / Get budget ID

API:

1. Log on to the Starling Devleoper Website
2. Create a personal API token
3. Enter the token into the api_key field in your configuration.yaml file
