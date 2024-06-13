#!/bin/bash
set -e

#tail -f ./logs/es_config_interface_api.log
sudo journalctl -u es_config_interface_api.service -f