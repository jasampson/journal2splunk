 # :warning: You should really not use this for anything.  Splunk finally added Universal Forwarder support for journald in 8.1.0.  [Please see the release notes for details](https://docs.splunk.com/Documentation/Splunk/8.1.0/ReleaseNotes/MeetSplunk#What.27s_New_in_8.1).

# journal2splunk
This project exists because the Splunk Universal Forwarder does not support log ingestion from Linux journald without first writing logs out to disk.

# Setup
You will need to do several things to get things working.

In Splunk do the following:
1. Log in to the Splunk web interface as a user with admin rights.
2. Go to `Settings -> Data Inputs` in the top menu.
3. Under `Local Inputs` on the `UDP` row, click the `+ Add new` button.
4. Choose a port for the UDP listener to listen on and enter it here and click `Next >` at the top.  We're using 5516 in our example.
5. Click on `Select Source Type` and choose `_json`.  Under Index settings, choose or create a new index.  In our case I've created a new index called `linux_journald`.  Click `Review >` at the top.
6. After reviewing this page, click `Submit >` at the top.
7. You must now edit `props.conf` to pick up timestamps from our logs.  If you don't do this, you won't see any data at all in the index.  In Linux this file lives at `/opt/splunk/etc/system/local/props.conf`.  Add the following lines to it:
```
[linux-journald]
TIME_PREFIX=^{"TIMESTAMP":
TIME_FORMAT=%d-%b-%Y,%H:%M:%S
```

On your Linux servers do the following:
1. Log in as root.
2. Clone this git repository and cd into the directory.
3. Set your splunk server and udp port in `journal2splunk.conf`
4. Run `./setup.py` to install the service.

Now go back to Splunk and do the following:
1. Force Splunk to reread your `props.conf` changes and verify that you have events appearing in your index in the Search & Reporting app: `index="linux_journald" | extract reload=T`
2. Set up automatic field extraction by going to `Settings -> Fields`.
3. Click on `+ Add new` on the `Field extractions` row.
4. For `Name`, enter something like `ColonCommaKVPs`.
5. For `Apply to` leave `sourcetype` selected and in `named` type in `_json`.
6. In the `Extraction/Transform` box paste in this regex `"(?<_KEY_1>[^"]*)": "(?<_VAL_1>[^"]*)"`
7. Click `Save` and return to the Search & Reporting app.  Verify that you are now seeing your key/value pairs being extracted into field names.

# Compatibility
This script should work with any modern Linux distro with a reasonably recent version of Python 3 and journald.  It has been tested on Ubuntu 18 and 20 LTS and Fedora 34.

# TODO
* Filtering logs being sent would be a cool feature.  Right now we simply send everything from journald which may not work in all situations.  There's some code commented out in journal2splunk which may help, but it is not tested in any way.  I'd prefer to make this a config file option.
