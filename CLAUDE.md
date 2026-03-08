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
- **クラス名**: PascalCase、`Scene` を継承（例: `LimitsScene`）
- **関数名**: snake_case
- **インデント**: スペース4つ
- **文字コード**: UTF-8

## シーンファイルのひな形
```python
from manim import *

class TopicScene(Scene):
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

## よくある問題と対処
- **LaTeX エラー**: 数式には `MathTex` を使い、通常テキストには `Text` を使う
- **フォント問題**: カスタムフォントは `assets/fonts/` に配置し、`Text(font="フォント名")` で指定
- **出力先**: `media/` フォルダに自動保存される（`manim.cfg` で設定済み）
