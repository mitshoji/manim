# Manim 数学アニメーションプロジェクト

## プロジェクト概要
ManimCE を使って数学の概念を視覚的に説明するアニメーション動画を制作するプロジェクト。
1本の動画につき1つの仕様書（`specs/` フォルダ内）と1つのシーンファイル（`src/scenes/` フォルダ内）を対応させる。

## 技術スタック
- Python 3.10+
- ManimCE（最新安定版）
- NumPy

## フォルダ構成
```
project/
├── CLAUDE.md              # このファイル（プロジェクト共通ルール）
├── manim.cfg              # Manim 設定
├── README.md
├── src/
│   ├── scenes/            # シーンファイル（動画1本 = .pyファイル1つ）
│   └── utils/             # 共通ヘルパー関数・カスタムクラス
├── specs/                 # 仕様書（001_topic.md 形式）
├── assets/
│   ├── images/
│   ├── audio/
│   └── fonts/
├── media/                 # Manim 出力先（自動生成）
└── docs/                  # 制作メモ・変更ログ
```

## コーディング規約
- **ファイル名**: `001_topic_name.py`（specs と番号を合わせる）
- **クラス名**: PascalCase、`ReelScene` を継承（例: `LimitsScene`）
- **関数名**: snake_case
- **インデント**: スペース4つ
- **文字コード**: UTF-8

## 出力フォーマット
- **対象**: Instagram リール（縦型 9:16、1080×1920px）
- **基底クラス**: すべてのシーンは `Scene` ではなく **`ReelScene`** を継承すること
- **`ReelScene` の定義**: `src/utils/reel_scene.py`（フレームサイズ・解像度を一括管理）
- 横型動画を作る場合のみ例外的に `Scene` を継承する

## シーンファイルのひな形
```python
from manim import *
import numpy as np
from src.utils.reel_scene import ReelScene

class TopicScene(ReelScene):
    def construct(self):
        # ここにアニメーションを記述
        pass
```

## Manim 実行コマンド
```bash
# 低品質プレビュー（高速）
manim -ql src/scenes/<file>.py <SceneName>

# 中品質
manim -qm src/scenes/<file>.py <SceneName>

# 高品質（最終出力）
manim -qh src/scenes/<file>.py <SceneName>

# レンダリング後に自動再生
manim -ql --preview src/scenes/<file>.py <SceneName>
```

## 仕様書（specs）の読み方
- `specs/` フォルダ内の `.md` ファイルが各動画の仕様書
- ファイル名の番号が `src/scenes/` の対応ファイルと一致する
- 実装前に仕様書を必ず読み、シーン構成・出力ファイル名・クラス名を確認すること

## 作業ディレクトリ
- **常に `C:/manim` で作業すること**（GitHub と連携しているメインリポジトリ）
- git worktree は使用しない。`C:/manim/.claude/worktrees/` 以下にファイルを作らないこと

## よくある問題と対処
- **LaTeX エラー**: 数式には `MathTex` を使い、通常テキストには `Text` を使う
- **フォント問題**: カスタムフォントは `assets/fonts/` に配置し、`Text(font="フォント名")` で指定
- **出力先**: `media/` フォルダに自動保存される（`manim.cfg` で設定済み）
