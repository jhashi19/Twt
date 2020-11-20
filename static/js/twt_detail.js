$('.like-btn').on('click',　function(event){
    event.preventDefault();
    let like = $(this);
    let comment_id = like.attr('value');
    $.ajax({
        url: like.attr('data-href'),
        type: 'POST',
        data:{
          'comment_id': comment_id
        },
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(resp){
        // toggleでhide-heartクラスの挿入・削除
        $('#comment-like-' + comment_id).toggleClass('hide-heart');
        $('#comment-not-like-' + comment_id).toggleClass('hide-heart_blank');
        // resp.like_countでいいねの数を更新
        let like_count_id = 'comment-like-count-' + comment_id;
        let like_count_attrs = $('#' + like_count_id);
        let like_count_class = like_count_attrs.attr('class');
        let like_count_href = like_count_attrs.attr('href');
        like_count_attrs.html('<a id="' + like_count_id + '" class="' + like_count_class +
                              '" href="' + like_count_href + '">' + resp.comment_like_count + '</a>');
    })
    .fail(function(resp, e){
            console.log(resp.responseText);
    })
});

$('.detail-like-btn').on('click',　function(event){
    event.preventDefault();
    let like = $(this);
    let tweet_id = like.attr('value');
    $.ajax({
        url: like.attr('data-href'),
        type: 'POST',
        data:{
          'tweet_id': tweet_id
        },
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(resp){
        // toggleでhide-heartクラスの挿入・削除
        $('#detail-like').toggleClass('hide-heart');
        $('#detail-not-like').toggleClass('hide-heart_blank');
        // resp.like_countでいいねの数を更新
        let like_count_id = 'tweet-detail-like';
        $('#' + like_count_id).html('<span id="' + like_count_id + '">'
            + resp.detail_like_count + '件のいいね！</span>')
    })
    .fail(function(e){
            // console.log(resp.responseText);
    })
});
