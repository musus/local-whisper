# ローカルWhisper文字起こしツール

このツールは、OpenAIのWhisperモデルをローカル環境で使用して、音声ファイルをテキストに文字起こしします。

## 特徴

*   インターネット接続なしで文字起こしを実行可能（モデルダウンロード後）
*   複数のモデルサイズを選択可能（精度と速度のトレードオフ）
*   シンプルなコマンドラインインターフェース

## 必要なもの (Prerequisites)

*   **Python:** 3.7 以降 (pip を含む)
*   **ffmpeg:** Whisperが様々な音声フォーマットを処理するために必要です。
    *   **macOS (Homebrew):**
        ```bash
        brew install ffmpeg
        ```
    *   **Ubuntu/Debian:**
        ```bash
        sudo apt update && sudo apt install ffmpeg
        ```
    *   **Windows:** [公式サイト](https://ffmpeg.org/download.html) からダウンロードし、実行ファイルへのパスを環境変数に追加してください。

## インストール手順 (Installation)

1.  **リポジトリのクローン:**
    ```bash
    git clone <リポジトリURL>
    cd <リポジトリ名>
    ```
    または、このリポジトリのファイルをダウンロードして展開します。

2.  **(推奨) 仮想環境の作成と有効化:**
    ```bash
    python -m venv venv
    source venv/bin/activate      # Linux/macOS (bash/zsh など)
    source venv/bin/activate.fish # Linux/macOS (fish)
    # venv\Scripts\activate  # Windows
    ```

3.  **依存ライブラリのインストール:**
    ```bash
    pip install -r requirements.txt
    ```
    *(このコマンドは `whisper-openai` などをインストールします)*

## 使い方 (Usage)

基本的なコマンドは以下の通りです。

```bash
python transcribe.py <入力音声ファイルパス> [オプション]
```

**例:**
    
```bash
# audio/input.m4a をデフォルト設定 (baseモデル) で文字起こし
python transcribe.py audio/input.m4a

# 結果は audio/input.txt に保存される
```

### オプション

*   `-o <出力ファイルパス>`, `--output <出力ファイルパス>`:
    出力テキストファイルのパスを指定します。指定しない場合、入力ファイルと同じディレクトリに `<入力ファイル名>.txt` として保存されます。
    ```bash
    python transcribe.py audio/input.m4a -o text/output.txt
    ```
*   `-m <モデルサイズ>`, `--model <モデルサイズ>`:
    使用するWhisperモデルのサイズを指定します。デフォルトは `base` です。
    利用可能なサイズ: `tiny`, `base`, `small`, `medium`, `large`, `large-v1`, `large-v2`, `large-v3`
    ```bash
    # medium モデルを使用
    python transcribe.py audio/input.m4a -m medium
    ```

## モデルサイズについて

| モデル     | 精度 | 速度/リソース | 特徴                                  |
| :--------- | :--- | :------------ | :------------------------------------ |
| `tiny`     | 低   | 最速/最小     | 英語向け、非常に高速                  |
| `base`     | ↓    | ↓             | デフォルト、バランス型                |
| `small`    | ↓    | ↓             |                                       |
| `medium`   | ↓    | ↓             | 高精度、要求リソース増加              |
| `large`    | 高   | 最遅/最大     | 最高精度 (v1, v2, v3 バリエーションあり) |

*   モデルサイズが大きいほど、精度は向上しますが、処理時間が長くなり、より多くのメモリ（RAMおよびVRAM）を必要とします。
*   各モデルサイズを**初めて使用する際**には、モデルファイルのダウンロードが自動的に行われます（数GB単位になることもあります）。

## 注意点

*   **初回実行**: 初めてスクリプトを実行する際や、新しいモデルサイズを指定した際には、モデルのダウンロードに時間がかかることがあります。
*   **処理時間**: 長時間の音声ファイルや、CPUのみで大きなモデルを使用する場合、文字起こしにかなりの時間がかかることがあります。
*   **GPU高速化**: NVIDIA GPUとCUDAが利用可能な環境では、Whisperは自動的にGPUを使用し、処理速度が大幅に向上します。
*   **ffmpeg**: `ffmpeg` が見つからない場合、スクリプトはエラーを出力して終了します。インストール手順を確認してください。
*   **モデルファイル**: Whisperモデルは `.gitignore` によってGitの追跡対象から除外されています。モデルは実行時に自動的にダウンロード・キャッシュされるため、リポジトリに含める必要はありません。
*   **ファイル形式**: m4aなど多くの形式に対応していますが、問題が発生する場合は、`ffmpeg` を使って `wav` 形式などに変換してから試すことも有効です。
    ```bash
    # 例: ffmpeg を使って m4a を wav に変換
    ffmpeg -i input.m4a output.wav
    ``` 