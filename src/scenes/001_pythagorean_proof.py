from manim import *
import numpy as np
from src.utils.reel_scene import ReelScene # ReelFrame

# ── カラーパレット（3Blue1Brown 風ダークテーマ） ──────────────
BG_COLOR = "#0f0f1e"
COLOR_A  = "#58c4dd"   # シアン青（辺 a）
COLOR_B  = "#83c167"   # 緑      （辺 b）
COLOR_C  = "#e07a5f"   # 赤橙    （斜辺 c）


class PythagoreanProof(ReelScene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── 薄いグリッド背景（不透明度 4%）─────────────────────
        grid = NumberPlane(
            background_line_style={
                "stroke_color": WHITE,
                "stroke_opacity": 0.04,
            },
            axis_config={"stroke_opacity": 0},
        )
        self.add(grid)

        # ═══════════════════════════════════════════════════════
        # フェーズ1：直角三角形の登場
        # ═══════════════════════════════════════════════════════

        # 辺の比 a:b = 105:72（÷40 でスクリーン座標に変換）
        a_len = 105 / 50   # 2.625
        b_len =  72 / 50   # 1.800

        # 頂点を原点基準で定義
        #   A = 直角頂点（左下）
        #   B = 右下  （a の対辺側）
        #   C = 左上  （b の対辺側）
        A0 = np.array([0.0,    0.0,   0.0])
        B0 = np.array([b_len,  0.0,   0.0])
        C0 = np.array([0.0,    a_len, 0.0])

        # 三角形の重心を「画面中央やや下（DOWN*0.5）」に合わせる
        centroid0 = (A0 + B0 + C0) / 3
        offset = np.array([0.0, +3.0, 0.0]) - centroid0
        A, B, C = A0 + offset, B0 + offset, C0 + offset

        # ── 三角形本体 ────────────────────────────────────────
        tri = Polygon(
            A, B, C,
            fill_color=WHITE, fill_opacity=0.08,
            stroke_color=WHITE, stroke_width=0,
        )

        # 辺ごとに色付け
        side_b = Line(A, B, color=COLOR_B, stroke_width=4)   # 下辺 b（緑）
        side_a = Line(A, C, color=COLOR_A, stroke_width=4)   # 左辺 a（青）
        side_c = Line(B, C, color=COLOR_C, stroke_width=4)   # 斜辺 c（赤橙）

        # 直角マーク（□）
        right_mark = RightAngle(
            side_b, side_a,
            length=0.22,
            color=WHITE,
            stroke_width=2,
        )

        # ── 辺ラベル ──────────────────────────────────────────
        label_a = MathTex("a", color=COLOR_A, font_size=42)
        label_b = MathTex("b", color=COLOR_B, font_size=42)
        label_c = MathTex("c", color=COLOR_C, font_size=42)

        # a ラベル：左辺の中点から左へ
        label_a.move_to((A + C) / 2 + LEFT * 0.38)

        # b ラベル：下辺の中点から下へ
        label_b.move_to((A + B) / 2 + DOWN * 0.38)

        # c ラベル：斜辺の外側（外向き法線方向）へ
        bc_vec  = C - B
        bc_norm = np.array([bc_vec[1], -bc_vec[0], 0.0])
        bc_norm /= np.linalg.norm(bc_norm)
        label_c.move_to((B + C) / 2 + bc_norm * 0.40)

        # ── アニメーション ────────────────────────────────────

        # 三角形をフェードイン
        self.play(FadeIn(tri), run_time=0.8)

        # 辺・直角マークを順番に描画（smooth = ease-in-out）
        self.play(
            Create(side_b),
            Create(side_a),
            Create(side_c),
            Create(right_mark),
            run_time=1.5,
            lag_ratio=0.2,
            rate_func=smooth,
        )
        self.wait(0.3)

        # ラベルを少し遅らせてフェードイン
        self.play(
            FadeIn(label_a, shift=LEFT    * 0.1),
            FadeIn(label_b, shift=DOWN    * 0.1),
            FadeIn(label_c, shift=bc_norm * 0.1),
            run_time=1.0,
            lag_ratio=0.25,
        )
        self.wait(1.5)

        # ═══════════════════════════════════════════════════════
        # フェーズ2：4つの三角形を配置する
        # ═══════════════════════════════════════════════════════

        # ── ラベルをフェードアウト ────────────────────────────
        self.play(
            FadeOut(label_a),
            FadeOut(label_b),
            FadeOut(label_c),
            run_time=0.6,
        )

        # 個別オブジェクトをVGroupにまとめて管理しやすくする
        self.remove(tri, side_b, side_a, side_c, right_mark)
        orig_group = VGroup(tri, side_b, side_a, side_c, right_mark)
        self.add(orig_group)

        s = a_len + b_len  # 外側正方形の辺長 (a + b)

        # ── 外側 (a+b)² 正方形の4隅（原点中心）──────────────
        sq_TL = np.array([-s / 2,  s / 2, 0.0])
        sq_TR = np.array([ s / 2,  s / 2, 0.0])
        sq_BR = np.array([ s / 2, -s / 2, 0.0])
        sq_BL = np.array([-s / 2, -s / 2, 0.0])

        # ── 内側 c² 正方形の4頂点（各辺を a:b で分割した点）──
        #   P1: 上辺、TL から a 右
        #   P2: 右辺、TR から a 下
        #   P3: 下辺、BR から a 左
        #   P4: 左辺、BL から a 上
        P1 = sq_TL + np.array([ a_len,    0,  0.0])
        P2 = sq_TR + np.array([    0, -a_len, 0.0])
        P3 = sq_BR + np.array([-a_len,    0,  0.0])
        P4 = sq_BL + np.array([    0,  a_len, 0.0])

        # ── 直角三角形VGroup生成ヘルパー ──────────────────────
        def make_tri(ra_v, leg_b_end, leg_a_end):
            """直角三角形VGroupを生成（多角形＋色付き辺＋直角マーク）。
            submobjectの順序は orig_group と合わせる:
              [0] polygon, [1] lb(緑), [2] la(青), [3] lc(赤橙), [4] 直角マーク
            """
            poly  = Polygon(
                ra_v, leg_b_end, leg_a_end,
                fill_color=WHITE, fill_opacity=0.08, stroke_width=0,
            )
            lb    = Line(ra_v, leg_b_end, color=COLOR_B, stroke_width=4)
            la    = Line(ra_v, leg_a_end, color=COLOR_A, stroke_width=4)
            lc    = Line(leg_b_end, leg_a_end, color=COLOR_C, stroke_width=4)
            ra_mk = RightAngle(lb, la, length=0.22, color=WHITE, stroke_width=2)
            return VGroup(poly, lb, la, lc, ra_mk)

        # ── 各コーナーの目標三角形を定義 ──────────────────────
        #   TL: 直角=sq_TL, b→P4(下),  a→P1(右)  ← 時計回り90°
        #   TR: 直角=sq_TR, b→P1(左),  a→P2(下)  ← 180°
        #   BR: 直角=sq_BR, b→P2(上),  a→P3(左)  ← 反時計回り90°
        #   BL: 直角=sq_BL, b→P3(右),  a→P4(上)  ← 元の三角形（0°）
        target_TL = make_tri(sq_TL, P4, P1)
        target_TR = make_tri(sq_TR, P1, P2)
        target_BR = make_tri(sq_BR, P2, P3)
        target_BL = make_tri(sq_BL, P3, P4)

        # 3枚のコピーを元の位置で生成してシーンに追加
        copy_TR = orig_group.copy()
        copy_BR = orig_group.copy()
        copy_BL = orig_group.copy()
        self.add(copy_TR, copy_BR, copy_BL)

        # ── アニメーション：1枚ずつ各コーナーへ ──────────────

        # 元の三角形 → 左上コーナー
        self.play(
            Transform(orig_group, target_TL),
            run_time=1.2, rate_func=smooth,
        )
        self.wait(0.3)

        # コピー1 → 右上コーナー
        self.play(
            Transform(copy_TR, target_TR),
            run_time=1.2, rate_func=smooth,
        )
        self.wait(0.3)

        # コピー2 → 右下コーナー
        self.play(
            Transform(copy_BR, target_BR),
            run_time=1.2, rate_func=smooth,
        )
        self.wait(0.3)

        # コピー3 → 左下コーナー
        self.play(
            Transform(copy_BL, target_BL),
            run_time=1.2, rate_func=smooth,
        )
        self.wait(0.5)

        # ── 内側の c² 正方形（赤橙の枠）を自然に表示 ──────────
        inner_sq = Polygon(
            P1, P2, P3, P4,
            stroke_color=COLOR_C,
            stroke_width=3,
            fill_opacity=0,
        )
        self.play(Create(inner_sq), run_time=1.0, rate_func=smooth)
        self.wait(1.5)

        # ═══════════════════════════════════════════════════════
        # フェーズ3：外側の正方形を認識させる
        # ═══════════════════════════════════════════════════════

        # ── 外側 (a+b)² 正方形：黄色の枠線でハイライト ──────────
        outer_sq = Polygon(
            sq_TL, sq_TR, sq_BR, sq_BL,
            stroke_color=YELLOW,
            stroke_width=4,
            fill_opacity=0,
        )

        # フラッシュ演出：描画 → Indicate で一瞬強調
        self.play(Create(outer_sq), run_time=0.8, rate_func=smooth)
        self.play(Indicate(outer_sq, color=YELLOW, scale_factor=1.02), run_time=0.7)
        self.wait(0.3)

        # ── 上辺の分割：TL→P1 = a（青）、P1→TR = b（緑）──────────
        # P1 の位置に目盛り（縦の短い線）
        tick_top = Line(
            P1 + UP   * 0.18,
            P1 + DOWN * 0.18,
            color=WHITE,
            stroke_width=2,
        )

        # 左区間（TL → P1）= a のブレースとラベル
        brace_top_a = BraceBetweenPoints(sq_TL, P1, UP)
        brace_top_a.set_color(COLOR_A)
        label_top_a = MathTex("a", color=COLOR_A, font_size=36)
        label_top_a.next_to(brace_top_a, UP, buff=0.12)

        # 右区間（P1 → TR）= b のブレースとラベル
        brace_top_b = BraceBetweenPoints(P1, sq_TR, UP)
        brace_top_b.set_color(COLOR_B)
        label_top_b = MathTex("b", color=COLOR_B, font_size=36)
        label_top_b.next_to(brace_top_b, UP, buff=0.12)

        # ── 右辺の分割：TR→P2 = a（青）、P2→BR = b（緑）──────────
        # P2 の位置に目盛り（横の短い線）
        tick_right = Line(
            P2 + LEFT  * 0.18,
            P2 + RIGHT * 0.18,
            color=WHITE,
            stroke_width=2,
        )

        # 上区間（TR → P2）= a のブレースとラベル
        brace_right_a = BraceBetweenPoints(sq_TR, P2, RIGHT)
        brace_right_a.set_color(COLOR_A)
        label_right_a = MathTex("a", color=COLOR_A, font_size=36)
        label_right_a.next_to(brace_right_a, RIGHT, buff=0.12)

        # 下区間（P2 → BR）= b のブレースとラベル
        brace_right_b = BraceBetweenPoints(P2, sq_BR, RIGHT)
        brace_right_b.set_color(COLOR_B)
        label_right_b = MathTex("b", color=COLOR_B, font_size=36)
        label_right_b.next_to(brace_right_b, RIGHT, buff=0.12)

        # ── アニメーション：目盛り → 上辺ブレース → 右辺ブレース ──
        self.play(
            Create(tick_top),
            Create(tick_right),
            run_time=0.5,
        )

        # 上辺：a → b の順でブレース＆ラベルを表示
        self.play(
            Create(brace_top_a),
            FadeIn(label_top_a, shift=UP * 0.1),
            run_time=0.8, rate_func=smooth,
        )
        self.play(
            Create(brace_top_b),
            FadeIn(label_top_b, shift=UP * 0.1),
            run_time=0.8, rate_func=smooth,
        )

        # 右辺：a → b の順でブレース＆ラベルを表示
        self.play(
            Create(brace_right_a),
            FadeIn(label_right_a, shift=RIGHT * 0.1),
            run_time=0.8, rate_func=smooth,
        )
        self.play(
            Create(brace_right_b),
            FadeIn(label_right_b, shift=RIGHT * 0.1),
            run_time=0.8, rate_func=smooth,
        )

        self.wait(1.5)

        # ═══════════════════════════════════════════════════════
        # フェーズ4：(a+b)² の式が登場
        # ═══════════════════════════════════════════════════════

        # 数式エリア（画面下部）の Y 座標
        # ※ 外側正方形の下端 y = -s/2 ≈ -2.21 のさらに下
        # ※ フェーズ6の行2（EQ_Y2）が見切れないよう -2.9 に設定
        EQ_Y = -5.0

        # ── 外側正方形の中央に (a+b)² をフェードイン ────────────
        eq_ab2 = MathTex("(a+b)^2", font_size=48, color=YELLOW)
        eq_ab2.move_to(ORIGIN)  # 外側正方形の中央 = 原点

        self.play(FadeIn(eq_ab2, scale=1.2), run_time=0.8)
        self.wait(0.5)

        # ── (a+b)² を画面下部・行1の左端へスライド ──────────────
        eq_ab2.generate_target()
        eq_ab2.target.to_edge(LEFT, buff=0.4)   # 左端に寄せる
        eq_ab2.target.set_y(EQ_Y)               # Y 座標を数式エリアに合わせる

        self.play(MoveToTarget(eq_ab2), run_time=1.2, rate_func=smooth)
        self.wait(0.3)

        # ── = a² + 2ab + b² の各項を作成 ──────────────────────
        # 色分け仕様：a²=青, 2ab=白, b²=緑, (a+b)²=黄, 記号=白
        eq_eq  = MathTex("=",    font_size=48, color=WHITE)
        eq_a2  = MathTex("a^2",  font_size=48, color=COLOR_A)   # シアン青
        eq_p1  = MathTex("+",    font_size=48, color=WHITE)
        eq_2ab = MathTex("2ab",  font_size=48, color=WHITE)     # 白
        eq_p2  = MathTex("+",    font_size=48, color=WHITE)
        eq_b2  = MathTex("b^2",  font_size=48, color=COLOR_B)   # 緑

        # (a+b)² の右側に横一列で配置（まだ非表示）
        row1_expansion = VGroup(eq_eq, eq_a2, eq_p1, eq_2ab, eq_p2, eq_b2)
        row1_expansion.arrange(RIGHT, buff=0.20)
        row1_expansion.next_to(eq_ab2, RIGHT, buff=0.25)

        # ── 仕様通り = → a² → + → 2ab → + → b² の順に出現 ───
        self.play(
            Write(eq_eq),
            run_time=0.4,
        )
        self.wait(0.1)

        self.play(
            FadeIn(eq_a2, shift=UP * 0.15),
            run_time=0.5,
        )
        self.wait(0.1)

        self.play(
            Write(eq_p1),
            run_time=0.3,
        )
        self.wait(0.1)

        self.play(
            FadeIn(eq_2ab, shift=UP * 0.15),
            run_time=0.5,
        )
        self.wait(0.1)

        self.play(
            Write(eq_p2),
            run_time=0.3,
        )
        self.wait(0.1)

        self.play(
            FadeIn(eq_b2, shift=UP * 0.15),
            run_time=0.5,
        )

        self.wait(1.5)
        # ── 後続フェーズで参照する変数 ─────────────────────────
        # eq_ab2   : フェーズ7（FadeOut）、フェーズ9（消去）で使用
        # eq_2ab   : フェーズ7（+2ab と −2ab の衝突演出）で使用
        # eq_a2    : フェーズ9（a²+b² の再配置）で使用
        # eq_b2    : フェーズ9（a²+b² の再配置）で使用
        # eq_p1,p2 : フェーズ9（式の整理）で使用
        # EQ_Y     : フェーズ6以降（行2の配置基準）で使用

        # ═══════════════════════════════════════════════════════
        # フェーズ5：4つの三角形の面積を示す
        # ═══════════════════════════════════════════════════════

        # 三角形オブジェクトをリストで管理
        # Transform後の実体は orig_group, copy_TR, copy_BR, copy_BL
        tris = [orig_group, copy_TR, copy_BR, copy_BL]

        # 各三角形の重心を計算（½ab ラベルの配置基準）
        centroid_TL = (sq_TL + P1 + P4) / 3
        centroid_TR = (sq_TR + P2 + P1) / 3
        centroid_BR = (sq_BR + P3 + P2) / 3
        centroid_BL = (sq_BL + P4 + P3) / 3
        centroids = [centroid_TL, centroid_TR, centroid_BR, centroid_BL]

        # ── 左上の三角形（tris[0]）を白くフラッシュ ──────────────
        self.play(
            Indicate(tris[0], color=WHITE, scale_factor=1.05),
            run_time=0.8,
        )
        self.wait(0.2)

        # ── 辺 a（青）をグロー強調 ────────────────────────────────
        # submobject[2] = la（a辺、青）← make_tri の定義と合わせた順序
        self.play(
            Indicate(tris[0][2], color=COLOR_A, scale_factor=1.4),
            run_time=0.7,
        )
        self.wait(0.2)

        # ── 辺 b（緑）をグロー強調 ────────────────────────────────
        # submobject[1] = lb（b辺、緑）
        self.play(
            Indicate(tris[0][1], color=COLOR_B, scale_factor=1.4),
            run_time=0.7,
        )
        self.wait(0.3)

        # ── TL三角形の中央に ½ab ラベルをフェードイン ────────────
        label_half_ab = [
            MathTex(r"\frac{1}{2}ab", font_size=30, color=WHITE)
            for _ in range(4)
        ]
        for lbl, c in zip(label_half_ab, centroids):
            lbl.move_to(c)

        self.play(
            FadeIn(label_half_ab[0], scale=0.8),
            run_time=0.8,
        )
        self.wait(0.5)

        # ── 残り3つの三角形に ½ab を一斉に表示 ──────────────────
        self.play(
            FadeIn(label_half_ab[1], scale=0.8),
            FadeIn(label_half_ab[2], scale=0.8),
            FadeIn(label_half_ab[3], scale=0.8),
            run_time=0.8,
        )

        self.wait(1.5)

        # ── 後続フェーズで参照する変数 ──────────────────────────
        # label_half_ab : フェーズ8（三角形フェードアウト時に一緒に消える）
        # tris          : フェーズ8（1枚ずつフェードアウト）
        # centroids     : フェーズ6（4×½ab=2ab の式配置）で参照可能

        # ═══════════════════════════════════════════════════════
        # フェーズ6：4つの三角形の合計面積
        # ═══════════════════════════════════════════════════════

        # 行2のY座標（行1の少し下）
        # フレーム底（y = -4.0）に対して font_size=48（高さ≈0.45u）が収まるよう設定
        # EQ_Y2 = -2.9 - 0.60 = -3.50 → 下端 ≈ -3.73（フレーム内）
        EQ_Y2 = EQ_Y - 0.60

        # ── 4つの三角形の中央に「4 × ½ab = 2ab」をフェードイン ──
        eq_4x_half = MathTex(r"4 \times \frac{1}{2}ab", font_size=44, color=WHITE)
        eq_eq6     = MathTex("=",                        font_size=44, color=WHITE)
        eq_2ab_r2  = MathTex("2ab",                      font_size=48, color=WHITE)

        # 横一列に並べて原点（4つの三角形の中央）に配置
        _layout6 = VGroup(eq_4x_half, eq_eq6, eq_2ab_r2)
        _layout6.arrange(RIGHT, buff=0.25)
        _layout6.move_to(ORIGIN)

        self.play(
            FadeIn(eq_4x_half, scale=0.9),
            FadeIn(eq_eq6,     scale=0.9),
            FadeIn(eq_2ab_r2,  scale=0.9),
            run_time=1.0,
        )
        self.wait(0.8)

        # ── 2ab を行2へスライド、「4 × ½ab =」を同時 FadeOut ────
        # 行2の目標位置：行1の +2ab（eq_2ab）と同じ x 座標、行2の y 座標
        # ※ フェーズ7で −2ab が真上の +2ab と衝突するよう x を揃える
        eq_2ab_r2.generate_target()
        eq_2ab_r2.target.move_to(
            np.array([eq_2ab.get_x(), EQ_Y2, 0])
        )

        self.play(
            MoveToTarget(eq_2ab_r2, rate_func=smooth),
            FadeOut(eq_4x_half),
            FadeOut(eq_eq6),
            run_time=1.2,
        )

        self.wait(1.5)

        # ── 後続フェーズで参照する変数 ──────────────────────────
        # eq_2ab_r2 : 行2の 2ab（フェーズ7で左に − が付き −2ab になる）
        # EQ_Y2     : 行2のY座標（フェーズ7で使用）


        # ═══════════════════════════════════════════════════════
        # フェーズ7：−2ab の登場と相殺
        # ═══════════════════════════════════════════════════════

        # ── 行2の 2ab の左に「−」をフェードイン → −2ab になる ──
        minus_sign = MathTex("-", font_size=48, color=WHITE)
        minus_sign.move_to(np.array([eq_p1.get_x(), eq_2ab_r2.get_y(), 0]))

        self.play(
            FadeIn(minus_sign, shift=LEFT * 0.12),
            run_time=0.6,
        )
        self.wait(0.3)

        # ── 外側正方形の辺ラベル（ブレース類）をフェードアウト ───
        # outer_sq（黄枠）はフェーズ8まで残す
        self.play(
            FadeOut(brace_top_b),  FadeOut(label_top_b),
            FadeOut(brace_top_a),  FadeOut(label_top_a),
            FadeOut(tick_top),
            FadeOut(brace_right_b), FadeOut(label_right_b),
            FadeOut(brace_right_a), FadeOut(label_right_a),
            FadeOut(tick_right),
            run_time=0.8,
        )
        self.wait(0.3)

        # ── −2ab がゆっくり上昇して行1の +2ab（eq_2ab）に衝突 ───
        # minus_sign と eq_2ab_r2 を同量シフトして eq_2ab の位置へ揃える
        stop_gap = 0.35  # この値を大きくするほど手前で止まる（単位: Manim座標）
        collision_shift = eq_2ab.get_center() - eq_2ab_r2.get_center() - UP * stop_gap

        self.play(
            eq_2ab_r2.animate.shift(collision_shift),
            minus_sign.animate.shift(collision_shift),
            run_time=1.5,
            rate_func=smooth,
        )

        # ── バウンス演出（上下に少し弾む）────────────────────────
        # 衝突に巻き込まれるオブジェクト：−2ab（2つ）と +2ab（eq_2ab）と その左の +（eq_p1）
        BOUNCE = 0.15

        # ① 衝突の反動で上へ
        self.play(
            eq_2ab_r2.animate.shift(UP * BOUNCE),
            minus_sign.animate.shift(UP * BOUNCE),
            eq_2ab.animate.shift(UP * BOUNCE),
            eq_p1.animate.shift(UP * BOUNCE),
            run_time=0.25,
            rate_func=linear,
        )
        # ② 下へ戻る
        self.play(
            eq_2ab_r2.animate.shift(DOWN * BOUNCE),
            minus_sign.animate.shift(DOWN * BOUNCE),
            eq_2ab.animate.shift(DOWN * BOUNCE),
            eq_p1.animate.shift(DOWN * BOUNCE),
            run_time=0.25,
            rate_func=linear,
        )

        # ── +2ab（行1）と −2ab（行2）が両方消える ────────────────
        # eq_p1（+2ab の直前の「+」）も同時消去
        # → 残り行1: eq_ab2 / eq_eq / eq_a2 / eq_p2 / eq_b2
        #   = "(a+b)² = a² + b²"（eq_p2 が自然に a² と b² の間の + になる）
        self.play(
            FadeOut(eq_2ab_r2),
            FadeOut(minus_sign),
            FadeOut(eq_2ab),
            FadeOut(eq_p1),
            run_time=0.5,
        )

        self.wait(1.5)

        # ── 後続フェーズで参照する変数 ──────────────────────────
        # eq_ab2        : フェーズ9（FadeOut）で使用
        # eq_eq         : フェーズ9（式の整理）で使用
        # eq_a2, eq_p2, eq_b2 : フェーズ9（a²+b² の再配置）で使用
        # outer_sq      : フェーズ8（黄色 → 白枠に変更）で使用
        # inner_sq      : フェーズ8（c² 正方形として残る）で使用
        # tris          : フェーズ8（1枚ずつフェードアウト）で使用
        # label_half_ab : フェーズ8（各三角形と一緒に消える）で使用

        # ═══════════════════════════════════════════════════════
        # フェーズ8：三角形が消えて c² だけ残る
        # ═══════════════════════════════════════════════════════

        # 左上→右上→右下→左下の順に1枚ずつフェードアウト
        # ½ab ラベルも各三角形と同時に消える
        #　三角形が1枚消えるたびに外枠を細くする
        outer_widths = [3.0, 2.0, 1.0, 0.4]

        for i in range(4):  # TL(0) → TR(1) → BR(2) → BL(3)
            self.play(
                FadeOut(tris[i]),
                FadeOut(label_half_ab[i]),
                outer_sq.animate.set_stroke(width=outer_widths[i]),
                run_time=0.5,
                rate_func=smooth,
            )
            self.wait(0.1)

        # 色を白へ・幅を最終値に整える
        self.play(
            outer_sq.animate.set_stroke(color=WHITE, width=0.5),
            run_time=0.8,
            rate_func=smooth,
        )
       
        self.wait(1.5)

        # ── 後続フェーズで参照する変数 ──────────────────────────
        # inner_sq  : フェーズ9（c² の正方形として残る）で使用
        # outer_sq  : フェーズ10（FadeOut）で使用
        # eq_ab2, eq_eq, eq_a2, eq_p2, eq_b2 : フェーズ9（式の整理）で使用

        # ═══════════════════════════════════════════════════════
        # フェーズ9：(a+b)² が消え、a²+b² = c² が完成する
        # ═══════════════════════════════════════════════════════

        # ── (a+b)² と = をフェードアウト ────────────────────────
        # eq_eq（展開式の「=」）も同時に消してすっきりさせる
        self.play(
            FadeOut(eq_ab2),
            FadeOut(eq_eq),
            run_time=0.8,
            rate_func=smooth,
        )
        self.wait(0.3)

        # ── 最終式 a² + b² = c² の目標レイアウトを計算 ──────────
        # ダミーVGroupで各項の目標座標を算出（画面中央・数式エリア）
        _layout9 = VGroup(
            MathTex("a^2", color=COLOR_A, font_size=48),
            MathTex("+",   color=WHITE,   font_size=48),
            MathTex("b^2", color=COLOR_B, font_size=48),
            MathTex("=",   color=WHITE,   font_size=48),
            MathTex("c^2", color=COLOR_C, font_size=48),
        )
        _layout9.arrange(RIGHT, buff=0.20)
        _layout9.move_to(np.array([0, EQ_Y, 0]))  # 水平中央・数式エリア

        # ── a², +, b² が中央に向かって移動し a² + b² としてまとまる ──
        self.play(
            eq_a2.animate.move_to(_layout9[0].get_center()),
            eq_p2.animate.move_to(_layout9[1].get_center()),
            eq_b2.animate.move_to(_layout9[2].get_center()),
            run_time=1.2,
            rate_func=smooth,
        )
        self.wait(0.5)

        # ── 内側正方形の2辺に c ラベルを表示 ──────────────────
        # 辺の中点から原点の外向きにオフセットして配置
        # 使用する2辺：P4→P1（左上辺）、P1→P2（右上辺）
        def _outward_pos(va, vb, offset=0.38):
            mid = (va + vb) / 2
            return mid + mid / np.linalg.norm(mid) * offset

        label_c_s1 = MathTex("c", font_size=36, color=COLOR_C)
        label_c_s2 = MathTex("c", font_size=36, color=COLOR_C)
        label_c_s1.move_to(_outward_pos(P4, P1))
        label_c_s2.move_to(_outward_pos(P1, P2))

        self.play(
            FadeIn(label_c_s1),
            FadeIn(label_c_s2),
            run_time=0.7,
        )
        self.wait(0.4)

        # ── 内側 c² 正方形の中央に c² ラベルをフェードイン ─────
        # inner_sq は P1,P2,P3,P4 の中心 = 原点
        label_c2 = MathTex("c^2", font_size=52, color=COLOR_C)
        label_c2.move_to(ORIGIN)

        self.play(FadeIn(label_c2, scale=0.8), run_time=0.8)
        self.wait(0.5)

        # ── c² ラベルが正方形の中央から数式エリアへスライド ─────
        # 辺の c ラベルも同時にフェードアウト
        self.play(
            label_c2.animate.move_to(_layout9[4].get_center()),
            FadeOut(label_c_s1),
            FadeOut(label_c_s2),
            run_time=1.2,
            rate_func=smooth,
        )
        self.wait(0.3)

        # ── = 符号がフェードインして a² + b² = c² が完成 ────────
        eq_final_eq = MathTex("=", font_size=48, color=WHITE)
        eq_final_eq.move_to(_layout9[3].get_center())

        self.play(
            FadeIn(eq_final_eq, scale=1.2),
            run_time=0.6,
        )

        self.wait(1.5)

        # ── 後続フェーズで参照する変数 ──────────────────────────
        # eq_a2, eq_p2, eq_b2 : フェーズ10（式の拡大強調）で使用
        # eq_final_eq         : フェーズ10（式の拡大強調）で使用
        # label_c2            : フェーズ10（式の拡大強調）で使用
        # outer_sq, inner_sq  : フェーズ10（FadeOut）で使用

        # ═══════════════════════════════════════════════════════
        # フェーズ10：最終強調
        # ═══════════════════════════════════════════════════════

        # ── 完成した a² + b² = c² を VGroup にまとめる ──────────
        # （eq_a2, eq_p2, eq_b2, eq_final_eq, label_c2 は全て EQ_Y 上に整列済み）
        final_eq_group = VGroup(eq_a2, eq_p2, eq_b2, eq_final_eq, label_c2)

        # ── 式を 1.0 → 1.6 → 1.3 倍に拡大縮小 ─────────────────
        self.play(
            final_eq_group.animate.scale(1.6),
            run_time=0.8,
            rate_func=smooth,
        )
        self.play(
            final_eq_group.animate.scale(1.3 / 1.6),  # 1.6倍状態から 1.3倍へ
            run_time=0.5,
            rate_func=smooth,
        )
        self.wait(0.8)

        # ── 外側・内側の正方形をフェードアウト ──────────────────
        self.play(
            FadeOut(outer_sq),
            FadeOut(inner_sq),
            run_time=1.0,
            rate_func=smooth,
        )
        self.wait(0.5)

        # ── 最後に直角三角形1つをフェードイン ───────────────────
        # フェーズ1と同じ頂点 A, B, C で再生成
        # （フェーズ2〜8で4枚に分散・消去済みのため新規作成）
        final_tri      = Polygon(
            A, B, C,
            fill_color=WHITE, fill_opacity=0.08,
            stroke_color=WHITE, stroke_width=0,
        )
        final_side_b   = Line(A, B, color=COLOR_B, stroke_width=4)
        final_side_a   = Line(A, C, color=COLOR_A, stroke_width=4)
        final_side_c   = Line(B, C, color=COLOR_C, stroke_width=4)
        final_right_mk = RightAngle(
            final_side_b, final_side_a,
            length=0.22, color=WHITE, stroke_width=2,
        )
        final_tri_group = VGroup(
            final_tri, final_side_b, final_side_a, final_side_c, final_right_mk,
        )

        self.play(
            FadeIn(final_tri_group),
            run_time=1.0,
            rate_func=smooth,
        )

        # ↓ ここから追加 ──────────────────────────────────────
        # ── 辺ラベルを作成（頂点・法線はフェーズ1と同じ変数をそのまま使用）──
        final_label_a = MathTex("a", color=COLOR_A, font_size=42)
        final_label_b = MathTex("b", color=COLOR_B, font_size=42)
        final_label_c = MathTex("c", color=COLOR_C, font_size=42)

        final_label_a.move_to((A + C) / 2 + LEFT  * 0.38)
        final_label_b.move_to((A + B) / 2 + DOWN  * 0.38)
        final_label_c.move_to((B + C) / 2 + bc_norm * 0.40)  # bc_norm はフェーズ1で定義済み

        self.play(
            FadeIn(final_label_a, shift=LEFT    * 0.1),
            FadeIn(final_label_b, shift=DOWN    * 0.1),
            FadeIn(final_label_c, shift=bc_norm * 0.1),
            run_time=1.0,
            lag_ratio=0.25,
        )
        # ↑ ここまで追加 ──────────────────────────────────────

        self.wait(3.0)
