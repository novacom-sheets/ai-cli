"""Example: Logging plugin that adds request/response logging."""

import logging
from typing import Dict, Any
from datetime import datetime
from pydantic import Field

from ai_cli.plugins import Plugin, PluginConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_cli.logging_plugin")


class LoggingPluginConfig(PluginConfig):
    """Configuration for logging plugin."""
    log_requests: bool = Field(default=True, description="Log all requests")
    log_responses: bool = Field(default=True, description="Log all responses")
    log_file: str = Field(default="ai_cli.log", description="Log file path")


class LoggingPlugin(Plugin):
    """
    Plugin that logs all AI interactions.

    Adds logging for requests and responses with timestamps.
    """

    def __init__(self, config: LoggingPluginConfig = None):
        super().__init__(config or LoggingPluginConfig())
        self.config: LoggingPluginConfig

        # Setup file handler
        if self.config.log_file:
            handler = logging.FileHandler(self.config.log_file)
            handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            logger.addHandler(handler)

    def get_name(self) -> str:
        return "logging"

    def get_version(self) -> str:
        return "1.0.0"

    def get_schema_extensions(self) -> Dict[str, Dict[str, Any]]:
        """Add logging-related fields to requests."""
        return {
            "GenerateRequest": {
                "log_id": (str, Field(default="", description="Unique log ID for this request")),
            },
            "GenerateResponse": {
                "log_id": (str, Field(default="", description="Log ID from request")),
            }
        }

    def on_generate_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Log generation requests."""
        if self.config.log_requests:
            log_id = f"req_{datetime.now().timestamp()}"
            request["log_id"] = log_id

            logger.info(f"[{log_id}] Generate Request:")
            logger.info(f"  Model: {request.get('model')}")
            logger.info(f"  Prompt: {request.get('prompt')[:100]}...")

        return request

    def on_generate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Log generation responses."""
        if self.config.log_responses:
            log_id = response.get("log_id", "unknown")

            logger.info(f"[{log_id}] Generate Response:")
            logger.info(f"  Response: {response.get('response', '')[:100]}...")
            logger.info(f"  Duration: {response.get('total_duration', 0)}ns")

        return response


# Example usage
if __name__ == "__main__":
    from ai_cli.plugin_manager import get_global_manager

    # Create and register plugin
    config = LoggingPluginConfig(log_requests=True, log_responses=True)
    plugin = LoggingPlugin(config)

    manager = get_global_manager()
    manager.register_plugin(plugin)

    print(f"Registered plugin: {plugin.get_name()} v{plugin.get_version()}")
