import random
from datetime import timedelta

class GameManager:
    """
    ゲーム全体の進行、状態、時刻を管理するクラス。
    Pythonでゲームのコアロジックを担います。
    """
    def __init__(self, anomaly_manager, base_app):
        self.anomaly_manager = anomaly_manager
        self.base_app = base_app # main.pyのインスタンスにアクセスするため

        # --- ゲームバランス設定 ---
        self.anomaly_chance = 0.75  # 異変が発生する確率
        self.time_advance_minutes = 35 # 正解時に進む時間

        # --- ゲーム状態変数 ---
        self.current_time = None
        self.is_anomaly_active = False
        self.correct_answers = 0
        self.win_time = timedelta(hours=4, minutes=40)

    @property
    def time_as_string(self):
        """時刻を HH:MM 形式の文字列で返す"""
        hours, remainder = divmod(self.current_time.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}"

    def start_new_shift(self):
        """新しい夜勤を開始する"""
        self.current_time = timedelta(hours=0)
        self.correct_answers = 0
        print(f"--- New Shift Started --- Time: {self.time_as_string}")
        self.prepare_next_loop()

    def prepare_next_loop(self):
        """次のループの準備をする。異変を抽選し状態を更新する。"""
        if random.random() <= self.anomaly_chance:
            next_anomaly = self.anomaly_manager.pick_new_anomaly()
            if next_anomaly:
                self.is_anomaly_active = True
                # ここで3D空間に異変を実際に生成するロジックを呼び出す
                # self.base_app.level.spawn_anomaly(next_anomaly)
                print(f"Anomaly spawned: {next_anomaly['id']}")
            else:
                self.is_anomaly_active = False
        else:
            self.is_anomaly_active = False
            print("No anomaly generated for this loop (by chance).")

        print(f"Loop Prepared. Anomaly Active: {self.is_anomaly_active}")

    def process_player_decision(self, player_reported_anomaly):
        """プレイヤーの判断を処理する"""
        print(f"Player reported anomaly: {player_reported_anomaly}. Actual state: {self.is_anomaly_active}")
        is_correct = (self.is_anomaly_active == player_reported_anomaly)

        if is_correct:
            self._advance_time()
        else:
            self._reset_shift()

    def _reset_shift(self):
        """不正解だった場合にシフトをリセットする"""
        print(f"Incorrect decision. Resetting shift from {self.time_as_string}.")
        # プレイヤーをスタート地点に戻す処理などを呼び出す
        # self.base_app.player.reset_position()
        self.start_new_shift()

    def _advance_time(self):
        """正解だった場合に時刻を進める"""
        self.correct_answers += 1
        self.current_time += timedelta(minutes=self.time_advance_minutes)
        print(f"Correct decision. Time advanced to {self.time_as_string}. Total correct: {self.correct_answers}")

        if self.current_time >= self.win_time:
            self._end_shift()
        else:
            # 次のループへ
            self.prepare_next_loop()

    def _end_shift(self):
        """シフト完了（ゲームクリア）の処理"""
        print("--- Shift Complete! --- You survived.")
        # エンディング処理（アプリケーション終了など）
        self.base_app.userExit()
