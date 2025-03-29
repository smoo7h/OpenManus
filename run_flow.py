import asyncio
import glob
import os
import random
import time
from datetime import datetime
from pathlib import Path

from app.agent.manus import Manus
from app.config import config
from app.flow.flow_factory import FlowFactory, FlowType
from app.logger import logger


async def run_flow():
    agents = {
        "manus": Manus(),
    }

    original_cwd = os.getcwd()
    try:
        # --- Create unique task directory ---
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_dir_name = f"flow_run_{timestamp}"
        task_path = config.workspace_root / task_dir_name
        task_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created task directory: {task_path}")

        # --- Change CWD to task directory ---
        os.chdir(task_path)
        logger.info(f"Changed working directory to: {task_path}")

        prompt = input("Enter your prompt: ")

        if prompt.strip().isspace() or not prompt:
            logger.info(
                "No prompt provided, selecting a random prompt from the prompts/ directory"
            )
            try:
                prompt_files = glob.glob("prompts/*.txt")
                if not prompt_files:
                    logger.warning("No prompt files found in the prompts/ directory.")
                    return

                selected_prompt_file = random.choice(prompt_files)
                logger.info(f"Using prompt from: {selected_prompt_file}")
                with open(selected_prompt_file, "r") as f:
                    prompt = f.read()
                if not prompt.strip():
                    logger.warning(
                        f"Selected prompt file '{selected_prompt_file}' is empty."
                    )
                    return
            except Exception as e:
                logger.error(f"Error reading prompt file: {e}")
                return

        flow = FlowFactory.create_flow(
            flow_type=FlowType.PLANNING,
            agents=agents,
        )
        logger.warning("Processing your request...")

        try:
            # --- Execute Flow ---
            start_time = time.time()
            result = await asyncio.wait_for(
                flow.execute(prompt),
                timeout=3600,  # 60 minute timeout for the entire execution
            )
            elapsed_time = time.time() - start_time
            logger.info(f"Request processed in {elapsed_time:.2f} seconds")
            logger.info(result)
        except asyncio.TimeoutError:
            logger.error("Request processing timed out after 1 hour")
            logger.info(
                "Operation terminated due to timeout. Please try a simpler request."
            )

    except KeyboardInterrupt:
        logger.info("Operation cancelled by user.")
    except Exception as e:
        logger.error(f"Error: {str(e)}")

    finally:
        # --- Restore original CWD ---
        os.chdir(original_cwd)
        logger.info(f"Restored working directory to: {original_cwd}")


if __name__ == "__main__":
    asyncio.run(run_flow())
