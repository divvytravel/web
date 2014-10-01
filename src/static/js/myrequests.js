$(function() {
  var detail_block = $('#detail_trip_page');

  detail_block.on('click', 'a.approve-request', function(){
    var triprequest_id = $(this).data('triprequest'),
        approve_link = $(this);

    $.ajax({
      type: "POST",
      url: "/api/triprequest/"+triprequest_id+"/approve/",
      dataType: "json",
      contentType: "application/json; charset=utf-8",
      success: function(data) {
        approve_link.hide();
      },
      error: function(data) {
        console.log('Error', data);
      }
    });
  });
});