"""質問スクリプトのテスト（Gemini APIを呼ばない）。"""

from types import SimpleNamespace

from app import ask


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        text="回答",
        usage_metadata=SimpleNamespace(
            prompt_token_count=12,
            candidates_token_count=34,
        ),
    )
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(
        ask.genai,
        "Client",
        lambda **_kwargs: SimpleNamespace(
            models=SimpleNamespace(
                generate_content=lambda **_kwargs: response,
            )
        ),
    )

    assert ask.ask("質問") == "回答"
    assert capsys.readouterr().out == "[トークン数] 入力: 12 / 出力: 34\n"


def test_ask_reports_missing_usage_metadata(monkeypatch, capsys):
    response = SimpleNamespace(text="回答", usage_metadata=None)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(
        ask.genai,
        "Client",
        lambda **_kwargs: SimpleNamespace(
            models=SimpleNamespace(
                generate_content=lambda **_kwargs: response,
            )
        ),
    )

    assert ask.ask("質問") == "回答"
    assert capsys.readouterr().out == "[トークン数] 使用量情報を取得できませんでした\n"
