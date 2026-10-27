jQuery(document).ready(function($) {

    function getRankBadge(rank) {
        if (!rank || rank <= 0 || isNaN(rank)) {
            return '<span class="wprt-badge wprt-badge-unranked">-</span>';
        }
        var r = parseInt(rank, 10);
        var cls = 'wprt-badge-top100';
        if (r <= 3) cls = 'wprt-badge-top3';
        else if (r <= 10) cls = 'wprt-badge-top10';
        else if (r <= 20) cls = 'wprt-badge-top20';
        else if (r <= 50) cls = 'wprt-badge-top50';
        return '<span class="wprt-badge ' + cls + '">' + r + '</span>';
    }

    function getRankChange(current, previous) {
        if (!current || current <= 0) return '';
        if (!previous || previous <= 0) return '<span class="wprt-change-up">NEW</span>';
        var diff = previous - current;
        if (diff > 0) return '<span class="wprt-change-up">▲ +' + diff + '</span>';
        if (diff < 0) return '<span class="wprt-change-down">▼ ' + diff + '</span>';
        return '<span class="wprt-change-same">— 0</span>';
    }

    // Check Single Keyword
    $(document).on('click', '.wprt-btn-check-single', function(e) {
        e.preventDefault();
        var $btn = $(this);
        var kwId = $btn.data('id');
        var $row = $('#wprt-row-' + kwId);

        $btn.prop('disabled', true).text('Checking...');
        $row.find('.wprt-col-rank').html('<span class="spinner is-active" style="float:none;"></span>');

        $.ajax({
            url: wprtData.ajax_url,
            type: 'POST',
            data: {
                action: 'wprt_check_single_rank',
                nonce: wprtData.nonce,
                keyword_id: kwId
            },
            success: function(resp) {
                $btn.prop('disabled', false).text('Check');
                if (resp.success) {
                    var data = resp.data;
                    var badge = getRankBadge(data.current_rank);
                    var change = getRankChange(data.current_rank, data.previous_rank);
                    $row.find('.wprt-col-rank').html(badge + ' ' + change);

                    if (data.ranked_url && data.current_rank) {
                        $row.find('.wprt-col-url').html('<a href="' + data.ranked_url + '" target="_blank" class="wprt-url" title="' + data.ranked_url + '">' + data.ranked_url + '</a>');
                    } else {
                        $row.find('.wprt-col-url').html('<span style="color:#8c8f94;">Not ranked</span>');
                    }
                    $row.find('.wprt-col-date').text(data.last_checked);
                } else {
                    $row.find('.wprt-col-rank').html('<span style="color:red;">Error</span>');
                    alert('Error checking rank: ' + (resp.data || 'Unknown error'));
                }
            },
            error: function() {
                $btn.prop('disabled', false).text('Check');
                $row.find('.wprt-col-rank').html('<span style="color:red;">Failed</span>');
            }
        });
    });

    // Delete Keyword
    $(document).on('click', '.wprt-btn-delete', function(e) {
        e.preventDefault();
        if (!confirm('Are you sure you want to delete this keyword?')) return;

        var $btn = $(this);
        var kwId = $btn.data('id');
        var $row = $('#wprt-row-' + kwId);

        $.ajax({
            url: wprtData.ajax_url,
            type: 'POST',
            data: {
                action: 'wprt_delete_keyword',
                nonce: wprtData.nonce,
                keyword_id: kwId
            },
            success: function(resp) {
                if (resp.success) {
                    $row.fadeOut(300, function() { $(this).remove(); });
                } else {
                    alert('Error deleting keyword: ' + resp.data);
                }
            }
        });
    });

    // Bulk Check All Rankings
    $('#wprt-btn-check-all').on('click', function(e) {
        e.preventDefault();
        var $rows = $('.wprt-keyword-row');
        if ($rows.length === 0) {
            alert('No keywords found to check.');
            return;
        }

        var total = $rows.length;
        var completed = 0;
        var $btn = $(this);

        $btn.prop('disabled', true).text('Checking All Keywords...');
        $('#wprt-progress-container').show();
        $('#wprt-progress-bar').css('width', '0%');
        $('#wprt-progress-text').text('Scanning 0 / ' + total + ' keywords...');

        var queue = [];
        $rows.each(function() {
            queue.push($(this).data('id'));
        });

        function processNext() {
            if (queue.length === 0) {
                $btn.prop('disabled', false).text('▶ Check All Rankings Now');
                $('#wprt-progress-text').text('Scan completed! ' + total + ' keywords checked.');
                setTimeout(function() { location.reload(); }, 1200);
                return;
            }

            var currentId = queue.shift();
            var $row = $('#wprt-row-' + currentId);
            $row.find('.wprt-col-rank').html('<span class="spinner is-active" style="float:none;"></span>');

            $.ajax({
                url: wprtData.ajax_url,
                type: 'POST',
                data: {
                    action: 'wprt_check_single_rank',
                    nonce: wprtData.nonce,
                    keyword_id: currentId
                },
                success: function(resp) {
                    completed++;
                    var pct = Math.round((completed / total) * 100);
                    $('#wprt-progress-bar').css('width', pct + '%');
                    $('#wprt-progress-text').text('Scanning ' + completed + ' / ' + total + ' (' + pct + '%)...');

                    if (resp.success) {
                        var data = resp.data;
                        var badge = getRankBadge(data.current_rank);
                        var change = getRankChange(data.current_rank, data.previous_rank);
                        $row.find('.wprt-col-rank').html(badge + ' ' + change);

                        if (data.ranked_url && data.current_rank) {
                            $row.find('.wprt-col-url').html('<a href="' + data.ranked_url + '" target="_blank" class="wprt-url" title="' + data.ranked_url + '">' + data.ranked_url + '</a>');
                        } else {
                            $row.find('.wprt-col-url').html('<span style="color:#8c8f94;">Not ranked</span>');
                        }
                        $row.find('.wprt-col-date').text(data.last_checked);
                    }
                    setTimeout(processNext, 250); // slight delay to respect rate limits
                },
                error: function() {
                    completed++;
                    processNext();
                }
            });
        }

        processNext();
    });

});
