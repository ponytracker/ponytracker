$('#confirm-delete').on('show.bs.modal', function(e) {
    var item = $(e.relatedTarget).data('item');
    if (!item) {
        item = 'item';
    }
    $('#confirm-delete-form').attr('action', $(e.relatedTarget).data('action'));
    $('#confirm-delete-title').html('Delete ' + item);
    $('#confirm-delete-message').html('Are you sure to delete this ' + item + '?');
});
