#!/bin/bash
# Script to run Experiment 2 in Docker

echo "Starting Experiment 2 in Docker container..."
echo ""

docker run -it --rm --privileged \
  -v "$(pwd)":/workspace \
  -w /workspace \
  -e SKIP_CLI=1 \
  iwaseyusuke/mininet \
  bash -c "sudo -E python3 exp2.py"

echo ""
echo "Experiment 2 completed! Check result2.txt for results."

