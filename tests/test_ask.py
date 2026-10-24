from types import SimpleNamespace

from app import ask


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=34),
        text="回答です",
    )

    class FakeModels:
        def generate_content(self, **kwargs):
            return response

    class FakeClient:
        def __init__(self, api_key):
            self.models = FakeModels()

    monkeypatch.setattr(ask.genai, "Client", FakeClient)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")

    assert ask.ask("質問") == "回答です"
    output = capsys.readouterr().out
    assert "入力: 12 tokens" in output
    assert "出力: 34 tokens" in output


def test_interactive_mode_keeps_the_same_chat_for_follow_up_questions(
    monkeypatch, capsys
):
    questions = []

    class FakeChat:
        def send_message(self, question):
            questions.append(question)
            return SimpleNamespace(
                usage_metadata=None,
                text=f"{question}への回答",
            )

    chat = FakeChat()

    class FakeChats:
        def create(self, **kwargs):
            assert kwargs == {"model": ask.MODEL}
            return chat

    class FakeClient:
        def __init__(self, api_key):
            assert api_key == "test-key"
            self.chats = FakeChats()

    monkeypatch.setattr(ask.genai, "Client", FakeClient)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")
    answers = iter(("続きの質問", ""))
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr("sys.argv", ["app.ask", "--interactive", "最初の質問"])

    ask.main()

    assert questions == ["最初の質問", "続きの質問"]
    assert "続きの質問への回答" in capsys.readouterr().out