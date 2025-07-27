# MarkdownToPdf変換ツール

PandocとXeLaTeXを使用してMarkdownファイルをPDFに変換するPythonツールです。

## 特徴

✅ **日本語完全対応** - XeLaTeXエンジンによる美しい日本語PDF生成  
✅ **豊富なフォーマット** - 表、リスト、コードブロック、数式をサポート  
✅ **簡単操作** - コマンドライン一つで即座に変換  
✅ **カスタマイズ可能** - PDFエンジンやオプションを柔軟に設定  
✅ **デモ機能** - サンプルファイル自動生成でお試し可能  

## インストール

### 1. 依存関係のインストール

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y pandoc texlive-xetex texlive-fonts-recommended texlive-fonts-extra

# macOS (Homebrew)
brew install pandoc
brew install --cask mactex

# Windows
# 1. https://pandoc.org/installing.html からpandocをインストール
# 2. https://miktex.org/ からMiKTeXをインストール
```

### 2. Pythonツールの準備

```bash
# ファイルを実行可能にする
chmod +x MarkdownToPdf.py
```

## 使用方法

### 基本構文

```bash
python3 MarkdownToPdf.py [入力ファイル.md] [出力ファイル.pdf]
```

### 基本的な変換

```bash
python3 MarkdownToPdf.py input.md output.pdf
```

### デモ実行（お試し）

```bash
python3 MarkdownToPdf.py --demo
```

### 依存関係チェック

```bash
python3 MarkdownToPdf.py --check
```

## 実行時のコード例

### 1. 簡単な文書変換

```bash
# README.mdをPDFに変換
python3 MarkdownToPdf.py README.md README.pdf

# 技術文書の変換
python3 MarkdownToPdf.py documentation.md documentation.pdf

# 日本語文書の変換
python3 MarkdownToPdf.py 仕様書.md 仕様書.pdf
```

### 2. 出力ディレクトリを指定

```bash
# outputフォルダに保存
python3 MarkdownToPdf.py report.md output/report.pdf

# 日付付きファイル名で保存
python3 MarkdownToPdf.py meeting.md output/meeting_2025-07-27.pdf
```

### 3. 複数ファイルの一括変換

```bash
# 複数ファイルを個別に変換
python3 MarkdownToPdf.py chapter1.md output/chapter1.pdf
python3 MarkdownToPdf.py chapter2.md output/chapter2.pdf
python3 MarkdownToPdf.py chapter3.md output/chapter3.pdf
```

### 4. 詳細オプション付きの変換

```bash
# PDFエンジンを指定
python3 MarkdownToPdf.py input.md output.pdf --engine pdflatex

# 追加のpandocオプション付き
python3 MarkdownToPdf.py input.md output.pdf --options "--toc" "--number-sections"

# 詳細出力モード
python3 MarkdownToPdf.py input.md output.pdf --verbose
```

### 5. 実際の作業例

```bash
# 1. 現在のディレクトリ構造確認
ls -la

# 2. デモ実行でツールをテスト
python3 MarkdownToPdf.py --demo

# 3. 実際のMarkdownファイルを変換
python3 MarkdownToPdf.py my_document.md my_document.pdf

# 4. 変換結果確認
ls -la *.pdf
```

## サポートする機能

### Markdownフォーマット

- **テキスト装飾**: 太字、イタリック、取り消し線、下線
- **見出し**: H1～H6レベル対応
- **リスト**: 順序付き・順序なしリスト、ネスト対応
- **表**: 複雑な表構造もサポート
- **リンク**: URL・内部リンク
- **画像**: 各種画像形式対応
- **コードブロック**: シンタックスハイライト付き
- **引用**: ブロック引用文
- **水平線**: セクション区切り

### 数学記法

```markdown
インライン数式: $E = mc^2$

ブロック数式:
$$\sum_{i=1}^{n} x_i = \frac{n(n+1)}{2}$$
```

### 日本語対応

- UTF-8エンコーディング完全対応
- 日本語フォント自動選択
- 適切な行間・文字間隔
- 縦書き対応（オプション設定により）

## コマンドオプション

| オプション | 説明 | デフォルト |
|------------|------|------------|
| `--engine` | PDFエンジン指定 | `xelatex` |
| `--demo` | デモ実行 | - |
| `--check` | 依存関係チェック | - |
| `--options` | 追加pandocオプション | - |
| `--verbose` | 詳細出力 | - |

### PDFエンジン

- **xelatex** (推奨): 日本語対応、Unicodeサポート
- **pdflatex**: 標準エンジン、高速
- **lualatex**: Lua拡張、柔軟性が高い

## トラブルシューティング

### よくある問題

**Q: 「pandoc: command not found」エラーが出る**
```bash
# pandocをインストール
sudo apt install pandoc  # Ubuntu/Debian
brew install pandoc      # macOS
```

**Q: 「xelatex: command not found」エラーが出る**
```bash
# XeLaTeXをインストール
sudo apt install texlive-xetex  # Ubuntu/Debian
```

**Q: 日本語フォントが表示されない**
```bash
# 日本語フォントパッケージをインストール
sudo apt install texlive-fonts-extra fonts-noto-cjk
```

**Q: 数式が表示されない**
```bash
# 数式パッケージをインストール
sudo apt install texlive-latex-extra
```

### 依存関係確認

```bash
# 依存関係の確認
python3 MarkdownToPdf.py --check

# pandocのバージョン確認
pandoc --version

# XeLaTeXの確認
xelatex --version
```

## 出力例

### 生成されるファイル

- **入力**: `document.md` (Markdownファイル)
- **出力**: `document.pdf` (PDFファイル)
- **設定**: A4サイズ、2cm余白、12ptフォント

### デモ出力

```bash
$ python3 MarkdownToPdf.py --demo

==================================================
  Markdown to PDF 変換ツール
==================================================

🚀 デモモード開始:
✓ pandoc 2.9.2.1
✓ サンプルファイルを作成: output/demo.md

📄 PDF変換実行:
✓ 変換完了: output/demo.pdf

🎉 デモ完了!
  📁 入力ファイル: output/demo.md
  📁 出力ファイル: output/demo.pdf
  📊 ファイルサイズ: 22,621 bytes
```

## ライセンス

このプロジェクトは [MIT ライセンス](LICENSE) の下で公開されています。

```
MIT License

Copyright (c) 2025 MarkdownToPdf Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 利用について

- ✅ **商用利用可**: 商業プロジェクトでも自由に利用できます
- ✅ **改変可**: ソースコードを自由に改変できます
- ✅ **再配布可**: 改変版も含めて自由に配布できます
- ✅ **プライベート利用可**: 個人・組織内での利用に制限はありません
- ⚠️ **著作権表示必要**: 配布時は著作権表示とライセンス全文の記載が必要です
- ⚠️ **保証なし**: ソフトウェアの品質や動作に関する保証はありません

## 作成者

- 作成日: 2025年7月27日
- バージョン: 1.0.0
- エンジン: Python 3.x + Pandoc + XeLaTeX

---

📄 **お困りの際は `--help` オプションでヘルプを表示できます**
