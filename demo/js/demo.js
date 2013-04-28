require(["jquery", "../../lib/main"], function($) {
  $(function() {

    $('#demo-form-sim').submit(function (e) {
      e.preventDefault();

      var source = JSON.parse( $('*[name="source"]', this).first().val() ) || '';
      var method = $('*[name="method"]:checked', this).val();

      var recommendations = new Recommendations();

      // データはひとまず中から持ってきている
      var result = recommendations[method](source, 'Lisa Rose', 'Gene Seymour');

      $('*[name="result"]', this).first().val(result);
    });

  });
});
