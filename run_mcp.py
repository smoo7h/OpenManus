#!/usr/bin/env python
import argparse
import asyncio
import glob
import os
import random
import sys
from datetime import datetime
from pathlib import Path

from app.agent.mcp import MCPAgent
from app.config import config
from app.logger import logger


class MCPRunner:
    """Runner class for MCP Agent with proper path handling and configuration."""

    def __init__(self):
        self.root_path = config.root_path
        self.server_reference = "app.mcp.server"
        self.agent = MCPAgent()

    async def initialize(
        self,
        connection_type: str,
        server_url: str | None = None,
    ) -> None:
        """Initialize the MCP agent with the appropriate connection."""
        logger.info(f"Initializing MCPAgent with {connection_type} connection...")

        if connection_type == "stdio":
            await self.agent.initialize(
                connection_type="stdio",
                command=sys.executable,
                args=["-m", self.server_reference],
            )
        else:  # sse
            await self.agent.initialize(connection_type="sse", server_url=server_url)

        logger.info(f"Connected to MCP server via {connection_type}")

    async def run_interactive(self) -> None:
        """Run the agent in interactive mode."""
        print("\nMCP Agent Interactive Mode (type 'exit' to quit)\n")
        while True:
            user_input = input("\nEnter your request: ")
            if user_input.lower() in ["exit", "quit", "q"]:
                break
            response = await self.agent.run(user_input)
            print(f"\nAgent: {response}")

    async def run_single_prompt(self, prompt: str) -> None:
        """Run the agent with a single prompt."""
        await self.agent.run(prompt)

    async def run_default(self) -> None:
        """Run the agent in default mode."""
        prompt = input("Enter your prompt: ")
        if not prompt.strip():
            logger.info(
                "No prompt provided, selecting a random prompt from the prompts/ directory"
            )
            try:
                # Use absolute path to the prompts directory from the project root
                prompts_path = os.path.join(self.root_path, "prompts", "*.txt")
                prompt_files = glob.glob(prompts_path)
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
        await self.agent.run(prompt)
        logger.info("Request processing completed.")

    async def cleanup(self) -> None:
        """Clean up agent resources."""
        await self.agent.cleanup()
        logger.info("Session ended")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run the MCP Agent")
    parser.add_argument(
        "--connection",
        "-c",
        choices=["stdio", "sse"],
        default="stdio",
        help="Connection type: stdio or sse",
    )
    parser.add_argument(
        "--server-url",
        default="http://127.0.0.1:8000/sse",
        help="URL for SSE connection",
    )
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Run in interactive mode"
    )
    parser.add_argument("--prompt", "-p", help="Single prompt to execute and exit")
    return parser.parse_args()


async def run_mcp() -> None:
    """Main entry point for the MCP runner."""
    args = parse_args()
    runner = MCPRunner()

    original_cwd = os.getcwd()
    try:
        # --- Create unique task directory ---
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_dir_name = f"mcp_run_{timestamp}"
        task_path = config.workspace_root / task_dir_name
        task_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created task directory: {task_path}")

        # --- Change CWD to task directory ---
        os.chdir(task_path)
        logger.info(f"Changed working directory to: {task_path}")

        # --- Initialize and run the agent ---
        await runner.initialize(args.connection, args.server_url)

        if args.prompt:
            await runner.run_single_prompt(args.prompt)
        elif args.interactive:
            await runner.run_interactive()
        else:
            await runner.run_default()

    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"Error running MCPAgent: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        # --- Restore original CWD ---
        os.chdir(original_cwd)
        logger.info(f"Restored working directory to: {original_cwd}")
        # --- Cleanup agent resources ---
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(run_mcp())
