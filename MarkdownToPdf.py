#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MarkdownからPDFへの変換ツール（日本語完全対応版）

Pandocを使用してMarkdownファイルをPDFに変換します。
日本語フォント（Noto CJK）による美しいPDF生成に対応。

必要な環境:
- pandoc: https://pandoc.org/installing.html
- TeXディストリビューション（TeX Live, MiKTeXなど）
- 日本語フォント: fonts-noto-cjk, fonts-ipafont

使用例:
    python3 MarkdownToPdf.py input.md output.pdf
    python3 MarkdownToPdf.py --demo
    python3 MarkdownToPdf.py --help

Author: s-taku0502
License: MIT License
Version: 2.0.0
Date: 2025-07-27
"""

import subprocess
import os
import sys
import argparse
import tempfile
from pathlib import Path


def check_pandoc():
    """pandocがインストールされているかチェック"""
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✓ {version}")
            return True
        else:
            return False
    except FileNotFoundError:
        print("✗ pandocが見つかりません")
        print("インストール方法: https://pandoc.org/installing.html")
        return False


def check_xelatex():
    """XeLaTeXがインストールされているかチェック"""
    try:
        result = subprocess.run(['xelatex', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ XeLaTeX が利用可能")
            return True
        else:
            return False
    except FileNotFoundError:
        print("✗ XeLaTeXが見つかりません")
        print("インストール方法: sudo apt install texlive-xetex")
        return False


def check_japanese_fonts():
    """日本語フォントがインストールされているかチェック"""
    try:
        result = subprocess.run(['fc-list', ':lang=ja'], 
                              capture_output=True, text=True)
        if result.returncode == 0 and result.stdout:
            # Noto CJKフォントがあるかチェック
            if 'Noto' in result.stdout:
                print("✓ 日本語フォント (Noto CJK) が利用可能")
                return 'noto'
            elif 'IPA' in result.stdout:
                print("✓ 日本語フォント (IPA) が利用可能")
                return 'ipa'
            else:
                print("⚠️  日本語フォントが検出されましたが最適ではありません")
                return 'basic'
        else:
            print("✗ 日本語フォントが見つかりません")
            return None
    except FileNotFoundError:
        print("✗ fontconfigが見つかりません")
        return None


def get_font_options(font_type=None):
    """フォントタイプに応じたpandocオプションを返す"""
    if font_type == 'noto':
        return [
            '--variable=CJKmainfont=Noto Serif CJK JP',
            '--variable=CJKsansfont=Noto Sans CJK JP',
            '--variable=CJKmonofont=Noto Sans Mono CJK JP'
        ]
    elif font_type == 'ipa':
        return [
            '--variable=CJKmainfont=IPAexMincho',
            '--variable=CJKsansfont=IPAexGothic',
            '--variable=CJKmonofont=IPAGothic'
        ]
    else:
        # フォールバック設定
        return [
            '--variable=CJKmainfont=DejaVu Serif',
            '--variable=CJKsansfont=DejaVu Sans'
        ]


def convert_markdown_to_pdf(input_file, output_file, engine='xelatex', options=None, font_type=None):
    """MarkdownをPDFに変換（日本語フォント対応）"""
    if not os.path.exists(input_file):
        print(f"✗ 入力ファイルが見つかりません: {input_file}")
        return False

    # 出力ディレクトリを作成
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"✓ 出力ディレクトリを作成: {output_dir}")

    try:
        # 基本的なpandocコマンド
        command = [
            'pandoc',
            input_file,
            '-o', output_file,
            f'--pdf-engine={engine}',
            '--from=markdown',
            '--to=pdf'
        ]
        
        # 基本的なレイアウトオプション
        layout_options = [
            '--variable=geometry:margin=2cm',
            '--variable=fontsize=12pt',
            '--variable=papersize=a4',
            '--variable=documentclass=article'
        ]
        command.extend(layout_options)
        
        # 日本語フォントオプション
        font_options = get_font_options(font_type)
        command.extend(font_options)
        
        # 追加オプションがある場合は追加
        if options:
            command.extend(options)
        
        print(f"実行中: {' '.join(command)}")
        
        # pandocを実行
        result = subprocess.run(
            command, 
            check=True, 
            capture_output=True, 
            text=True, 
            encoding='utf-8'
        )
        
        print(f"✓ 変換完了: {output_file}")
        return True

    except FileNotFoundError as e:
        print(f"✗ コマンドが見つかりません: {e}")
        return False
    except subprocess.CalledProcessError as e:
        print(f"✗ 変換エラー (終了コード: {e.returncode})")
        if e.stdout:
            print(f"標準出力: {e.stdout}")
        if e.stderr:
            print(f"標準エラー: {e.stderr}")
        
        # 一般的なエラーの対処法を提示
        if "font" in e.stderr.lower() or "cjk" in e.stderr.lower():
            print("\n💡 日本語フォントエラーの可能性があります:")
            print("   sudo apt install fonts-noto-cjk fonts-ipafont")
            print("   fc-cache -fv")
        
        return False
    except Exception as e:
        print(f"✗ 予期せぬエラー: {e}")
        return False


def create_sample_markdown(output_path):
    """日本語対応のサンプルMarkdownファイルを作成"""
    content = """# 日本語MarkdownからPDF変換のデモ

