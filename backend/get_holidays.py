import json
import urllib.request

def lambda_handler(event, context):
    # パラメータから年を取得
    for p in event.get('parameters', []):
        if p.get('name') == 'year':
            year = p.get('value')
    
    # 祝日データを取得
    url = f"https://holidays-jp.github.io/api/v1/{year}/date.json"
    with urllib.request.urlopen(url) as response:
        holidays = json.loads(response.read())
    
    # 結果を整形
    text = f"{year}年の日本の祝日:\n"
    for date, name in sorted(holidays.items()):
        text += f"{date}: {name}\n"
    
    # Bedrockエージェント用のレスポンス
    return {
        'response': {
            'actionGroup': event['actionGroup'],
            'function': event['function'],
            'functionResponse': {
                'responseBody': {
                    'TEXT': {'body': text}
                }
            }
        },
        'messageVersion': event.get('messageVersion', 1)
    }