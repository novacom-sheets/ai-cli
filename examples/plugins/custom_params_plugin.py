"""Example: Custom parameters plugin - adds new model parameters."""

from typing import Dict, Any
from pydantic import Field

from ai_cli.plugins import Plugin, PluginConfig


class CustomParamsPluginConfig(PluginConfig):
    """Configuration for custom parameters plugin."""
    enable_top_k: bool = Field(default=True, description="Enable top_k parameter")
    enable_repeat_penalty: bool = Field(default=True, description="Enable repeat_penalty")
    enable_seed: bool = Field(default=False, description="Enable seed parameter")


class CustomParamsPlugin(Plugin):
    """
    Plugin that adds custom model parameters.

    Demonstrates how to extend AgentConfig and GenerateRequest
    with new parameters that get passed to the model.
    """

    def __init__(self, config: CustomParamsPluginConfig = None):
        super().__init__(config or CustomParamsPluginConfig())
        self.config: CustomParamsPluginConfig

    def get_name(self) -> str:
        return "custom_params"

    def get_version(self) -> str:
        return "1.0.0"

    def get_schema_extensions(self) -> Dict[str, Dict[str, Any]]:
        """Add custom model parameters to schemas."""
        extensions = {}

        # Add to AgentConfig
        agent_fields = {}
        if self.config.enable_top_k:
            agent_fields["top_k"] = (
                int,
                Field(default=40, description="Top-K sampling parameter")
            )
        if self.config.enable_repeat_penalty:
            agent_fields["repeat_penalty"] = (
                float,
                Field(default=1.1, description="Repetition penalty parameter")
            )
        if self.config.enable_seed:
            agent_fields["seed"] = (
                int,
                Field(default=-1, description="Random seed for reproducibility")
            )

        if agent_fields:
            extensions["AgentConfig"] = agent_fields

        # Add to GenerateRequest
        request_fields = {}
        if self.config.enable_top_k:
            request_fields["top_k"] = (
                int,
                Field(default=40, description="Top-K sampling")
            )
        if self.config.enable_repeat_penalty:
            request_fields["repeat_penalty"] = (
                float,
                Field(default=1.1, description="Repetition penalty")
            )
        if self.config.enable_seed:
            request_fields["seed"] = (
                int,
                Field(default=-1, description="Random seed")
            )

        if request_fields:
            extensions["GenerateRequest"] = request_fields

        return extensions

    def on_agent_init(self, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """Process agent initialization with custom params."""
        # Custom params are automatically added via schema extensions
        # Here we can add validation or defaults

        if self.config.enable_top_k and "top_k" in agent_config:
            # Ensure top_k is in valid range
            top_k = agent_config["top_k"]
            if top_k < 1:
                agent_config["top_k"] = 40

        if self.config.enable_repeat_penalty and "repeat_penalty" in agent_config:
            # Ensure repeat_penalty is positive
            repeat_penalty = agent_config["repeat_penalty"]
            if repeat_penalty < 0:
                agent_config["repeat_penalty"] = 1.1

        return agent_config

    def on_generate_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Add custom params to request options."""
        if "options" not in request:
            request["options"] = {}

        # Transfer custom params to options dict for Ollama
        if self.config.enable_top_k and "top_k" in request:
            request["options"]["top_k"] = request["top_k"]

        if self.config.enable_repeat_penalty and "repeat_penalty" in request:
            request["options"]["repeat_penalty"] = request["repeat_penalty"]

        if self.config.enable_seed and "seed" in request:
            seed = request["seed"]
            if seed >= 0:
                request["options"]["seed"] = seed

        return request


# Example usage
if __name__ == "__main__":
    from ai_cli.plugin_manager import get_global_manager
    from ai_cli.types import AgentConfig

    # Create and register plugin
    config = CustomParamsPluginConfig(
        enable_top_k=True,
        enable_repeat_penalty=True,
        enable_seed=True
    )
    plugin = CustomParamsPlugin(config)

    manager = get_global_manager()
    manager.register_plugin(plugin)

    print(f"Registered plugin: {plugin.get_name()} v{plugin.get_version()}")

    # Now you can use the new parameters!
    agent_config = AgentConfig(
        name="custom_agent",
        role="Assistant with custom params",
        system_prompt="You are a helpful assistant.",
        top_k=50,  # New parameter added by plugin!
        repeat_penalty=1.2,  # New parameter!
        seed=42  # New parameter!
    )

    print("\nAgent config with custom params:")
    print(f"  top_k: {agent_config.top_k}")
    print(f"  repeat_penalty: {agent_config.repeat_penalty}")
    print(f"  seed: {agent_config.seed}")

    # Generate modelfile with custom params
    print("\nGenerated Modelfile:")
    print(agent_config.to_modelfile())
