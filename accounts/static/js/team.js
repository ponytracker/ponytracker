/* This script switch the visible add form when we
 * change between user and group tab on team page. */
$('a[data-toggle="tab"]').on("show.bs.tab", function () {
  var tab = $(this).data('tab');
  var hiddentab;
  if (tab == 'user') {
    hiddentab = 'group';
  } else {
    hiddentab = 'user';
  }
  $('#add-' + hiddentab + '-form').addClass('hidden');
  $('#add-' + tab + '-form').removeClass('hidden');
});
