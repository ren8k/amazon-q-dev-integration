# Amazon Bedrock Agent サンプルコード解説

このリポジトリには、Amazon Bedrock Agentを使用して情報を取得し、その出力を確認するためのサンプルコードが含まれています。このドキュメントでは、初心者の方でも簡単に理解できるよう、コードの使い方と出力の見方を説明します。

## 前提条件

- AWS アカウント
- Python 3.8以上
- boto3ライブラリ（AWS SDK for Python）
- Amazon Bedrock Agentの使用権限
- 設定済みのBedrockエージェント（ID、エイリアスIDが必要）

## セットアップ手順

1. **AWS認証情報の設定**:
   ```bash
   aws configure
   ```
   または、`~/.aws/credentials`ファイルに認証情報を設定します。

2. **依存ライブラリのインストール**:
   ```bash
   pip install boto3
   ```

3. **コードの準備**:
   `bedrock_agent_example.py`ファイル内の以下の部分を実際の値に更新してください：
   ```python
   AGENT_ID = "YOUR_AGENT_ID"  # 例: "ABCDEF123456"
   AGENT_ALIAS_ID = "YOUR_AGENT_ALIAS_ID"  # 例: "ZYXWVU987654"
   ```
   
   これらの値はAWS Bedrockコンソールから取得できます。

## 使用方法

1. スクリプトを実行します：
   ```bash
   python bedrock_agent_example.py
   ```

2. スクリプトは事前に定義された3つの質問をエージェントに送信し、各結果を表示します。
   必要に応じて、`main()`関数内の`queries`リストを編集して、独自の質問を追加・変更できます。

## 出力の見方

スクリプトは各質問に対して次のような出力を生成します：

```
🔍 エージェントへの問い合わせ: '会社の四半期財務レポートを要約してください。'

==================================================
📝 エージェントの回答:
--------------------------------------------------
[エージェントからの回答テキストがここに表示されます]
--------------------------------------------------

📚 引用情報:
  引用 1:
  - タイトル: [文書のタイトル]
  - ドキュメント: [文書の場所]
  - 抜粋: [文書からの抜粋]

  引用 2:
  - ...

🔍 詳細なトレース情報:
[JSONフォーマットの詳細なトレース情報]
```

### 出力の内容説明

1. **エージェントの回答**: 
   Bedrockエージェントが質問に対して生成した回答です。テキスト形式で表示されます。

2. **引用情報**:
   エージェントが回答を生成するために参照したデータソースに関する情報です。
   - **タイトル**: 参照された文書のタイトル
   - **ドキュメント**: 文書のストレージ場所やパス
   - **抜粋**: 参照された文書の関連部分

3. **詳細なトレース情報**:
   エージェントがどのように回答を生成したかに関する技術的な詳細です。JSON形式で表示され、以下の情報を含みます：
   - 検索された情報
   - 使用されたナレッジベース
   - レスポンス生成プロセスの詳細
   - 信頼度スコア
   - その他のメタデータ

## トラブルシューティング

### 一般的なエラー

1. **認証エラー**:
   ```
   エラー発生: An error occurred (AccessDeniedException) when calling the InvokeAgent operation: User is not authorized to perform bedrock-agent-runtime:InvokeAgent
   ```
   **解決策**: IAMポリシーに適切なBedrockのアクセス権限があるか確認してください。

2. **エージェントIDエラー**:
   ```
   エラー発生: An error occurred (ResourceNotFoundException) when calling the InvokeAgent operation: Agent with ID 'YOUR_AGENT_ID' not found
   ```
   **解決策**: 正しいエージェントIDとエイリアスIDを設定しているか確認してください。

3. **リージョンエラー**:
   ```
   エラー発生: An error occurred (UnrecognizedClientException) when calling the InvokeAgent operation: The security token included in the request is invalid.
   ```
   **解決策**: Bedrock Agentが利用可能なリージョンを使用しているか確認してください。

## 出力のカスタマイズ

コード内の`process_agent_response`関数を変更することで、出力形式をカスタマイズできます。例えば、特定の情報のみを表示したり、異なる形式で表示したりすることが可能です。

## 詳細なデバッグ

より詳細なデバッグ情報を確認したい場合は、`enableTrace=True`パラメータを使用していることを確認してください。これにより、エージェントの内部処理に関する詳細な情報が取得できます。

---

このサンプルコードとドキュメントが、Amazon Bedrock Agentの理解と利用の一助となれば幸いです。質問や問題がありましたら、お気軽にお問い合わせください。