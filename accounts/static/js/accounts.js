/* This script is used to remove user from group,
 * user from team or group from team dynamically
 * with a ajax request. */
$('a[role="remove"]').on("click", function () {
  var a = $(this);
  var href = a.data('href');
  var type = a.data('type');
  a.html('removing...');
  $.ajax(href)
    .done(function(data, textStatus) {
      a.parents('li').remove();
      var counter = $('#' + type + '-counter');
      var empty = $('#' + type + '-empty');
      var count = parseInt(counter.html());
      count--;
      counter.html(count);
      if (count < 0) {
        // should not happen
        window.location.reload();
      } else if (count == 0) {
        empty.removeClass('hidden');
      } else {
        empty.addClass('hidden');
      }
    })  
    .fail(function () {
      window.location.reload();
    }); 
});
