$(document).ready(function() {
  $('form').on('submit', function(event) {

    //Request to server with form data
    $.ajax({
        data: {
          collage_type: $('#collage_type').val(),
          time_frame: $('#time_frame').val(),
          size: $('#size').val()
        },
        type: 'POST',
        url: '/collage'
      })

      //Utilize data from request
      .done(function(data) {

        if (!data.hasOwnProperty('error')) {
          artwork = JSON.parse(data);
          var display_style = $('#display').val();
          var item;


          //Toggle the corresponding collage
          if ($('#size').val() == "4") {
            id = '#four';
            $('.three').hide();
            $('.four').show();
          } else {
            id = '#';
            $('.four').hide();
            $('.three').show();
          }

          //Reset styles/content of target elements
          $('.row').css('margin', '0 auto');
          $('.collage-list').empty();
          $('.display-text').show();

          //Generate collage
          for (item = 0; item < artwork.items.length; item++) {
            $(id + item.toString()).attr('src', artwork.items[item].url);
            $(id + item.toString()).next().text(artwork.items[item].name);
            $('.collage-list').append('<li>' + artwork.items[item].name + '</li>');
          }

          //All three options are on initially. Only keep the style from input
          if (display_style == 'overlay')
            $('.collage-list').hide();
          else if (display_style == 'default') {
            $('.display-text').hide();
            $('.collage-list').hide();
          } else {
            $('.display-text').hide();
            $('.collage-list').show();
            $('.row').css('margin-left', '500px');
          }
        }

        // Error from server
        else {
          $('.collage-list').empty();
          $('.three').hide();
          $('.four').hide();
          alert(data.error);
        }
      })
    event.preventDefault();
  });

  //Allow user to logout.
  $('.logout').click(function() {
    const url = 'https://www.spotify.com/logout/';
    const logout_window = window.open(url, 'Spotify Logout', 'width=500,height=500,top=40,left=40');
    setTimeout(function() {
      logout_window.close();
    }, 3000);
  });
});
