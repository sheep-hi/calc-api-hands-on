import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


def create_html_response(content: str, status_code: int = 200) -> func.HttpResponse:
    """HTML形式のレスポンスを作成する"""
    html = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>計算結果</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                border-radius: 8px;
                padding: 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #333;
                text-align: center;
                margin-bottom: 20px;
            }}
            .result {{
                font-size: 24px;
                color: #0066cc;
                text-align: center;
                padding: 20px;
                background-color: #e8f4ff;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .error {{
                font-size: 18px;
                color: #cc0000;
                text-align: center;
                padding: 20px;
                background-color: #ffe8e8;
                border-radius: 5px;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {content}
        </div>
    </body>
    </html>
    """
    return func.HttpResponse(html, mimetype="text/html", status_code=status_code)


def validate_params(req: func.HttpRequest):
    """パラメータA, Bを検証し、浮動小数点数として返す"""
    try:
        a_str = req.params.get('A')
        b_str = req.params.get('B')
        
        if not a_str or not b_str:
            return None, None, 'パラメータAとBを指定してください'
        
        a = float(a_str)
        b = float(b_str)
        
        if a <= 0 or b <= 0:
            return None, None, 'AとBは正の数を指定してください'
        
        return a, b, None
    except ValueError:
        return None, None, 'AとBは数値で指定してください'


@app.route(route="multiply", methods=["GET", "POST"])
def multiply(req: func.HttpRequest) -> func.HttpResponse:
    """掛け算APIエンドポイント"""
    logging.info(f'Multiply function processed a request. Method: {req.method}')
    
    try:
        # ログにリクエスト情報を記録
        logging.info(f'Request details - Method: {req.method}, URL: {req.url}, Headers: {dict(req.headers)}')
        
        a, b, error = validate_params(req)
        
        if error:
            logging.warning(f'Validation error in multiply: {error}, Params: A={req.params.get("A")}, B={req.params.get("B")}')
            content = f'<h1>エラー</h1><div class="error">{error}</div>'
            return create_html_response(content, status_code=400)
        
        result = a * b
        
        logging.info(f'Multiply calculation successful: {a} × {b} = {result}')
        
        content = f'''
            <h1>掛け算の結果</h1>
            <div class="result">
                <p>{a} × {b} = {result}</p>
            </div>
        '''
        return create_html_response(content)
        
    except Exception as e:
        logging.error(f'Unexpected error in multiply: {str(e)}', exc_info=True)
        content = '<h1>エラー</h1><div class="error">予期しないエラーが発生しました</div>'
        return create_html_response(content, status_code=500)


@app.route(route="divide", methods=["GET", "POST"])
def divide(req: func.HttpRequest) -> func.HttpResponse:
    """割り算APIエンドポイント"""
    logging.info(f'Divide function processed a request. Method: {req.method}')
    
    try:
        # ログにリクエスト情報を記録
        logging.info(f'Request details - Method: {req.method}, URL: {req.url}, Headers: {dict(req.headers)}')
        
        a, b, error = validate_params(req)
        
        if error:
            logging.warning(f'Validation error in divide: {error}, Params: A={req.params.get("A")}, B={req.params.get("B")}')
            content = f'<h1>エラー</h1><div class="error">{error}</div>'
            return create_html_response(content, status_code=400)
        
        # ゼロ除算チェック（既にvalidate_paramsでb > 0を確認しているが念のため）
        if b == 0:
            logging.warning(f'Division by zero attempted: A={a}, B={b}')
            content = '<h1>エラー</h1><div class="error">0で割ることはできません</div>'
            return create_html_response(content, status_code=400)
        
        result = a / b
        
        logging.info(f'Divide calculation successful: {a} ÷ {b} = {result}')
        
        content = f'''
            <h1>割り算の結果</h1>
            <div class="result">
                <p>{a} ÷ {b} = {result}</p>
            </div>
        '''
        return create_html_response(content)
        
    except Exception as e:
        logging.error(f'Unexpected error in divide: {str(e)}', exc_info=True)
        content = '<h1>エラー</h1><div class="error">予期しないエラーが発生しました</div>'
        return create_html_response(content, status_code=500)
