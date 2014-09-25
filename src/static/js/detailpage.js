$(function() {
  $('.fotorama').fotorama({
    nav: 'thumbs',
    thumbheight: '60px',
    transition: 'dissolve',
    arrows: true,
    fit: 'cover',
    allowfullscreen: false
  });

  $('.request-send a.action-send').on('click', function(){
    $('.request-send').hide();
    $('.request-send-approve').show();
  });

  $('.request-send-approve a.action-send').on('click', function(){
    var trip_id = $(this).data('tripid'),
        allow_post_fb = $('#post_to_fb_checkox').prop('checked');

    $.ajax({
      type: "POST",
      url: "/api/triprequest/"+trip_id+"/",
      data: JSON.stringify({ "allow_post_fb": allow_post_fb }),
      dataType: "json",
      contentType: "application/json; charset=utf-8",
      success: function(data) {
        $('.request-block').html(data.html);
      },
      error: function(data) {
        console.log('Error',data);
      }
    });
  })
});