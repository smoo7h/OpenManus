import asyncio
import glob
import os
import random

from app.agent.manus import Manus
from app.logger import logger


async def main():
    agent = Manus()
    try:
        prompt = input("Enter your prompt: ")
        if not prompt.strip():
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

        logger.warning("Processing your request...")
        await agent.run(prompt)
        logger.info("Request processing completed.")
    except KeyboardInterrupt:
        logger.warning("Operation interrupted.")


if __name__ == "__main__":
    asyncio.run(main())
