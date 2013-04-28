# -*- coding: utf-8 -*-
from math import sqrt


# 映画の評者といくつかの映画に対する彼らの評点のディクショナリ
critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 4.5
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5
    },
    'Toby': {
        'Snakes on a Plane': 4.5,
        'You, Me and Dupree': 1.0,
        'Superman Returns': 4.0
    },
}


# person1 と person2 の距離を基にした類似性スコアを返す
def sim_distance(prefs, person1, person2):

    # 二人とも評価しているアイテムのリストを得る
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    # 両者共に評価しているものが一つもなければ 0 の距離を基にした類似性スコアを返す
    if len(si) == 0:
        return 0

    # すべての差の平方を足し合わせる
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                         for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + sqrt(sum_of_squares))


# p1 と p2 のピアソン相関係数を返す
def sim_pearson(prefs, p1, p2):

    # 両者が互いに評価しているアイテムのリストを取得
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    # 要素の数を調べる
    n = len(si)

    # 共に評価しているアイテムがなければ 0 を返す
    if n == 0:
        return 0

    # すべての嗜好を合計する
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # 平方を合計する
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    # 積を合計する
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # ピアソンによるスコアを計算する
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0

    r = num / den

    return r


# ディクショナリ prefs から person にもっともマッチするものたちを返す
# 結果の数と類似性関数はオプションのパラメータ
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]

    # 高スコアがリストの最初に来るように並び替える
    scores.sort()
    scores.reverse()
    return scores[0:n]


# person 以外の全ユーザの評点の重み付き平均を使い、person への推薦を算出する
def getRecommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        # 自分自身とは比較しない
        if other == person:
            continue

        sim = similarity(prefs, person, other)

        # 0 以下のスコアは無視する
        if sim <= 0:
            continue

        for item in prefs[other]:
            # まだ見ていない映画の得点のみを算出
            if item not in prefs[person] or prefs[person][item] == 0:
                # 類似度 * スコア
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # 類似度を合計
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # 正規化したリストを作る
    rankings = [(total / simSums[item], item)
                for item, total in totals.items()]

    # ソート済みのリストを返す
    rankings.sort()
    rankings.reverse()
    return rankings


def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})

            # item と person を入れ替える
            result[item][person] = prefs[person][item]
    return result


def calculateSimilarItems(prefs, n=10):
    # アイテムをキーとして持ち、それぞれのアイテムに似ている
    # アイテムのリストを値として持つディクショナリを作る
    result = {}

    # 嗜好の行列をアイテム中心なかたちに反転させる
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        # 巨大なデータセット用にステータスを表示
        if c % 100 == 0:
            print "%d / %d" % (c, len(itemPrefs))
        # このアイテムにもっとも似ているアイテムたちを探す
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result
