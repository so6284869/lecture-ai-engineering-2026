# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：素のLLMは「初級・中級・上級」の一般論を答え、講座固有の内容を誤って推測した。エージェントは用語集を参照し、「基礎・実装・発展」の3段階で、どれか1つに取り組めばよいと答えた。
- `--trace` で見えたツール呼び出し（ツール名と引数）：`search_glossary`（`query: "3レベル"`）
- 1つの質問での LLM 呼び出し回数（`requests`）：2回（今回の実行結果）
- 追加したツールと、docstring に書いた説明：`make_quiz(lecture: int)`を追加した。docstringには「指定した回の用語で理解確認問題を1問作る必要があるときに使う。lectureには対象の回（1始まり）を指定する」と記載した。

## 宿題

- 取り組んだレベル：発展（a）Google ADK
- やったこと：`adk_agent/glossary_agent/`にADK用の`root_agent`を作成し、既存の`INSTRUCTIONS`と`search_glossary`・`get_lecture_summary`・`make_quiz`を登録した。`PYTHONPATH=. uv run --with google-adk adk run adk_agent/glossary_agent`で起動し、演習と同じ質問をした。
- 結果：ADK版も用語集をもとに「基礎・実装・発展」の3段階と回答し、どれか1つに取り組めばよいと説明した。Pydantic AI版と内容はほぼ同じで、ADK版は最後を「第1回」としていた。
- 気づき・疑問：Pydantic AI版は`Agent(instructions=...)`を作ってから`tool_plain()`でツールを登録する。ADK版は`Agent`の作成時に`instruction`と`tools`を渡し、`root_agent`として公開する。ADK版の`adk run`では今回の確認に使った回答やツールの情報は表示されたが、Pydantic AIの`--trace`のような形式や`requests`の値は確認できなかった。
