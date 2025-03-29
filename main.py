import asyncio
import os

from app.agent.manus import Manus
from app.logger import logger


async def main():
    agent = Manus()
    try:
        prompt = input("Enter your prompt: ")
        if not prompt.strip():
            logger.info(
                "No prompt provided, using default prompt from prompts/prompt.txt"
            )
            try:
                prompt_file_path = "prompts/prompt.txt"
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

        logger.warning("Processing your request...")
        await agent.run(prompt)
        logger.info("Request processing completed.")
    except KeyboardInterrupt:
        logger.warning("Operation interrupted.")


if __name__ == "__main__":
    asyncio.run(main())
