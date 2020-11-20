$('.like-btn').on('click',　function(event){
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
      $('#tweet-like-' + tweet_id).toggleClass('hide-heart');
      $('#tweet-not-like-' + tweet_id).toggleClass('hide-heart_blank');
      // resp.like_countでいいねの数を更新
      let like_count_id = 'tweet-like-count-' + tweet_id;
      let like_count_attrs = $('#' + like_count_id);
      let like_count_class = like_count_attrs.attr('class');
      let like_count_href = like_count_attrs.attr('href');
      like_count_attrs.html('<a id="' + like_count_id + '" class="' + like_count_class +
                            '" href="' + like_count_href + '">' + resp.like_count + '</a>');
  })
  .fail(function(resp, e){
          console.log(resp.responseText);
  })
});
