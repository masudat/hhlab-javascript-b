require(["jquery", "../../lib/main"], function($) {
  $(function() {

    // とりあえず、フォームに入力されたデータをつかうための用意
    var makeOption = (function ($form) {
      var func = function ($form) {
        var source = JSON.parse( $('[name="source"]', $form).first().val() ) || '';
        var $option = $('<option />');

        $('[name*="target"]', $form).html('');

        for (var name in source) {
          $option.clone().val(name).text(name).appendTo($('[name*="target"]', $form));
        }
      };

      // 初回読み込み時にも実行
      func();

      // [name="source"]の変更があったときにoptionを再構成
      $( $('[name="source"]').first() ).on('keyup change', function (e) {
        func( $(this).closest('form') );
      });

      return func;
    })();

    // Recommendations をつかう
    var recommendations = new Recommendations();

    // 2章
    $('#demo-form-chapter2').on('submit', function (e) {
      e.preventDefault();

      var source = JSON.parse( $('[name="source"]', this).first().val() );
      var method = $('[name="method"]:checked', this).val();

      // 2.3.1 / 2.3.2
      var c31_target_a = $('[name="c31_target_a"]', this).first().val();
      var c31_target_b = $('[name="c31_target_b"]', this).first().val();
      var c31_result = recommendations[method](source, c31_target_a, c31_target_b);
      $('[name="c31_result"]', this).first().val(c31_result);

      // 2.3.4
      var c34_target = $('[name="c34_target"]', this).first().val();
      var c34_limit = $('[name="c34_limit"]', this).first().val();
      var c34_result = recommendations.topMatches(source, c34_target, c34_limit, method);
      $('[name="c34_result"]', this).first().html(c34_result.join('<br>'));

      // 2.4
      var c40_target = $('[name="c40_target"]', this).first().val();
      var c40_result = recommendations.getRecommendations(source, c40_target, method);
      $('[name="c40_result"]', this).first().html(c40_result.join('<br>'));
    });

  });
});
