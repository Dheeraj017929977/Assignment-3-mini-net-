#!/bin/bash
# Script to run Experiment 1 in Docker

echo "Starting Experiment 1 in Docker container..."
echo ""

docker run -it --rm --privileged \
  -v "$(pwd)":/workspace \
  -w /workspace \
  -e SKIP_CLI=1 \
  iwaseyusuke/mininet \
  bash -c "sudo -E python3 exp1.py"

echo ""
echo "Experiment 1 completed! Check result1.txt for results."

