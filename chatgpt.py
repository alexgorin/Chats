import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def get_completion(prompt, model="gpt-3.5-turbo", temperature=0):
    return get_completion_from_messages([{"role": "user", "content": prompt}], model, temperature)


class IO:
    def get_user_input(self) -> str:
        raise NotImplementedError

    def output(self, user: str, message: str) -> None:
        raise NotImplementedError


class CLI(IO):
    def get_user_input(self) -> str:
        return input()

    def output(self, user: str, message: str) -> None:
        print(f"{user}: {message}")


class Chat:
    def __init__(self, context: list[dict[str, str]], io: IO):
        self._context = context
        self._io = io

    def get_input(self):
        prompt = self._io.get_user_input()
        self._context.append({'role': 'user', 'content': f"{prompt}"})

    def reply(self) -> None:
        response = get_completion_from_messages(self._context)
        self._context.append({'role': 'assistant', 'content': f"{response}"})
        self._io.output('assistant', response)


def main():
    context = [{'role': 'system', 'content': """
       You are Mean Advisor, an automated service
       to ask people about their problems and give them bad advice.
       You first greet the customer in a passive-aggressive way,
       then ask him about his problems.
       Then depending on the type of issue, give one of the following advices:
       - if the problem is related to his family, recommend a divorce;
       - if the problem is related to his job, recommend quitting
       and starting some criminal career and give two examples;
       - otherwise, recommend a psychotherapist.
       Finish with a mean comment.
       Style your responses like Cartman from South Park.
   """}]

    chat = Chat(context, CLI())
    while True:
        chat.get_input()
        chat.reply()


if __name__ == "__main__":
    main()
