#!/usr/bin/env bash

dev_appserver.py --host=localhost --port=8080 \
                 --admin_port=9080 --datastore_path=datastore.sqlite3 \
                 --skip_sdk_update_check=True --show_mail_body=True \
                 .
