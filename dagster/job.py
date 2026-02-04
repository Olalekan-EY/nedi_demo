from dagster import op, job, Config
from typing import Dict, Optional
import requests
import subprocess
import os

# FastAPI server URL (using service name from docker network)
FASTAPI_BASE_URL = "http://fastapi:8000/api"


# ========== FastAPI Sync Operations ==========

@op
def push_examinations(context) -> Dict:
    """Call push_examinations endpoint"""
    try:
        response = requests.post(f"{FASTAPI_BASE_URL}/examinations/clickhouse")
        response.raise_for_status()
        result = response.json()
        context.log.info(f"push_examinations: {result}")
        return result
    except Exception as e:
        context.log.error(f"Error in push_examinations: {str(e)}")
        raise

@op
def push_teachers(context) -> Dict:
    """Call push_teachers endpoint"""
    try:
        response = requests.post(f"{FASTAPI_BASE_URL}/teachers/clickhouse")
        response.raise_for_status()
        result = response.json()
        context.log.info(f"push_teachers: {result}")
        return result
    except Exception as e:
        context.log.error(f"Error in push_teachers: {str(e)}")
        raise

@op
def push_students(context) -> Dict:
    """Call push_students endpoint"""
    try:
        response = requests.post(f"{FASTAPI_BASE_URL}/students/clickhouse")
        response.raise_for_status()
        result = response.json()
        context.log.info(f"push_students: {result}")
        return result
    except Exception as e:
        context.log.error(f"Error in push_students: {str(e)}")
        raise

@op
def push_schools(context) -> Dict:
    """Call push_schools endpoint"""
    try:
        response = requests.post(f"{FASTAPI_BASE_URL}/schools/clickhouse")
        response.raise_for_status()
        result = response.json()
        context.log.info(f"push_schools: {result}")
        return result
    except Exception as e:
        context.log.error(f"Error in push_schools: {str(e)}")
        raise


# ========== DBT Operations ==========

class DbtConfig(Config):
    """Configuration for dbt operations"""
    project_dir: str = "/app/dbt"  # Mount dbt folder at /app/dbt in dagster_user_code container
    profiles_dir: str = "/app/dbt/profiles"
    target: str = "dev"
    select: Optional[str] = None  # Optional: select specific models (e.g., "staging.*" or "build.*")
    full_refresh: bool = False


@op
def run_dbt_models(context, config: DbtConfig, sync_result: Dict = None) -> Dict:
    """Run dbt staging and build models to transform ClickHouse data"""
    try:
        if sync_result:
            context.log.info(f"Running dbt after sync completion: {list(sync_result.keys())}")
        # Set environment variables for dbt
        env = os.environ.copy()
        env["DBT_PROFILES_DIR"] = config.profiles_dir
        
        # Build dbt command - select staging and build models
        cmd = [
            "dbt", "run",
            "--project-dir", config.project_dir,
            "--profiles-dir", config.profiles_dir,
            "--target", config.target
        ]
        
        # Add select if specified, otherwise select all staging and build models
        if config.select:
            cmd.extend(["--select", config.select])
        else:
            # Select all staging and build models using path selectors
            cmd.extend(["--select", "path:models/transformations/staging", "path:models/transformations/build"])
        
        # Add full-refresh if needed
        if config.full_refresh:
            cmd.append("--full-refresh")
        
        context.log.info(f"Running dbt command: {' '.join(cmd)}")
        
        # Execute dbt command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
            cwd=config.project_dir
        )
        
        if result.returncode != 0:
            context.log.error(f"dbt run failed with exit code {result.returncode}")
            context.log.error(f"stdout: {result.stdout}")
            context.log.error(f"stderr: {result.stderr}")
            raise Exception(f"dbt run failed: {result.stdout}\n{result.stderr}")
        
        context.log.info(f"dbt run succeeded: {result.stdout}")
        return {
            "status": "success",
            "stdout": result.stdout,
            "stderr": result.stderr
        }
        
    except Exception as e:
        context.log.error(f"Error running dbt: {str(e)}")
        raise


@op
def test_dbt_models(context, config: DbtConfig, run_result: Dict) -> Dict:
    """Test dbt staging and build models for data quality"""
    try:
        env = os.environ.copy()
        env["DBT_PROFILES_DIR"] = config.profiles_dir
        
        cmd = [
            "dbt", "test",
            "--project-dir", config.project_dir,
            "--profiles-dir", config.profiles_dir,
            "--target", config.target
        ]
        
        # Add select if specified, otherwise select all staging and build models
        if config.select:
            cmd.extend(["--select", config.select])
        else:
            # Select all staging and build models using path selectors
            cmd.extend(["--select", "path:models/transformations/staging", "path:models/transformations/build"])
        
        context.log.info(f"Running dbt test: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
            cwd=config.project_dir
        )
        
        if result.returncode != 0:
            context.log.warning(f"dbt test warnings: {result.stderr}")
            # Don't fail the job on test failures, just log them
            return {
                "status": "warning",
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        
        context.log.info(f"dbt test passed: {result.stdout}")
        return {
            "status": "success",
            "stdout": result.stdout
        }
        
    except Exception as e:
        context.log.error(f"Error running dbt test: {str(e)}")
        raise


# ========== Jobs ==========

@job
def sync_to_clickhouse():
    """Job that calls all FastAPI endpoints concurrently"""
    # All ops run concurrently since they have no dependencies
    push_examinations()
    push_teachers()
    push_students()
    push_schools()


@job
def run_dbt_transformations():
    """Job to run dbt staging and build transformations on ClickHouse data"""
    # Run models first, then test them
    run_result = run_dbt_models()
    # Test depends on run completing successfully
    test_result = test_dbt_models(run_result)


@op
def wait_for_sync(context, exam_result: Dict, teacher_result: Dict, student_result: Dict, school_result: Dict) -> Dict:
    """Wait for all sync operations to complete before proceeding"""
    context.log.info("All sync operations completed successfully")
    return {
        "examinations": exam_result,
        "teachers": teacher_result,
        "students": student_result,
        "schools": school_result
    }


@job
def execute_data_pipeline():
    """
    Complete data pipeline that:
    1. Syncs data from PostgreSQL to ClickHouse
    2. Runs dbt transformations to create staging and build models
    3. Tests the transformed data
    """
    # Step 1: Sync all data to ClickHouse (runs concurrently)
    exam_result = push_examinations()
    teacher_result = push_teachers()
    student_result = push_students()
    school_result = push_schools()
    
    # Step 2: Wait for all syncs to complete
    sync_complete = wait_for_sync(exam_result, teacher_result, student_result, school_result)
    
    # Step 3: Run dbt models after all data is synced
    dbt_result = run_dbt_models(sync_result=sync_complete)
    
    # Step 4: Test dbt models
    test_result = test_dbt_models(dbt_result)
