from typing import Callable, Dict

from loguru import logger

from app.schemas.iris.methods import IrisDutyEventMethod


class Route:
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
        self.my_signal_handlers: Dict[str, Callable] = {}
        self.signal_handlers: Dict[str, Callable] = {}

    def method_handler(self, method: IrisDutyEventMethod):
        def decorator(func: Callable):
            if method in self.handlers:
                logger.warning(f"Handler for method '{method}' is already registered.")
            self.handlers[method] = func
            return func

        return decorator

    def my_signal_handler(self, commands: list[str]):
        def decorator(func: Callable):
            for command in commands:
                if command in self.my_signal_handlers:
                    logger.warning(
                        f"Handler for command '{command}' is already registered."
                    )
                self.my_signal_handlers[command] = func
            return func

        return decorator

    def signal_handler(self, commands: list[str]):
        def decorator(func: Callable):
            for command in commands:
                if command in self.signal_handlers:
                    logger.warning(
                        f"Handler for command '{command}' is already registered."
                    )
                self.signal_handlers[command] = func
            return func

        return decorator

    def get_handler(self, method: IrisDutyEventMethod) -> Callable:
        """Return the handler based on the IrisDutyEventMethod."""
        return self.handlers.get(method, None)

    def get_my_signal_handler(self, command: str) -> Callable:
        """Return the handler based on the command."""
        return self.my_signal_handlers.get(command, None)

    def get_signal_handler(self, command: str) -> Callable:
        """Return the handler based on the command."""
        return self.signal_handlers.get(command, None)


route = Route()
