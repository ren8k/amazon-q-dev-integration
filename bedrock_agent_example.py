"""
Amazon Bedrock Agentのサンプルコード
このコードは初心者向けに、Amazon Bedrock Agentの出力を確認する方法を示します。
"""
import boto3
import json
import time
from botocore.config import Config

# 日本語コメント: AWSの認証情報と設定
# AWS認証情報を設定します（AWSプロファイルを使用するか、適切な認証情報を設定してください）
# リージョンはAmazon Bedrock Agentが利用可能なリージョンを選択します
config = Config(
    region_name="us-east-1",  # 必要に応じてリージョンを変更してください
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

# 日本語コメント: Bedrock Agentクライアントを初期化
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', config=config)

# 日本語コメント: Agentの問い合わせ関数
def query_agent(agent_id, agent_alias_id, prompt, enable_trace=True):
    """
    Bedrockエージェントに問い合わせを行う関数
    
    引数:
        agent_id (str): エージェントのID
        agent_alias_id (str): エージェントエイリアスのID
        prompt (str): エージェントに送信するプロンプト
        enable_trace (bool): トレース情報を表示するかどうか
        
    戻り値:
        dict: エージェントからのレスポンス
    """
    print(f"\n🔍 エージェントへの問い合わせ: '{prompt}'")
    
    # エージェントへのリクエストを作成
    response = bedrock_agent_runtime.invoke_agent(
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=f"session-{int(time.time())}",  # セッションIDを一意に生成
        inputText=prompt,
        enableTrace=enable_trace
    )
    
    return process_agent_response(response)

# 日本語コメント: エージェントのレスポンス処理関数
def process_agent_response(response):
    """
    Bedrockエージェントのレスポンスを処理する関数
    
    引数:
        response: エージェントからの生のレスポンス
        
    戻り値:
        dict: 整形されたレスポンス情報
    """
    result = {
        "completion": "",
        "trace_info": {},
        "citations": []
    }
    
    # レスポンスストリームを処理
    for event in response.get("completion"):
        if "chunk" in event:
            chunk = json.loads(event["chunk"]["bytes"].decode())
            if "content" in chunk:
                for content_item in chunk["content"]:
                    if content_item.get("type") == "text":
                        result["completion"] += content_item.get("text", "")
    
    # トレース情報の取得（デバッグ用）
    if "trace" in response:
        trace_data = json.loads(response["trace"]["completionDetails"]["sourceAttribution"]["citations"])
        result["trace_info"] = trace_data
        
        # 引用情報を整形
        for citation in trace_data.get("citations", []):
            result["citations"].append({
                "title": citation.get("title", "不明"),
                "document": citation.get("retrievedReferences", {}).get("document", {}).get("location", "不明"),
                "excerpt": citation.get("textPart", "不明")
            })
    
    return result

# 日本語コメント: メイン関数
def main():
    """
    メイン実行関数 - エージェントへの問い合わせと結果表示を行います
    """
    # 実際のエージェントIDとエイリアスIDを設定してください
    # これらの値はAWS Bedrockコンソールから取得できます
    AGENT_ID = "YOUR_AGENT_ID"  # 例: "ABCDEF123456"
    AGENT_ALIAS_ID = "YOUR_AGENT_ALIAS_ID"  # 例: "ZYXWVU987654"
    
    # エージェントへの問い合わせ例
    queries = [
        "会社の四半期財務レポートを要約してください。",
        "製品Xの販売データを分析してください。",
        "顧客満足度調査の結果から主要な洞察を教えてください。"
    ]
    
    for query in queries:
        try:
            response = query_agent(AGENT_ID, AGENT_ALIAS_ID, query)
            
            # 結果の表示
            print("\n" + "="*50)
            print("📝 エージェントの回答:")
            print("-"*50)
            print(response["completion"])
            print("-"*50)
            
            # 引用情報があれば表示
            if response["citations"]:
                print("\n📚 引用情報:")
                for i, citation in enumerate(response["citations"]):
                    print(f"  引用 {i+1}:")
                    print(f"  - タイトル: {citation['title']}")
                    print(f"  - ドキュメント: {citation['document']}")
                    print(f"  - 抜粋: {citation['excerpt']}")
                    print()
            
            # トレース情報の詳細を表示（デバッグ用）
            print("\n🔍 詳細なトレース情報:")
            print(json.dumps(response["trace_info"], indent=2, ensure_ascii=False))
            
        except Exception as e:
            print(f"エラー発生: {str(e)}")
    
    print("\n✨ 完了")

# スクリプトが直接実行された場合にメイン関数を呼び出し
if __name__ == "__main__":
    main()