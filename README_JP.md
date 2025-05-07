# Amazon Bedrock Knowledge Basesサンプルコード

このリポジトリには、Amazon Bedrock Knowledge Basesを使用してナレッジベースを作成し、クエリを実行する方法を示すサンプルコードが含まれています。

## 概要

Amazon Bedrock Knowledge Basesは、独自のデータをAmazon Bedrockの基盤モデル（FM）と接続できるサービスです。Knowledge Basesを使用すると、Retrieval Augmented Generation (RAG)パターンを実装して、独自のデータに基づいて回答を生成できます。

## 前提条件

- AWS アカウント（Amazon Bedrock へのアクセス権限あり）
- 適切なIAM権限を持つロール
- Python 3.6以上
- boto3ライブラリ (`pip install boto3`)

## 機能

このサンプルコードは以下の機能を示しています：

1. S3バケットの作成
2. サンプルデータファイルの作成とS3へのアップロード
3. Amazon Bedrock Knowledge Baseの作成
4. Knowledge Baseへのデータソースの追加
5. データ取り込みジョブの開始と監視
6. RAG（Retrieval Augmented Generation）を使用したナレッジベースのクエリ

## 使用方法

1. サンプルコードをダウンロードします
2. 必要なパッケージをインストールします：`pip install boto3`
3. `role_arn`変数を、適切な権限を持つIAMロールのARNに更新します
4. リージョンを必要に応じて変更します
5. スクリプトを実行します：`python bedrock_knowledge_base_sample.py`

## コードの説明

### S3バケットの作成
```python
def create_s3_bucket(bucket_name, region="XXXXXXXXX"):
    # バケットを作成するコード
```

### サンプルデータの作成と管理
```python
def create_sample_data_file(file_path):
    # サンプルデータファイルを作成するコード
    
def upload_file_to_s3(file_path, bucket_name, s3_key):
    # ファイルをS3にアップロードするコード
```

### ナレッジベースの作成と設定
```python
def create_knowledge_base(kb_name, role_arn, bucket_name, s3_prefix, region="us-east-1"):
    # ナレッジベースを作成するコード
    
def create_data_source(kb_id, data_source_name, bucket_name, s3_prefix, role_arn, region="us-east-1"):
    # データソースを作成するコード
    
def start_data_ingestion_job(kb_id, data_source_id, region="us-east-1"):
    # データ取り込みを開始するコード
```

### ナレッジベースのクエリ
```python
def query_knowledge_base(kb_id, query_text, model_id="anthropic.claude-v2", region="us-east-1"):
    # ナレッジベースにクエリを実行するコード
```

## 注意点

- このサンプルコードの実行には料金が発生する可能性があります。
- 作成したリソースが不要になった場合は削除してください。
- 実運用環境で使用する場合は、エラー処理やセキュリティを強化してください。

## 関連リソース

- [Amazon Bedrock ドキュメント](https://docs.aws.amazon.com/bedrock/)
- [Amazon Bedrock Knowledge Bases ユーザーガイド](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)