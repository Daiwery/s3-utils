# s3-utils
It is a set of tools for interaction with Yandex Object Storage implemented using boto3 library. 

- For installing run setup.sh.
```bash
bash setup.sh
```

- After installing it is possible to use s3-utils as CLI.
```bash
download profile command args
```
For more info see 'help'.

- Authentication in all commands is performed using profiles contained in the .aws/credentials file.
```
# .aws/credentials
[default]
  aws_access_key_id = 
  aws_secret_access_key = 
```
