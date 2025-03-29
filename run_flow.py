import asyncio
import os
import time

from app.agent.manus import Manus
from app.flow.flow_factory import FlowFactory, FlowType
from app.logger import logger


async def run_flow():
    agents = {
        "manus": Manus(),
    }

    try:
        prompt = input("Enter your prompt: ")

        prompt_file_path = "prompts/prompt.txt"
        if prompt.strip().isspace() or not prompt:
            logger.info(
                "No prompt provided, using default prompt from prompts/prompt.txt"
            )
            try:
                if os.path.exists(prompt_file_path):
                    with open(prompt_file_path, "r") as f:
                        prompt = f.read()
                    if not prompt.strip():
                        logger.warning("Default prompt file is empty.")
                        return
                else:
                    logger.warning("Default prompt file not found.")
                    return
            except Exception as e:
                logger.error(f"Error reading default prompt file: {e}")
                return

        flow = FlowFactory.create_flow(
            flow_type=FlowType.PLANNING,
            agents=agents,
        )
        logger.warning("Processing your request...")

        try:
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


if __name__ == "__main__":
    asyncio.run(run_flow())