これは**pandoc**と**XeLaTeX**を使った日本語MarkdownからPDFへの変換デモです。

## 🌟 主な特徴

このツールは以下の機能を提供します：

* ✅ **完全な日本語対応** - Noto CJKフォントによる美しい表示
* ✅ **豊富なフォーマット** - 表、リスト、コードブロック、数式
* ✅ **簡単操作** - コマンドライン一つで即座に変換
* ✅ **カスタマイズ可能** - PDFエンジンやオプションを柔軟に設定

## 📝 テキスト装飾

- **太字テキスト**
- *イタリックテキスト*
- ~~取り消し線~~
- `インラインコード`

## 📊 データ表

| 項目 | 説明 | 対応状況 |
|------|------|----------|
| 日本語表示 | 漢字・ひらがな・カタカナ | ✅ 完全対応 |
| 英数字 | ASCII文字 | ✅ 完全対応 |
| 記号 | 特殊文字・絵文字 | ✅ 対応 |
| 数式 | LaTeX記法 | ✅ 対応 |

## 💻 サンプルコード

```python
def convert_to_pdf(markdown_file, pdf_file):
    \"\"\"
    MarkdownファイルをPDFに変換する関数
    
    Args:
        markdown_file (str): 入力Markdownファイルパス
        pdf_file (str): 出力PDFファイルパス
    
    Returns:
        bool: 変換成功時True
    \"\"\"
    import subprocess
    
    # pandocコマンドを実行
    cmd = [
        'pandoc', markdown_file, 
        '-o', pdf_file,
        '--pdf-engine=xelatex',
        '--variable=CJKmainfont=Noto Serif CJK JP'
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ 変換成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ 変換失敗")
        return False

# 使用例
success = convert_to_pdf("入力.md", "出力.pdf")
```

## 🧮 数学記法

### インライン数式
エネルギーと質量の関係式: $E = mc^2$

### ブロック数式
総和の公式:
$$\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}$$

二次方程式の解の公式:
$$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$

## 📋 リスト例

### 順序なしリスト
- 第一項目
  - サブ項目1
  - サブ項目2
    - さらにネストした項目
- 第二項目
- 第三項目

### 順序付きリスト
1. **準備**: 依存関係をインストール
2. **実行**: コマンドラインから変換
3. **確認**: 生成されたPDFをチェック

## 💬 引用文

> 「コンピュータは非常に高速で正確で愚かである。
> 人間は非常に低速で不正確で賢明である。
> この組み合わせは、想像を絶する力を生み出す。」
> 
> — アルベルト・アインシュタイン

## 🎌 日本語文字の表示テスト

### ひらがな
あいうえお かきくけこ さしすせそ たちつてと なにぬねの
はひふへほ まみむめも やゆよ らりるれろ わをん

### カタカナ  
アイウエオ カキクケコ サシスセソ タチツテト ナニヌネノ
ハヒフヘホ マミムメモ ヤユヨ ラリルレロ ワヲン

### 漢字
一二三四五六七八九十 百千万億兆
春夏秋冬 東西南北 上下左右
山川海空 花鳥風月 雲雨雪霧

---

**🔧 技術情報**

- 作成日: 2025年7月27日
- ツール: MarkdownToPdf変換ツール v2.0
- エンジン: Pandoc + XeLaTeX
- フォント: Noto CJK (日本語完全対応)
- 文字エンコーディング: UTF-8

