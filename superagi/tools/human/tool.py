from typing import Callable, Type

from pydantic import Field, BaseModel

from superagi.tools.base_tool import BaseTool


def print_func(text: str) -> None:
    print("\n")
    print(text)


class HumanInputSchema(BaseModel):
    query: str = Field(
        ...,
        description="Question for the human",
    )


class HumanInput(BaseTool):
    name = "Human"
    description = (
        "You can ask a human for guidance when you think you "
        "got stuck or you are not sure what to do next. "
        "The input should be a question for the human."
    )
    args_schema: Type[HumanInputSchema] = HumanInputSchema
    prompt_func: Callable[[str], None] = Field(default_factory=lambda: print_func)
    input_func: Callable = Field(default_factory=lambda: input)

    def _execute(self, query: str) -> str:
        self.prompt_func(query)
        return self.input_func()
