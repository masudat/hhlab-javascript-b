require(["jquery", "../../lib/main"], function($) {
  $(function() {

    var makeOption = function ($form) {
      var source = JSON.parse( $('*[name="source"]', $form).first().val() ) || '';
      var $option = $('<option />');

      $('*[name^="item"]').html('');

      for (var name in source) {
        $option.clone().val(name).text(name).appendTo($('*[name="item1"]', $form).first());
        $option.clone().val(name).text(name).appendTo($('*[name="item2"]', $form).first());
      }
    };

    $( $('*[name="source"]').first() ).on('keyup change', function (e) {
      makeOption( $(this).closest('form') );
    });

    makeOption($('#demo-form-sim'));

    $('#demo-form-sim').on('submit', function (e) {
      e.preventDefault();

      var source = JSON.parse( $('*[name="source"]', this).first().val() ) || '';
      var method = $('*[name="method"]:checked', this).val();

      var item1 = $('*[name="item1"]', this).first().val();
      var item2 = $('*[name="item2"]', this).first().val();

      var recommendations = new Recommendations();

      // データはひとまず中から持ってきている
      var result = recommendations[method](source, item1, item2);

      $('*[name="result"]', this).first().val(result);
    });

  });
});