📄 このファイルは日本語MarkdownからPDFへの変換機能をテストするために生成されました。
"""
    
    # 出力ディレクトリを作成
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # ファイルを作成
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✓ 日本語サンプルファイルを作成: {output_path}")
    return output_path


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description='MarkdownファイルをPDFに変換します（日本語完全対応）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  %(prog)s sample.md sample.pdf              # 基本的な変換
  %(prog)s input.md output.pdf --engine pdflatex   # PDFエンジンを指定
  %(prog)s --demo                            # デモ実行
  %(prog)s --check                           # 依存関係チェック

サポートするPDFエンジン:
  - xelatex (デフォルト、日本語推奨)
  - pdflatex
  - lualatex

日本語フォント:
  - Noto CJK (推奨): sudo apt install fonts-noto-cjk
  - IPAフォント: sudo apt install fonts-ipafont

依存関係:
  - pandoc: https://pandoc.org/installing.html
  - TeX Live: sudo apt install texlive-xetex texlive-fonts-recommended
        """
    )
    
    # 位置引数
    parser.add_argument('input_file', nargs='?', 
                       help='入力Markdownファイル')
    parser.add_argument('output_file', nargs='?', 
                       help='出力PDFファイル')
    
    # オプション引数
    parser.add_argument('--engine', default='xelatex',
                       choices=['xelatex', 'pdflatex', 'lualatex'],
                       help='PDFエンジンを指定 (デフォルト: xelatex)')
    parser.add_argument('--demo', action='store_true',
                       help='デモ用サンプルファイルを作成して変換')
    parser.add_argument('--check', action='store_true',
                       help='依存関係をチェック')
    parser.add_argument('--options', nargs='*',
                       help='pandocに渡す追加オプション')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='詳細出力を有効にする')
    
    args = parser.parse_args()
    
    # バナー表示
    if args.verbose or args.demo or args.check:
        print("=" * 60)
        print("  Markdown to PDF 変換ツール (日本語完全対応版)")
        print("=" * 60)
    
    # 依存関係チェック
    if args.check:
        print("\n📋 依存関係チェック:")
        pandoc_ok = check_pandoc()
        xelatex_ok = check_xelatex()
        font_type = check_japanese_fonts()
        
        if pandoc_ok and xelatex_ok and font_type:
            print("\n✅ すべての依存関係が満たされています")
            if font_type == 'noto':
                print("🎌 Noto CJKフォントで最高品質の日本語PDFを生成できます")
            elif font_type == 'ipa':
                print("🎌 IPAフォントで高品質の日本語PDFを生成できます")
            else:
                print("⚠️  基本的な日本語表示は可能ですが、フォント追加を推奨します")
            return 0
        else:
            print("\n❌ 依存関係が不足しています")
            return 1
    
    # 日本語フォントチェック（デモや変換時）
    font_type = check_japanese_fonts() if not args.check else 'noto'
    
    # デモモード
    if args.demo:
        print("\n🚀 デモモード開始:")
        
        # 依存関係の簡易チェック
        if not check_pandoc():
            return 1
            
        # サンプルファイル作成
        output_dir = "output"
        sample_md = os.path.join(output_dir, "japanese_demo.md")
        sample_pdf = os.path.join(output_dir, "japanese_demo.pdf")
        
        create_sample_markdown(sample_md)
        
        # PDF変換
        print(f"\n📄 PDF変換実行 (フォントタイプ: {font_type or 'デフォルト'}):")
        if convert_markdown_to_pdf(sample_md, sample_pdf, args.engine, args.options, font_type):
            file_size = os.path.getsize(sample_pdf)
            print(f"\n🎉 デモ完了!")
            print(f"  📁 入力ファイル: {sample_md}")
            print(f"  📁 出力ファイル: {sample_pdf}")
            print(f"  📊 ファイルサイズ: {file_size:,} bytes")
            print(f"  🎌 日本語フォント: {font_type or 'デフォルト'}")
            return 0
        else:
            print("\n💥 デモに失敗しました")
            return 1
    
    # 通常の変換モード
    if not args.input_file or not args.output_file:
        parser.print_help()
        print(f"\n💡 ヒント: --demo オプションで日本語対応デモを実行できます")
        return 1
    
    # 入力ファイルの存在確認
    if not os.path.exists(args.input_file):
        print(f"❌ 入力ファイルが見つかりません: {args.input_file}")
        return 1
    
    # 簡易依存関係チェック
    if not check_pandoc():
        return 1
    
    # PDF変換実行
    print(f"\n📄 変換開始: {args.input_file} → {args.output_file}")
    if convert_markdown_to_pdf(args.input_file, args.output_file, args.engine, args.options, font_type):
        file_size = os.path.getsize(args.output_file)
        print(f"\n✅ 変換完了!")
        print(f"  📁 出力ファイル: {args.output_file}")
        print(f"  📊 ファイルサイズ: {file_size:,} bytes")
        print(f"  🎌 日本語フォント: {font_type or 'デフォルト'}")
        return 0
    else:
        print(f"\n❌ 変換に失敗しました")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  処理が中断されました")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 予期せぬエラー: {e}")
        sys.exit(1)
