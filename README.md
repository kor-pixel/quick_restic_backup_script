A quick python script to build restic commands from supplied variables

Requirments:
- A recent version of restic
- A server with restic serve running via rclone


Set up:
- Create a file named config.json and supply it with the following variables

``` json
{
  "ssh_address": "username@serverlocation",
  "ssh_key": "~/.ssh/key_file"
}
```
