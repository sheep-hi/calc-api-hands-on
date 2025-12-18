# Azure Functions - 計算API

Azure Functions (Python) を使用した掛け算と割り算のAPIプロジェクト。

## プロジェクト構成

```
calc-api-hands-on/
├── docs/                    # ドキュメント
│   ├── requirements.md      # 機能要件
│   └── nonrequirements.md   # 非機能要件
├── src/                     # ソースコード
│   ├── function_app.py      # メインのFunctions実装
│   ├── requirements.txt     # Python依存パッケージ
│   ├── host.json            # Functions設定
│   └── local.settings.json  # ローカル実行設定
└── tests/                   # テストコード
    └── test_function_app.py # 単体テスト
```

## API仕様

### 1. 掛け算API
- **エンドポイント:** `/api/multiply`
- **メソッド:** GET, POST
- **パラメータ:** A (正の小数), B (正の小数)
- **レスポンス:** HTML形式で計算結果を表示

### 2. 割り算API
- **エンドポイント:** `/api/divide`
- **メソッド:** GET, POST
- **パラメータ:** A (正の小数), B (正の小数)
- **レスポンス:** HTML形式で計算結果を表示

## ローカル開発環境のセットアップ

### 必要なツール
- Python 3.11
- Azure Functions Core Tools v4
- Visual Studio Code (推奨)
- Azure Functions 拡張機能 (推奨)

### インストール手順

1. **リポジトリのクローン**
   ```powershell
   git clone <repository-url>
   cd calc-api-hands-on
   ```

2. **Python仮想環境の作成**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **依存パッケージのインストール**
   ```powershell
   cd src
   pip install -r requirements.txt
   ```

4. **Azure Functions Core Toolsのインストール**
   ```powershell
   npm install -g azure-functions-core-tools@4 --unsafe-perm true
   ```

### ローカル実行

1. **Functionsの起動**
   ```powershell
   cd src
   func start
   ```

2. **ブラウザでアクセス**
   - 掛け算: `http://localhost:7071/api/multiply?A=10&B=5`
   - 割り算: `http://localhost:7071/api/divide?A=10&B=5`

### テストの実行

1. **テスト用パッケージのインストール**
   ```powershell
   pip install pytest pytest-cov
   ```

2. **単体テストの実行**
   ```powershell
   # プロジェクトルートディレクトリで実行
   python -m pytest tests/ -v
   ```

3. **カバレッジ測定**
   ```powershell
   python -m pytest tests/ --cov=src --cov-report=html --cov-report=term
   ```
   - カバレッジレポートは `htmlcov/index.html` で確認可能

## Azure へのデプロイ

### GitHub Actions を使用したデプロイ

このプロジェクトは GitHub Actions を使用して Azure Functions へのデプロイを自動化できます。

1. **Azure Functions アプリの作成**
   - Azure Portal で Functions アプリを作成
   - ランタイム: Python 3.11
   - リージョン: 東日本
   - プラン: Consumption Plan

2. **GitHub Secrets の設定**
   リポジトリの Settings > Secrets に以下を追加:
   - `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`: Functions アプリの公開プロファイル

3. **デプロイの実行**
   - main ブランチへのプッシュで自動デプロイ
   - または GitHub Actions タブから手動実行

### 手動デプロイ (Azure CLI)

```powershell
# Azureにログイン
az login

# リソースグループの作成
az group create --name <resource-group-name> --location japaneast

# Functions アプリの作成
az functionapp create --resource-group <resource-group-name> --consumption-plan-location japaneast --runtime python --runtime-version 3.11 --functions-version 4 --name <functionapp-name> --storage-account <storage-account-name> --os-type Linux

# デプロイ
cd src
func azure functionapp publish <functionapp-name>
```

## エラーハンドリング

以下のエラーケースに対応しています:

- **パラメータ未指定:** パラメータAまたはBが指定されていない
- **数値以外の入力:** 数値として解釈できない値
- **負の数またはゼロ:** 0以下の値が指定された
- **ゼロ除算:** 割り算APIでBに0が指定された (バリデーションで防止)

すべてのエラーはHTMLページで分かりやすく表示されます。

## ロギング

以下の情報がログに記録されます:

- リクエストの詳細 (メソッド、URL、ヘッダー)
- 入力パラメータ (A, B)
- 計算結果
- エラー情報 (バリデーションエラー、例外)

ログは Azure Portal の Application Insights で確認できます。

## ライセンス

このプロジェクトは学習用途で作成されています。
