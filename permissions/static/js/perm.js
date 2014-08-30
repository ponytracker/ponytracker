$('.perm-toggle').click(function() {
  var a = $(this);
  a.html('<span class="glyphicon glyphicon-time"></span>');
  var href = a.data('href');
  $.ajax(href)
    .done(function(data, textStatus) {
      if (data == '1') {
        a.html('<span class="glyphicon glyphicon-ok"></span>');
      } else {
        a.html('<span class="glyphicon glyphicon-remove"></span>');
      }
    });
});
