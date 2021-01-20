# STREAM SELECTOR TUTORIAL

The stream selector is a python script that allows the user to select which streams to import,
and, if the users wants to, delete properties from those streams. 

This is the first version of the scirpt, which only allows to select the streams. Unselecting
isn't suppoted yet, nor is reinstating deleted properties. Selecting a new stream after the first
execution is possible (notice that if you re-run the script there should be less properties).

If deleted properties are to be restored, a discovery should be run reseting the catalog used.

```bash 
.virtualenvs/tap-zendesk/bin/tap-zendesk --config zendesk_config.json --discover >> file_name.json 
```

### Running the script

The script is runned from the terminal with the following commands:

``` bash
python stream_selector.py folder_path 
```

Multiple files can be treated within the same execution.