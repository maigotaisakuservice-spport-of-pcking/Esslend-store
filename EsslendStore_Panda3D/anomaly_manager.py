import random

class AnomalyManager:
    """
    全ての異変データを管理し、抽選を行うクラス。
    """
    def __init__(self):
        self._load_anomalies()
        self.last_anomaly = None

    def _load_anomalies(self):
        """仕様書から全ての異変データをロードする"""
        self.all_anomalies = [
            # Tier 1: 即死・空間変化
            {'id': 'S01', 'tier': 1, 'desc': 'Shelf Man (擬態)'},
            {'id': 'S02', 'tier': 1, 'desc': 'Shelf Man (徘徊)'},
            {'id': 'S03', 'tier': 1, 'desc': '逆流トイレ'},
            {'id': 'S04', 'tier': 1, 'desc': '地下への階段'},
            {'id': 'S05', 'tier': 1, 'desc': '突然のT字路'},
            {'id': 'S06', 'tier': 1, 'desc': 'ブラックアウト'},
            # Tier 2: ホラー・精神的恐怖
            {'id': 'H01', 'tier': 2, 'desc': '視線'},
            {'id': 'H02', 'tier': 2, 'desc': '監視カメラ'},
            {'id': 'H03', 'tier': 2, 'desc': '増殖する店員'},
            {'id': 'H04', 'tier': 2, 'desc': '手招き'},
            {'id': 'H05', 'tier': 2, 'desc': '高速チャイム'},
            {'id': 'H06', 'tier': 2, 'desc': 'ポスターの顔'},
            # Tier 3: 違和感・環境変化
            {'id': 'E01', 'tier': 3, 'desc': '商品裏返し'},
            {'id': 'E02', 'tier': 3, 'desc': '巨大化'},
            {'id': 'E03', 'tier': 3, 'desc': '異常な値札'},
            {'id': 'E04', 'tier': 3, 'desc': '無限の奥行き'},
            {'id': 'E05', 'tier': 3, 'desc': 'コピー商品'},
            {'id': 'E06', 'tier': 3, 'desc': '水浸し'},
            {'id': 'E07', 'tier': 3, 'desc': '異臭（緑の霧）'},
            {'id': 'E08', 'tier': 3, 'desc': '照明点滅'},
            {'id': 'E09', 'tier': 3, 'desc': 'ポップ消失'},
            {'id': 'E10', 'tier': 3, 'desc': '赤い床'},
            {'id': 'E11', 'tier': 3, 'desc': '位置ズレ'},
            {'id': 'E12', 'tier': 3, 'desc': '完全無音'},
            {'id': 'E13', 'tier': 3, 'desc': 'ロゴ変化'},
            {'id': 'E14', 'tier': 3, 'desc': '鏡なし'},
            {'id': 'E15', 'tier': 3, 'desc': '空調強風'},
            # Tier 4: ストーリー伏線
            {'id': 'M01', 'tier': 4, 'desc': 'Endlessレシート'},
            {'id': 'M02', 'tier': 4, 'desc': '時計逆回転'},
        ]

    def pick_new_anomaly(self):
        """
        新しい異変を抽選する。
        同じ異変が2回連続で選ばれないようにする。
        """
        if not self.all_anomalies:
            print("Error: Anomaly list is empty!")
            return None

        # 前回選ばれた異変を除外したリストを作成
        available_anomalies = [a for a in self.all_anomalies if a['id'] != (self.last_anomaly['id'] if self.last_anomaly else None)]

        # 万が一リストが空になった場合（異変が1つしかないなど）は元のリストを使う
        if not available_anomalies:
            available_anomalies = self.all_anomalies

        # 新しい異変をランダムに選択
        current_anomaly = random.choice(available_anomalies)

        # 今回選ばれたものを「前回の異変」として記録
        self.last_anomaly = current_anomaly

        return current_anomaly
