from __future__ import annotations

class ConsoleIO:
    def read_int(self, prompt: str) -> int:
        return int(input(prompt))

    def write(self, text: str) -> None:
        print(text)
