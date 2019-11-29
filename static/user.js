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
          var four_id;
          if ($('#size').val() == "4"){
            for (item=0; item < artwork.items.length; item++){
             id = '#four' + item.toString();
             $(id).attr('src', artwork.items[item].url);
             console.log(artwork.items[item].url);
            }
            $('.four').toggle();

          }
          for (item=0; item < artwork.items.length; item++){
             id = '#' + item.toString();
             $(id).attr('src', artwork.items[item].url);
             console.log(artwork.items[item].url);
           }
          $('.three').toggle();
        }
        else{
          alert(data.error)
        }

        })

        event.preventDefault();

    });
});