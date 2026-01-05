from panda3d.core import NodePath, CollisionNode, CollisionSphere, CollisionHandlerPusher, BitMask32
from direct.task import Task

class Player:
    """
    プレイヤーキャラクターを管理するクラス。
    FPS視点のカメラ制御、移動、衝突判定を担当します。
    """
    def __init__(self, base):
        self.base = base
        self.camera = self.base.camera
        self.render = self.base.render

        # プレイヤーの物理的な実体（CollisionNode）を設定
        self.player_node = NodePath("player")
        self.player_node.reparentTo(self.render)
        self.player_node.setPos(0, 0, 1.0) # 初期位置 (床から少し上)

        # カメラをプレイヤーノードの子にする
        self.camera.reparentTo(self.player_node)
        self.camera.setPos(0, 0, 0.5) # プレイヤーの頭の高さにカメラを調整

        # 衝突判定の設定
        c_node = CollisionNode('player_collider')
        c_node.addSolid(CollisionSphere(0, 0, 0, 0.5)) # 半径0.5mの球体
        c_node.setFromCollideMask(BitMask32.bit(1))
        c_node.setIntoCollideMask(BitMask32.allOff())
        self.collider = self.player_node.attachNewNode(c_node)

        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.collider, self.player_node)
        self.base.cTrav.addCollider(self.collider, self.pusher)

        # プレイヤーの移動と視点操作に関する変数
        self.speed = 5.0
        self.sensitivity = 50.0
        self.heading = 0
        self.pitch = 0

        # キー入力の状態を保持する辞書
        self.key_map = {
            "forward": False, "backward": False, "left": False, "right": False
        }

        # キーボードイベントの受付を開始
        self.setup_controls()

        # プレイヤーの更新タスクを追加
        self.base.taskMgr.add(self.update, "player_update")

    def setup_controls(self):
        """キーボードの入力を受け付ける"""
        self.base.accept("w", self.update_key_map, ["forward", True])
        self.base.accept("w-up", self.update_key_map, ["forward", False])
        self.base.accept("s", self.update_key_map, ["backward", True])
        self.base.accept("s-up", self.update_key_map, ["backward", False])
        self.base.accept("a", self.update_key_map, ["left", True])
        self.base.accept("a-up", self.update_key_map, ["left", False])
        self.base.accept("d", self.update_key_map, ["right", True])
        self.base.accept("d-up", self.update_key_map, ["right", False])

    def update_key_map(self, key, value):
        """キー入力の状態を更新する"""
        self.key_map[key] = value

    def update(self, task):
        """毎フレーム呼ばれる更新処理"""
        dt = globalClock.getDt()

        # --- 視点操作 ---
        if self.base.mouseWatcherNode.hasMouse():
            md = self.base.win.getPointer(0)
            x = md.getX()
            y = md.getY()

            # 画面中央との差分からマウスの移動量を取得
            mouse_dx = x - self.base.win.getXSize() // 2
            mouse_dy = y - self.base.win.getYSize() // 2

            # 左右の視点移動 (heading)
            self.heading -= mouse_dx * self.sensitivity * dt
            # 上下の視点移動 (pitch)
            self.pitch -= mouse_dy * self.sensitivity * dt

            # 上下の角度制限
            self.pitch = max(-80, min(80, self.pitch))

            self.player_node.setHpr(self.heading, 0, 0)
            self.camera.setHpr(0, self.pitch, 0)

            # マウスカーソルを画面中央に戻す
            self.base.win.movePointer(0, self.base.win.getXSize() // 2, self.base.win.getYSize() // 2)

        # --- 移動処理 ---
        move_direction = [0, 0, 0]
        if self.key_map["forward"]:
            move_direction[1] += 1
        if self.key_map["backward"]:
            move_direction[1] -= 1
        if self.key_map["left"]:
            move_direction[0] -= 1
        if self.key_map["right"]:
            move_direction[0] += 1

        # 正規化して斜め移動が速くならないようにする
        move_vec = self.render.getRelativeVector(self.player_node, move_direction).normalized()

        self.player_node.setPos(self.player_node.getPos() + move_vec * self.speed * dt)

        return Task.cont
