$(document).ready(function() {
    // CSRF code
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('.like_comment').on('click', function(e) {
        e.preventDefault();
        var $this = $(this),
            data = $this.data();

        $.ajax({
            url: "/like_comment/",
            method: 'POST',
            data: data,
            success: function(data) {
                    $(".counter_like_" + data['id']).text(data['comment'])
            },
            error: function(d) {
                console.log(d);
            }
        });
    });

    $('.like').on('click', function() {
        var $this = $(this),
            data = $this.data();

        $.ajax({
            url: "/like_dislike/like/",
            method: 'POST',
            data: data,
            success: function(data) {
                var deal_counter = data['deal_counter'];
                var counter_multiple = deal_counter * 10;
                var session_id = data['session_data'];
                var id_deal = data['id'];
                    $(".counter_like_deal_" + data['id']).text(deal_counter);
                    $("#progress-bar-" + data['id']).attr('aria-valuenow', deal_counter);
                    $("#progress-bar-" + data['id']).css('width', counter_multiple + '%');
                    if (session_id[id_deal] === 'like') {
                        $(".btn-like-" + id_deal ).attr('disabled', true);
                    };

                    console.log(session_id[id_deal])
            },
            error: function(d) {
                console.log(d);
            }
        });
    });

    $('.dislike').on('click', function() {
        var $this = $(this),
            data = $this.data();

        $.ajax({
            url: "/like_dislike/dislike/",
            method: 'POST',
            data: data,
            success: function(data) {
                var deal_counter = data['deal_counter'];
                var counter_multiple = deal_counter * 10;
                var session_id = data['session_data'];
                var id_deal = data['id'].toString();
                $(".counter_like_deal_" + data['id']).text(deal_counter);
                $("#progress-bar-" + data['id']).attr('aria-valuenow', deal_counter);
                $("#progress-bar-" + data['id']).css('width', counter_multiple + '%');
                if (session_id[id_deal] === 'like') {
                        $(".btn-like-" + id_deal ).attr('disabled', true);
                };
            },
            error: function(d) {
                console.log(d);
            }
        });
    });

    $('.sidebar-slider').slick({
        vertical: true,
        infinite: true,
        slidesToShow: 5,
        slidesToScroll: 1,
        verticalSwiping: true,
        prevArrow: $('.prev_arrow'),
        nextArrow: $('.next_arrow')
  }).on('wheel', (function(e) {
      e.preventDefault();

      if (e.originalEvent.deltaY < 0) {
        $(this).slick('slickNext');
      } else {
        $(this).slick('slickPrev');
      }
    }));

});