# Description: This script creates the directory structure and files for the Elevtus Assessment project.

#!/bin/bash

# Create main directory structure
mkdir -p elevtus_assessment/app/models elevtus_assessment/app/services elevtus_assessment/app/repositories elevtus_assessment/app/routers elevtus_assessment/app/core elevtus_assessment/tests

# Create files in app directory
touch elevtus_assessment/app/main.py

# Create files in models directory
touch elevtus_assessment/app/models/user.py
touch elevtus_assessment/app/models/candidate.py

# Create files in services directory
touch elevtus_assessment/app/services/user_service.py
touch elevtus_assessment/app/services/candidate_service.py

# Create files in repositories directory
touch elevtus_assessment/app/repositories/user_repository.py
touch elevtus_assessment/app/repositories/candidate_repository.py

# Create files in routers directory
touch elevtus_assessment/app/routers/user.py
touch elevtus_assessment/app/routers/candidate.py

# Create files in core directory
touch elevtus_assessment/app/core/config.py
touch elevtus_assessment/app/core/security.py

# Create files in tests directory
touch elevtus_assessment/tests/test_user.py
touch elevtus_assessment/tests/test_candidate.py

# Create root level files
touch elevtus_assessment/Dockerfile
touch elevtus_assessment/docker-compose.yml
touch elevtus_assessment/requirements.txt

echo "Directory structure and files created successfully!"