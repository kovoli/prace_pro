$('.like').on('click', function(like) {
        like.preventDefault();
        var $this = $(this),
            data = $this.data();

        $.ajax({
            url: "/like_dislike/like/",
            method: 'POST',
            data: data,
            success: function(data) {
                    $(".counter_like_deal_" + data['id']).text(data['comment'])
            },
            error: function(d) {
                console.log(d);
            }
        });
    });

    $('.dislike').on('click', function(dislike) {
        dislike.preventDefault();
        var $this = $(this),
            data = $this.data();

        $.ajax({
            url: "/like_comment/dislike/",
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