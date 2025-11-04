"""Helper script to run data ingestion."""
import os
import sys

# Change to backend directory
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
os.chdir(backend_dir)

# Add backend to path
sys.path.insert(0, backend_dir)

# Run ingestion
if __name__ == "__main__":
    from ingest_data import main
    main()

