from panda3d.core import NodePath, GeomNode, GeomVertexFormat, GeomVertexData, Geom, GeomTriangles, GeomVertexWriter, BitMask32, LColor

class Level:
    """
    ゲームのステージ（コンビニ店内）をプロシージャルに生成するクラス。
    床、壁、天井、棚などをコードで作成します。
    """
    def __init__(self, base):
        self.base = base
        self.render = self.base.render
        self.level_node = NodePath("level")
        self.level_node.reparentTo(self.render)

        # マップのパーツを生成
        self._create_floor()
        self._create_ceiling()
        self._create_walls()
        self._create_shelves()

    def _create_cube(self, name, parent, pos, scale, color=(0.5, 0.5, 0.5, 1.0)):
        """指定されたパラメータで立方体を生成するヘルパー関数"""
        format = GeomVertexFormat.getV3n3cpt2()
        vdata = GeomVertexData(name, format, Geom.UHStatic)

        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color_writer = GeomVertexWriter(vdata, 'color')

        # 8つの頂点を定義
        verts = [
            (-1, -1, -1), ( 1, -1, -1), ( 1,  1, -1), (-1,  1, -1),
            (-1, -1,  1), ( 1, -1,  1), ( 1,  1,  1), (-1,  1,  1)
        ]
        # 6つの面の法線
        norms = [
            ( 0, -1,  0), ( 0,  1,  0), (-1,  0,  0), ( 1,  0,  0),
            ( 0,  0, -1), ( 0,  0,  1)
        ]

        # 面を定義する頂点のインデックス
        faces = [
            (0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 7, 3),
            (1, 2, 6, 5), (3, 2, 6, 7), (0, 1, 5, 4)
        ]

        v_idx = 0
        for i in range(6):
            for j in range(4):
                vertex.addData3(verts[faces[i][j]])
                normal.addData3(norms[i])
                color_writer.addData4f(color)

            tris = GeomTriangles(Geom.UHStatic)
            tris.addVertices(v_idx, v_idx + 1, v_idx + 2)
            tris.addVertices(v_idx, v_idx + 2, v_idx + 3)
            tris.closePrimitive()

            geom = Geom(vdata)
            geom.addPrimitive(tris)

            node = GeomNode(f'{name}_geom_{i}')
            node.addGeom(geom)

            cube_part = parent.attachNewNode(node)
            v_idx += 4

        cube = parent.attachNewNode(name)
        for child in parent.findAllMatches(f"*/{name}_geom_*"):
            child.wrtReparentTo(cube)

        cube.setPos(pos)
        cube.setScale(scale)
        return cube

    def _create_floor(self):
        """床を生成する"""
        self._create_cube("floor", self.level_node, pos=(0, 10, 0), scale=(15, 20, 0.1), color=LColor(0.2, 0.2, 0.2, 1))

    def _create_ceiling(self):
        """天井を生成する"""
        self._create_cube("ceiling", self.level_node, pos=(0, 10, 3), scale=(15, 20, 0.1), color=LColor(0.8, 0.8, 0.9, 1))

    def _create_walls(self):
        """壁を生成する（L字型になるように配置）"""
        wall_color = LColor(0.9, 0.9, 0.8, 1)
        # 外壁
        w1 = self._create_cube("wall1", self.level_node, pos=(-10, 15, 1.5), scale=(0.1, 15, 1.5), color=wall_color)
        w2 = self._create_cube("wall2", self.level_node, pos=(0, 30, 1.5), scale=(10, 0.1, 1.5), color=wall_color)
        w3 = self._create_cube("wall3", self.level_node, pos=(10, 10, 1.5), scale=(0.1, 20, 1.5), color=wall_color)
        w4 = self._create_cube("wall4", self.level_node, pos=(0, -10, 1.5), scale=(10, 0.1, 1.5), color=wall_color)
        # 内壁
        w5 = self._create_cube("wall5", self.level_node, pos=(0, 10, 1.5), scale=(0.1, 20, 1.5), color=wall_color)
        w6 = self._create_cube("wall6", self.level_node, pos=(-5, 0, 1.5), scale=(5, 0.1, 1.5), color=wall_color)

        for wall in [w1, w2, w3, w4, w5, w6]:
            wall.setCollideMask(BitMask32.bit(1)) # プレイヤーとの衝突判定を有効にする

    def _create_shelves(self):
        """棚を生成する"""
        shelf_color = LColor(0.5, 0.4, 0.3, 1)
        # Bエリアの棚
        s1 = self._create_cube("shelf1", self.level_node, pos=(-5, 15, 1), scale=(4, 1, 1), color=shelf_color)
        s2 = self._create_cube("shelf2", self.level_node, pos=(-5, 10, 1), scale=(4, 1, 1), color=shelf_color)
        s3 = self._create_cube("shelf3", self.level_node, pos=(-5, 5, 1), scale=(4, 1, 1), color=shelf_color)
        # Cエリアの棚
        s4 = self._create_cube("shelf4", self.level_node, pos=(5, 0, 1), scale=(1, 5, 1), color=shelf_color)
        s5 = self._create_cube("shelf5", self.level_node, pos=(8, 0, 1), scale=(1, 5, 1), color=shelf_color)

        for shelf in [s1, s2, s3, s4, s5]:
            shelf.setCollideMask(BitMask32.bit(1)) # プレイヤーとの衝突判定を有効にする
