from manim import *
from src.utils.reel_scene import ReelScene

# ── Color palette ──────────────────────────────────────────────────────────────
BG_COLOR    = "#0d1117"
COL_DEFAULT = "#e6edf3"
COL_LABEL   = "#58a6ff"   # S(n) / S(10) blue
COL_GOLD    = "#ffd700"   # highlight gold
COL_RED     = "#ff7b72"   # strikethrough red
COL_GREEN   = "#7ee787"   # pair sum green
COL_ORANGE  = "#ff9d5c"   # brace orange
COL_BOX     = "#58a6ff"   # box border

# ── Row Y coordinates ──────────────────────────────────────────────────────────
ROW1_Y =  1.2   # upper  (正順の式)
ROW2_Y =  0.0   # middle (逆順の式)
ROW3_Y = -1.2   # lower  (2S(n) = …)

# ── 共通スケール（ReelScene: frame_width = 8.0 units）──────────────────────────
SCALE = 0.65
BUFF  = 0.18

# ── ラウンド設定 ───────────────────────────────────────────────────────────────
CFG_NUMERIC = {
    "label":       r"S(10)",
    "syms1":       ["1", "+", "2", "+", "3", "+", r"\cdots", "+", "10"],
    "syms2_rev":   ["10", "+", "9", "+", "8", "+", r"\cdots", "+", "1"],
    "pair_label":  "11",
    "pair_scale":  SCALE,
    "brace_label": r"\times 10",
    "mul_text":    r"11 \times 10",
    "val_2x":      "110",
    "label_2x":    r"2S(10)",
    "val_half":    "55",
    "label_half":  r"S(10)",
    "final_syms":  ["1", "+", "2", "+", "3", "+", r"\cdots", "+", "10"],
    "final_ans":   "55",
    "is_last":     False,
}

CFG_SYMBOLIC = {
    "label":       r"S(n)",
    "syms1":       ["1", "+", "2", "+", "3", "+", r"\cdots", "+", "n"],
    "syms2_rev":   ["n", "+", r"n{-}1", "+", r"n{-}2", "+", r"\cdots", "+", "1"],
    "pair_label":  r"(n+1)",
    "pair_scale":  SCALE * 0.82,
    "brace_label": r"\times n",
    "mul_text":    r"(n+1) \times n",
    "val_2x":      r"n(n+1)",
    "label_2x":    r"2S(n)",
    "val_half":    r"\frac{1}{2}n(n+1)",
    "label_half":  r"S(n)",
    "final_syms":  ["1", "+", "2", "+", "3", "+", r"\cdots", "+", "n"],
    "final_ans":   r"\frac{1}{2}n(n+1)",
    "is_last":     True,
}


