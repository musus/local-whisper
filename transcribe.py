import whisper
import argparse
import os
import sys

def transcribe_audio(input_file, output_file, model_size="base"):
    """
    Whisperを使用して音声ファイルを文字起こしします。

    Args:
        input_file (str): 入力音声ファイルのパス。
        output_file (str): 出力テキストファイルのパス。
        model_size (str): 使用するWhisperモデルのサイズ (例: "tiny", "base", "small", "medium", "large")。
                           デフォルトは "base"。
    """
    # ffmpegがインストールされているか確認 (Whisperが必要とするため)
    try:
        # 単純なバージョンチェックコマンドを実行してみる
        import subprocess
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except FileNotFoundError:
        print("エラー: ffmpegがインストールされていないか、パスが通っていません。", file=sys.stderr)
        print("Whisperはffmpegが必要です。インストールしてください。", file=sys.stderr)
        print("インストール方法 (例):", file=sys.stderr)
        print("  - macOS (Homebrew): brew install ffmpeg", file=sys.stderr)
        print("  - Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError:
        # ffmpeg自体はあるが、実行時にエラーが発生した場合など (通常は考えにくい)
        print("エラー: ffmpegの実行中に問題が発生しました。", file=sys.stderr)
        sys.exit(1)


    print(f"Whisperモデル '{model_size}' をロードしています...")
    try:
        model = whisper.load_model(model_size)
    except Exception as e:
        print(f"モデルのロード中にエラーが発生しました: {e}", file=sys.stderr)
        print("指定されたモデルサイズが有効か、またはモデルファイルが正しくダウンロードされているか確認してください。", file=sys.stderr)
        sys.exit(1)

    print(f"音声ファイル '{input_file}' の文字起こしを開始します...")
    try:
        result = model.transcribe(input_file, verbose=True) # verbose=Trueで進捗を表示
    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{input_file}' が見つかりません。", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"文字起こし中にエラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)

    print("文字起こしが完了しました。")

    # 出力ファイルに結果を書き込み
    if output_file:
        output_path = output_file
    else:
        # textディレクトリに同じファイル名で保存
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_dir = "text"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{base_name}.txt")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        print(f"結果を '{output_path}' に保存しました。")
    except IOError as e:
        print(f"エラー: 出力ファイル '{output_path}' への書き込みに失敗しました: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Whisperを使用して音声ファイルを文字起こしするスクリプト")
    parser.add_argument("input_file", help="入力音声ファイルへのパス (例: audio.m4a)")
    parser.add_argument("-o", "--output", help="出力テキストファイルへのパス (指定しない場合は入力ファイル名+.txt)")
    parser.add_argument("-m", "--model", default="base",
                        choices=["tiny", "base", "small", "medium", "large", "large-v1", "large-v2", "large-v3"],
                        help="使用するWhisperモデルのサイズ (デフォルト: base)")

    args = parser.parse_args()

    transcribe_audio(args.input_file, args.output, args.model) 