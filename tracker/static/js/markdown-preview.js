var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

$('a[href="#preview"]').on("show.bs.tab", function (e) {
  $('#preview-content').html('Loading preview...');
  var project = $('#markdown-content').data('project');
  var comment = $('#markdown-content').val();
  $.post(markdown_preview_url, {'project': project, 'data': comment})
    .done(function(data, textStatus) {
      $('#preview-content').html(data);
    })
    .fail(function () {
      $('#preview-content').html('Sorry, an error occured.');
    });
})
