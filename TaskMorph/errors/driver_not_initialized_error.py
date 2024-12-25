class DriverNotInitializedError(Exception):
    def __init__(self) -> None:
        super().__init__('Inicialize o driver usando o método: `start_driver`')