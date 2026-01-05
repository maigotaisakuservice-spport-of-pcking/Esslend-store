from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, NodePath

# 作成した各モジュールをインポート
from player import Player
from level import Level
from game_manager import GameManager
from anomaly_manager import AnomalyManager

class EsslendStore(ShowBase):
    """
    ゲームのメインアプリケーションクラス。
    全てのモジュールを統合し、ゲームループを管理します。
    """
    def __init__(self):
        ShowBase.__init__(self)

        self.win.getProperties().setTitle('Esslend Store')
        props = self.win.getProperties()
        props.setCursorHidden(True)
        props.setMouseMode(props.M_relative)
        self.win.requestProperties(props)
        self.setBackgroundColor(0, 0, 0)

        # --- 各システムのインスタンスを生成 ---
        self.level = Level(self)
        self.player = Player(self)
        self.anomaly_manager = AnomalyManager()
        self.game_manager = GameManager(self.anomaly_manager, self)

        # --- UIのセットアップ ---
        self.time_ui = self._create_ui_text()
        self.anomaly_ui = self._create_ui_text(pos=(-1.2, 0, 0.8))

        # --- ゲーム開始 ---
        self.player.player_node.setPos(-8, 28, 1.0) # スタッフルーム(Aエリア)から開始
        self.game_manager.start_new_shift()

        # --- メインループタスクを追加 ---
        self.taskMgr.add(self.game_loop, "game_loop")

    def _create_ui_text(self, pos=(-1.2, 0, 0.9), scale=0.07):
        """画面にテキストを表示するためのヘルパー関数"""
        text_node = TextNode(f'ui_text_{id(pos)}')
        text_node.setAlign(TextNode.A_left)
        text_node.setTextColor(1, 1, 1, 1)
        text_node_path = self.aspect2d.attachNewNode(text_node)
        text_node_path.setScale(scale)
        text_node_path.setPos(pos)
        return text_node

    def game_loop(self, task):
        """毎フレーム実行されるメインループ"""
        # UIを更新
        self.time_ui.setText(f"Time: {self.game_manager.time_as_string}")
        anomaly_status = "DETECTED" if self.game_manager.is_anomaly_active else "CLEAR"
        self.anomaly_ui.setText(f"Status: {anomaly_status}")

        # --- トリガー判定 ---
        player_pos = self.player.player_node.getPos()

        # 出口通路(Dエリア)のトリガーゾーン (y座標が-5以下)
        if player_pos.y < -5:
            print("Player entered the exit area.")
            # 異変なしと判断したとみなし、結果を処理
            self.game_manager.process_player_decision(False)
            # プレイヤーをスタート地点に戻す
            self.player.player_node.setPos(-8, 28, 1.0)

        # 入り口ドア(Aエリア)のトリガーゾーン (y座標が29以上)
        if player_pos.y > 29:
            print("Player returned to the entrance.")
            # 異変ありと判断したとみなし、結果を処理
            self.game_manager.process_player_decision(True)
            # プレイヤーをスタート地点に戻す
            self.player.player_node.setPos(-8, 28, 1.0)

        return task.cont

# アプリケーションのインスタンスを作成して実行
if __name__ == "__main__":
    app = EsslendStore()
    app.run()
