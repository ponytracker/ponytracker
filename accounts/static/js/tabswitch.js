/* This script switch the visible add form when we
 * change between user and group tab on team page. */
$('a[data-toggle="tab"]').on("show.bs.tab", function () {
  var tab = $(this).data('showtab');
  var hiddentab = $(this).data('hidetab');
  $('#add-' + hiddentab + '-form').addClass('hidden');
  $('#add-' + tab + '-form').removeClass('hidden');
});
