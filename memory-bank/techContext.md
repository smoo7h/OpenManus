# OpenManus Technical Context

## Technologies Used

### Core Technologies

1. **Python 3.12**: The primary programming language for the project, chosen for its readability, extensive libraries, and strong support for AI/ML applications.

2. **Pydantic**: Used for data validation, settings management, and schema definition throughout the codebase.

3. **Asyncio**: Provides asynchronous programming capabilities, enabling efficient handling of concurrent operations.

4. **Docker**: Used for containerization and sandbox isolation of potentially risky operations.

5. **Playwright**: Powers browser automation capabilities, allowing the agent to interact with web pages.

### Language Models

OpenManus is designed to work with various LLM providers:

1. **OpenAI API**: Support for GPT models (default: gpt-4o)
2. **Anthropic API**: Support for Claude models (default: claude-3-7-sonnet)
3. **AWS Bedrock**: Integration with Amazon's LLM service
4. **Azure OpenAI**: Support for Microsoft's hosted OpenAI models
5. **Ollama**: Local LLM support for self-hosted deployments

The system is designed to be model-agnostic, with configuration options to specify the preferred model and provider.

### Development Tools

1. **Pre-commit**: Enforces code quality standards and formatting before commits
2. **TOML**: Used for configuration files
3. **Git**: Version control system

## Development Setup

### Environment Setup

OpenManus supports two installation methods:

1. **Conda-based setup**:
   ```bash
   conda create -n open_manus python=3.12
   conda activate open_manus
   pip install -r requirements.txt
   ```

2. **UV-based setup** (recommended):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv venv --python 3.12
   source .venv/bin/activate  # On Unix/macOS
   uv pip install -r requirements.txt
   ```

### Configuration

The system requires configuration via a `config.toml` file in the `config` directory:

```toml
# Global LLM configuration
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # API key required
max_tokens = 4096
temperature = 0.0

# Optional configuration for specific LLM models
[llm.vision]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # API key required
```

Additional optional configurations include:
- Browser settings
- Proxy configuration
- Search engine preferences
- Sandbox settings

### Project Structure

```
OpenManus/
├── app/                    # Core application code
│   ├── agent/              # Agent implementations
│   ├── flow/               # Multi-agent workflows
│   ├── mcp/                # Model Context Protocol support
│   ├── prompt/             # System and task prompts
│   ├── sandbox/            # Sandbox isolation
│   └── tool/               # Tool implementations
├── assets/                 # Static assets
├── config/                 # Configuration files
├── examples/               # Example use cases
├── tests/                  # Test suite
└── workspace/              # Working directory for agents
```

## Technical Constraints

### API Dependencies

- **LLM API Access**: Requires valid API keys for the chosen LLM provider
- **Rate Limits**: Subject to rate limiting by API providers
- **Token Limits**: Constrained by model context windows (typically 4K-8K tokens)

### System Requirements

- **Python 3.12**: Required for core functionality
- **Docker** (optional): Required for sandbox isolation
- **Memory**: Varies based on usage, but minimum 4GB RAM recommended
- **Disk Space**: Minimal for the core system, but workspace may grow based on usage

### Browser Automation

- **Playwright**: Required for browser automation features
- **Chromium/Chrome**: Used as the default browser for automation

### Network Requirements

- **Internet Access**: Required for LLM API calls and web browsing features
- **Firewall Considerations**: Outbound connections to API endpoints needed

## Dependencies

### Core Dependencies

```
pydantic>=2.0.0
aiohttp>=3.8.5
toml>=0.10.2
playwright>=1.40.0
docker>=6.1.3
```

### Optional Dependencies

```
# For AWS Bedrock support
boto3>=1.28.38

# For search capabilities
duckduckgo-search>=3.9.9
```

### Development Dependencies

```
pre-commit>=3.3.3
pytest>=7.4.0
pytest-asyncio>=0.21.1
```

## Integration Points

### External APIs

1. **LLM Providers**: Primary integration for reasoning and decision-making
2. **Search Engines**: Google, DuckDuckGo, Baidu for information retrieval
3. **Web Services**: Through browser automation

### File System

- **Workspace Directory**: Used for storing agent-generated files
- **Configuration Directory**: Stores user configuration

### Process Isolation

- **Docker Containers**: Used for sandboxing Python execution and terminal commands
- **Browser Processes**: Managed through Playwright

## Performance Considerations

- **Asynchronous Design**: Enables efficient handling of concurrent operations
- **LLM Latency**: Response times are primarily determined by LLM API performance
- **Memory Usage**: Grows with conversation history and context
- **Sandbox Overhead**: Docker-based sandboxing adds some performance overhead

## Security Considerations

- **API Key Management**: Keys stored in local configuration files
- **Sandbox Isolation**: Potentially risky operations contained in Docker
- **Browser Security**: Options to disable security features for testing
- **Code Execution**: Python code execution carries inherent risks
