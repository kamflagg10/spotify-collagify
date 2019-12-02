$(document).ready(function(){
    $('form').on('submit', function(event){

        $.ajax({
            data : {
                collage_type: $('#collage_type').val(),
                time_frame: $('#time_frame').val(),
                size: $('#size').val()
            },
            type: 'POST',
            url: '/collage'
        })

        .done(function(data) {
        if (!data.hasOwnProperty('error')){
          artwork = JSON.parse(data);
          var item;
          if ($('#size').val() == "4"){
            id = '#four';
            $('.three').hide();
            $('.four').show();
           }
          else{
            id = '#';
            $('.four').hide();
            $('.three').show();
          }
          $('.collage-list').empty();
          for (item=0; item < artwork.items.length; item++){
             id += item.toString();
             $(id).attr('src', artwork.items[item].url);
             $(id).next().text(artwork.items[item].name)
            }
        }
        else{
          $('.collage-list').empty();
          $('.three').hide();
          $('.four').hide();
          alert(data.error)
        }

        })

        event.preventDefault();

    });
});



//$('.collage-list').append('<li>' + artwork.items[item].name + '</li>');