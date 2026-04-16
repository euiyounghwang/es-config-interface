
#!/bin/bash
set -e

sudo kill -9 $(sudo lsof -t -i:9204)

echo "Stopped the services"