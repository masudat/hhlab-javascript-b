var Recommendations = function () {
  this.critics = critics;
};


// person1 と person2 の距離を基にした類似性スコアを返す
Recommendations.prototype.sim_distance = function (prefs, person1, person2) {

  // 二人とも評価しているアイテムのリストを得る
  // と同時に要素の数を数えておく
  var si = {}, n = 0;
  (function () {
    for (var item in prefs[person1]) {
      if (item in prefs[person2]) {
        si[item] = 1;
        n += 1;
      }
    }
  })();

  // 共に評価しているアイテムがなければ 0 を返す
  if (n === 0) return 0;

  // すべての差の平方を足し合わせる
  var sum_of_squares = 0;
  (function () {
    for (var item in prefs[person1]) {
      if (item in prefs[person2]) {
        sum_of_squares += Math.pow(prefs[person1][item] - prefs[person2][item], 2);
      }
    }
  })();

  return 1 / (1 + sum_of_squares);

};


// p1 と p2 のピアソン相関係数を返す
Recommendations.prototype.sim_pearson = function (prefs, person1, person2) {

  // 二人とも評価しているアイテムのリストを得る
  // と同時に要素の数を数えておく
  var si = {}, n = 0;
  for (var item in prefs[person1]) {
    if (item in prefs[person2]) {
      si[item] = 1;
      n += 1;
    }
  }

  // 共に評価しているアイテムがなければ 0 を返す
  if (n === 0) return 0;

  // すべての嗜好を合計する
  // 平方を合計する
  // 積を合計する
  var sum1 = 0, sum2 = 0, sum1Sq = 0, sum2Sq = 0, pSum = 0;
  for (var it in si) {
    sum1 += prefs[person1][it];
    sum2 += prefs[person2][it];
    sum1Sq += Math.pow(prefs[person1][it], 2);
    sum2Sq += Math.pow(prefs[person2][it], 2);
    pSum += prefs[person1][it] * prefs[person2][it];
  }

  // ピアソンによるスコアを計算する
  var num = pSum - (sum1 * sum2 / n);
  var den = Math.sqrt((sum1Sq - Math.pow(sum1, 2) / n) * (sum2Sq - Math.pow(sum2, 2) / n));

  if (den === 0) return 0;

  return num / den;

};


// ディクショナリ prefs から person にもっともマッチするものたちを返す
// 結果の数と類似性関数はオプションのパラメータ
Recommendations.prototype.topMatches = function (prefs, person, n, similarity) {
  n = (typeof n === 'undefined') ? 5 : n;
  similarity = (typeof similarity === 'undefined') ? sim_pearson : similarity;

};


// person 以外の全ユーザの評点の重み付き平均を使い、person への推薦を算出する
Recommendations.prototype.getRecommendations = function (prefs, person, similarity) {
  similarity = (typeof similarity === 'undefined') ? sim_pearson : similarity;

};


Recommendations.prototype.transformPrefs = function (prefs) {

};


Recommendations.prototype.calculateSimilarItems = function (prefs, n) {
  n = (typeof n === 'undefined') ? 5 : n;

};