class SeriesAnimation(ReelScene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        self._run_round(CFG_NUMERIC)
        self.wait(0.6)
        self.clear()
        self._run_round(CFG_SYMBOLIC)

    def _run_round(self, cfg):
        row1 = self._scene1(cfg)
        row2 = self._scene2(row1)
        row2_prefix, series2_rev = self._scene3(row2, cfg)
        row3_pre, result_groups, box_s10 = self._scene4(row1, row2_prefix, series2_rev, cfg)
        row3_pre, val_mob = self._scene5(row1, row2_prefix, series2_rev, row3_pre, result_groups, box_s10, cfg)
        s2_n, eq3, ans_mob = self._scene6(row1, row2_prefix, series2_rev, box_s10, row3_pre, val_mob, cfg)
        self._scene7(s2_n, eq3, ans_mob, cfg)

    # ──────────────────────────────────────────────────────────────────────────
    # ヘルパー: 指定した列中央 x 座標に要素を配置した series VGroup を生成
    # ──────────────────────────────────────────────────────────────────────────
    def _make_aligned_row(self, syms, col_centers, y):
        mobs = [MathTex(t, color=COL_DEFAULT).scale(SCALE) for t in syms]
        for mob, cx in zip(mobs, col_centers):
            mob.move_to([cx, y, 0])
        return VGroup(*mobs)

    # ──────────────────────────────────────────────────────────────────────────
    # Scene 1: 数列の登場と「= ?」
    # ──────────────────────────────────────────────────────────────────────────
    def _scene1(self, cfg):
        """
        1. 数列をタイプアウト（各要素 ~0.12 秒間隔）
        2. = ? をフェードイン
        3. 0.9 秒静止
        4. = ? をフェードアウト ← 同時に → S(n) = をフェードイン（0.8 秒）
        5. 0.3 秒静止
        """
        SYMS1     = cfg["syms1"]
        SYMS2_REV = cfg["syms2_rev"]

        # ── S(n) = prefix ────────────────────────────────────────────────────
        s_label = MathTex(cfg["label"], color=COL_LABEL).scale(SCALE)
        eq_pre  = MathTex(r"=",         color=COL_DEFAULT).scale(SCALE)
        prefix  = VGroup(s_label, eq_pre).arrange(RIGHT, buff=BUFF * 0.8)

        # ── 列幅を row1・row2 両方の最大幅で統一（縦揃えのため） ──────────────
        col_widths = [
            max(MathTex(t1).scale(SCALE).width, MathTex(t2).scale(SCALE).width)
            for t1, t2 in zip(SYMS1, SYMS2_REV)
        ]
        series_w = sum(col_widths) + BUFF * (len(col_widths) - 1)
        total_w  = prefix.width + BUFF + series_w

        prefix.move_to([-total_w / 2 + prefix.width / 2, ROW1_Y, 0])
        x = -total_w / 2 + prefix.width + BUFF
        col_centers = []
        for w in col_widths:
            col_centers.append(x + w / 2)
            x += w + BUFF
        self._col_centers = col_centers  # _scene3 で row2 にも再利用

        # ── series (row1): 各要素を列中央に配置 ─────────────────────────────
        series = self._make_aligned_row(SYMS1, col_centers, ROW1_Y)

        # ── = ? ───────────────────────────────────────────────────────────────
        eq_q = MathTex(r"= ?", color=COL_DEFAULT).scale(SCALE)
        eq_q.next_to(series, RIGHT, buff=BUFF)

        # 1. Typeout
        for elem in series:
            self.play(FadeIn(elem, run_time=0.12))

        # 2. Fade in "= ?"
        self.play(FadeIn(eq_q, run_time=0.4))

        # 3. Pause
        self.wait(0.9)

        # 4. Swap
        self.play(
            FadeOut(eq_q,   run_time=0.8),
            FadeIn(prefix,  run_time=0.8),
        )

        # 5. Pause
        self.wait(0.3)

        return VGroup(prefix, series)

    # ──────────────────────────────────────────────────────────────────────────
    # Scene 2: row2 の登場（スライドイン）
    # ──────────────────────────────────────────────────────────────────────────
    def _scene2(self, row1):
        """
        1. row1 と同じ内容を ROW1_Y にフェードイン
        2. ROW2_Y へ 0.9 秒スライド
        """
        row2 = row1.copy()
        row2.move_to([0, ROW1_Y, 0])

        self.play(FadeIn(row2, run_time=0.5))

        row2.generate_target()
        row2.target.move_to([0, ROW2_Y, 0])
        self.play(MoveToTarget(row2, run_time=0.9))

        return row2

    # ──────────────────────────────────────────────────────────────────────────
    # Scene 3: row2 を逆順に反転
    # ──────────────────────────────────────────────────────────────────────────
    def _scene3(self, row2, cfg):
        """
        row2 の数列部分を正順 → 逆順に変換（FadeOut → FadeIn）
        """
        series2 = row2[1]

        series2_rev = self._make_aligned_row(cfg["syms2_rev"], self._col_centers, ROW2_Y)

        self.play(FadeOut(series2, run_time=0.42))
        self.play(FadeIn(series2_rev, run_time=0.42))

        return row2[0], series2_rev  # (row2 prefix, 逆順 series)

    # ──────────────────────────────────────────────────────────────────────────
    # Scene 4: S(n)ボックス → 列ごとペアの和
    # ──────────────────────────────────────────────────────────────────────────
    def _scene4(self, row1, row2_prefix, series2_rev, cfg):
        """
        4①: S(n) を角丸ボックスで囲み、中間に赤い + → フェードアウト
        4②③: 列ごとに青いボックスでハイライトしながら
              row3 の resArea に pair_label を積み上げる
        """
        series1 = row1[1]
        s_r1    = row1[0][0]      # S(n) MathTex (row1)
        s_r2    = row2_prefix[0]  # S(n) MathTex (row2)

        # ── 4①: S(n) を囲む角丸ボックス ─────────────────────────────────────
        box_s10 = SurroundingRectangle(
            VGroup(s_r1, s_r2),
            corner_radius=0.12,
            color=COL_BOX,
            buff=0.08,
        )
        box_s10.set_fill(color=COL_BOX, opacity=0.09)
        box_s10.set_stroke(width=2.5)
        self.play(FadeIn(box_s10, run_time=0.4))

        # 2 つの S(n) の中間に赤い +
        plus_mid = MathTex("+", color=COL_RED).scale(SCALE)
        plus_mid.move_to([s_r1.get_center()[0], (ROW1_Y + ROW2_Y) / 2, 0])
        self.play(FadeIn(plus_mid, run_time=0.4))
        self.wait(0.65)
        self.play(FadeOut(plus_mid, run_time=0.3))

        # ── 4②③: row3 に "2S(n) =" を配置 ──────────────────────────────────
        s2_n     = MathTex(cfg["label_2x"], color=COL_LABEL).scale(SCALE)
        eq3      = MathTex(r"=",            color=COL_DEFAULT).scale(SCALE)
        row3_pre = VGroup(s2_n, eq3).arrange(RIGHT, buff=BUFF * 0.8)
        row3_pre.align_to(row1[0], LEFT).set_y(ROW3_Y)
        self.play(FadeIn(row3_pre, run_time=0.4))

        # 列ペア: (series の index, ラベル, ⋯フラグ)
        pairs = [
            (0, cfg["pair_label"], False),
            (2, cfg["pair_label"], False),
            (4, cfg["pair_label"], False),
            (6, r"\cdots",         True ),
            (8, cfg["pair_label"], False),
        ]

        res_last = row3_pre  # 次アイテムの配置基準
        result_groups = []

        for i, (col_idx, label, is_cdots) in enumerate(pairs):

            # 列ボックス（⋯ 列はスキップ）
            if not is_cdots:
                col_box = SurroundingRectangle(
                    VGroup(series1[col_idx], series2_rev[col_idx]),
                    corner_radius=0.1,
                    color=COL_BOX,
                    buff=0.06,
                )
                col_box.set_fill(color=COL_BOX, opacity=0.09)
                col_box.set_stroke(width=2.0)
                self.play(FadeIn(col_box, run_time=0.25))

            new_items = []
            if i > 0:
                plus_res = MathTex("+", color=COL_DEFAULT).scale(SCALE * 0.85)
                new_items.append(plus_res)

            color   = COL_GREEN if not is_cdots else COL_DEFAULT
            val_sc  = cfg["pair_scale"] if not is_cdots else SCALE
            val_mob = MathTex(label, color=color).scale(val_sc)
            new_items.append(val_mob)

            new_group = VGroup(*new_items).arrange(RIGHT, buff=BUFF * 0.5)
            new_group.next_to(res_last, RIGHT, buff=BUFF * 0.55)
            self.play(FadeIn(new_group, run_time=0.3))
            result_groups.append(new_group)
            res_last = new_group

            if not is_cdots:
                self.play(FadeOut(col_box, run_time=0.25))

        return row3_pre, result_groups, box_s10

    # ──────────────────────────────────────────────────────────────────────────
    # Scene 5: グレーアウト → 波括弧 → 右辺変換
    # ──────────────────────────────────────────────────────────────────────────
    def _scene5(self, row1, row2_prefix, series2_rev, row3_pre, result_groups, box_s10, cfg):
        """
        1. row1・row2 を opacity 0.2 にフェードアウト（薄暗く）
        2. resArea の下に波括弧と brace_label を表示（0.95 秒後フェードアウト）
        3. resArea を mul_text にフェード切替（0.8 秒）
        4. mul_text を val_2x にフェード切替（0.7 秒）、ゴールド
        """
        res_area = VGroup(*result_groups)

        # ── 1. row1・row2 を opacity 0.2 に ─────────────────────────────────
        self.play(
            row1.animate.set_opacity(0.2),
            row2_prefix.animate.set_opacity(0.2),
            series2_rev.animate.set_opacity(0.2),
            box_s10.animate.set_opacity(0.2),
            run_time=0.5,
        )

        # ── 2. 波括弧と brace_label ───────────────────────────────────────────
        brace = Brace(res_area, direction=DOWN)
        brace.set_color(COL_ORANGE)
        brace_label = MathTex(cfg["brace_label"], color=COL_ORANGE).scale(SCALE)
        brace_label.next_to(brace, DOWN, buff=0.1)

        self.play(
            FadeIn(brace,       run_time=0.4),
            FadeIn(brace_label, run_time=0.4),
        )
        self.wait(0.95)
        self.play(
            FadeOut(brace,       run_time=0.3),
            FadeOut(brace_label, run_time=0.3),
        )

        # ── 3. resArea を mul_text にフェード切替（0.8 秒） ───────────────────
        mul_mob = MathTex(cfg["mul_text"], color=COL_DEFAULT).scale(SCALE)
        mul_mob.next_to(row3_pre, RIGHT, buff=BUFF * 0.55)

        self.play(
            FadeOut(res_area, run_time=0.8),
            FadeIn(mul_mob,   run_time=0.8),
        )

        # ── 4. mul_text を val_2x にフェード切替（0.7 秒）、ゴールド ─────────
        val_mob = MathTex(cfg["val_2x"], color=COL_GOLD).scale(SCALE)
        val_mob.next_to(row3_pre, RIGHT, buff=BUFF * 0.55)

        self.play(
            FadeOut(mul_mob, run_time=0.7),
            FadeIn(val_mob,  run_time=0.7),
        )

        return row3_pre, val_mob

    # ──────────────────────────────────────────────────────────────────────────
    # Scene 6: 中央へ収束 → ÷2 → S(n)=val_half
    # ──────────────────────────────────────────────────────────────────────────
    def _scene6(self, row1, row2_prefix, series2_rev, box_s10, row3_pre, val_mob, cfg):
        """
        1. row1・row2 をフェードアウト（0.6 秒）
        2. 2S(n) = val_2x を画面中央へ移動（0.9 秒）
        3. val_2x 右に ÷2 フェードイン + 「2」に打ち消し線描画（同時）
        4. 1.1 秒後、2（打ち消し線ごと）・÷2・val_2x をフェードアウト
        5. = の直後に val_half をフェードイン
        6. val_half をゴールドにグロー強調（1.8 秒）
        """
        s2_n = row3_pre[0]  # MathTex(cfg["label_2x"])
        eq3  = row3_pre[1]  # MathTex(r"=")

        # ── 1. row1・row2 をフェードアウト（0.6 秒） ─────────────────────────
        self.play(
            FadeOut(row1,        run_time=0.6),
            FadeOut(row2_prefix, run_time=0.6),
            FadeOut(series2_rev, run_time=0.6),
            FadeOut(box_s10,     run_time=0.6),
        )

        # ── 2. 2S(n) = val_2x を画面中央へ移動（0.9 秒） ────────────────────
        expr_group = VGroup(row3_pre, val_mob)
        self.play(expr_group.animate.move_to(ORIGIN), run_time=0.9)
        self.wait(0.3)

        # ── 3. ÷2 フェードイン + 「2」に打ち消し線（同時） ──────────────────
        div2 = MathTex(r"\div 2", color=COL_DEFAULT).scale(SCALE)
        div2.next_to(val_mob, RIGHT, buff=BUFF * 0.55)

        # s2_n[0][0] = 「2」の第1パスのバウンディングボックスで打ち消し線を配置
        two_char = s2_n[0][0]
        strikeout = Line(
            two_char.get_corner(DL) + LEFT * 0.03 + DOWN * 0.03,
            two_char.get_corner(UR) + RIGHT * 0.03 + UP * 0.03,
            color=COL_RED,
            stroke_width=2.5,
        )

        self.play(
            FadeIn(div2,      run_time=0.6),
            Create(strikeout, run_time=0.6),
        )
        self.wait(1.1)

        # ── 4. 2（打ち消し線ごと）・÷2・val_2x をフェードアウト ──────────────
        # 2S(n) → S(n) へ Transform（「2」が消えるように見せる）
        sn_new = MathTex(cfg["label_half"], color=COL_LABEL).scale(SCALE)
        sn_new.align_to(s2_n, RIGHT).set_y(s2_n.get_center()[1])

        self.play(
            FadeOut(strikeout,          run_time=0.55),
            FadeOut(div2,               run_time=0.55),
            FadeOut(val_mob,            run_time=0.55),
            Transform(s2_n, sn_new,    run_time=0.55),
        )

        # ── 5. = の直後に val_half をフェードイン ────────────────────────────
        ans_mob = MathTex(cfg["val_half"], color=COL_DEFAULT).scale(SCALE)
        ans_mob.next_to(eq3, RIGHT, buff=BUFF * 0.55)
        self.play(FadeIn(ans_mob, run_time=0.6))
        self.wait(0.35)

        # ── 6. val_half をゴールドにグロー強調（1.8 秒） ─────────────────────
        self.play(
            ans_mob.animate.set_color(COL_GOLD),
            Flash(ans_mob, color=COL_GOLD, flash_radius=0.5, run_time=1.8),
        )

        return s2_n, eq3, ans_mob

    # ──────────────────────────────────────────────────────────────────────────
    # Scene 7: 最終式の表示
    # ──────────────────────────────────────────────────────────────────────────
    def _scene7(self, s2_n, eq3, ans_mob, cfg):
        """
        1. S(n) = val_half ラッパーをフェードアウト（1.2 秒）
        2. 画面中央に final_syms = final_ans をフェードイン（1.4 秒）
        3. is_last=False: 1.5 秒後にフェードアウト
           is_last=True:  ゴールドにグロー強調して保持
        """
        # ── 1. S(n) = val_half をフェードアウト（1.2 秒） ────────────────────
        self.play(
            FadeOut(s2_n,    run_time=1.2),
            FadeOut(eq3,     run_time=1.2),
            FadeOut(ans_mob, run_time=1.2),
        )

        # ── 2. 最終式をフェードイン（1.4 秒） ────────────────────────────────
        series_mobs = [MathTex(s, color=COL_DEFAULT).scale(SCALE) for s in cfg["final_syms"]]
        series_vg   = VGroup(*series_mobs).arrange(RIGHT, buff=BUFF * 0.7)
        eq_final    = MathTex(r"=",             color=COL_DEFAULT).scale(SCALE)
        ans_final   = MathTex(cfg["final_ans"], color=COL_GOLD).scale(SCALE)
        final_expr  = VGroup(series_vg, eq_final, ans_final).arrange(RIGHT, buff=BUFF * 0.9)
        final_expr.move_to(ORIGIN)

        # フレーム幅に収まるようスケール調整
        if final_expr.width > 7.5:
            final_expr.scale_to_fit_width(7.5)

        self.play(FadeIn(final_expr, run_time=1.4))

        # ── 3. ラウンド分岐 ───────────────────────────────────────────────────
        if not cfg["is_last"]:
            # Round 1: 1.5 秒後にフェードアウト（Round 2 へ接続）
            self.wait(1.5)
            self.play(FadeOut(final_expr, run_time=0.6))
        else:
            # Round 2（最終）: ゴールドにグロー強調して保持
            self.wait(0.5)
            self.play(
                Flash(ans_final, color=COL_GOLD, flash_radius=0.8, run_time=1.5),
            )
            self.wait(1.0)
