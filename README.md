# Features

- Gathers account balance from the Starling Bank API

------------
##  Installation
### Manual
1. Open the directory for your HA configuration (where configuration.yaml is located)
2. Open or create a custom_components directory
3. Download all the files from the custom_components/hasslingbank/ directory (folder) in this repository.
4. Place the files you downloaded into the custom_components directory
5. Add "hasslingbank:" to your HA configuration (see examples below)
6. Restart Home Assistant 

## Configuration options
| Key | Type | Required | Default | Description |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| api_key | string | yes | None | Your Starling Bank API token |
| name | string | no | sensor.starling | An optional custom name for the sensor |

## Example configuration.yaml

```yaml
hasslingbank:
  api_key: <api_key>
```


### Generate a Starling Bank Personal Access Token
Creating a Personal Access Token requires a Starling Bank Developer account. These are free and easy to setup.

1. Log in to the Starling Developer website
2. Open https://developer.starlingbank.com/personal/list
3. Create a new token with the permissions: 
	- account:read
	- balance:read
4. Enter your password and click Generate
5. Copy the token and paste it into the api_key entry in your configuration.yaml file


