jQuery(document).ready(function($) {

    var resultsData = [];

    function getFrontendBadge(rank) {
        if (!rank || rank <= 0 || isNaN(rank)) {
            return '<span class="wprt-badge-f wprt-badge-f-unranked">-</span>';
        }
        var r = parseInt(rank, 10);
        var cls = 'wprt-badge-f-top100';
        if (r <= 3) cls = 'wprt-badge-f-top3';
        else if (r <= 10) cls = 'wprt-badge-f-top10';
        else if (r <= 20) cls = 'wprt-badge-f-top20';
        else if (r <= 50) cls = 'wprt-badge-f-top50';
        return '<span class="wprt-badge-f ' + cls + '">' + r + '</span>';
    }

    $('#wprt-front-form').on('submit', function(e) {
        e.preventDefault();

        var domain = $('#wprt_front_domain').val().trim();
        var region = $('#wprt_front_region').val();
        var rawKws = $('#wprt_front_keywords').val().trim();
        var maxKws = parseInt($('.wprt-front-container').data('max-keywords'), 10) || 15;

        if (!domain) {
            alert('Please enter a target website domain.');
            return;
        }

        if (!rawKws) {
            alert('Please enter at least one keyword.');
            return;
        }

        var lines = rawKws.split(/[\r\n,]+/);
        var keywords = [];
        for (var i = 0; i < lines.length; i++) {
            var k = lines[i].trim();
            if (k && keywords.indexOf(k) === -1) {
                keywords.push(k);
            }
        }

        if (keywords.length === 0) {
            alert('Please enter valid keywords.');
            return;
        }

        if (keywords.length > maxKws) {
            alert('You can check up to ' + maxKws + ' keywords at once. Checking the first ' + maxKws + ' keywords.');
            keywords = keywords.slice(0, maxKws);
        }

        // Reset UI
        resultsData = [];
        var total = keywords.length;
        var completed = 0;
        var top3Count = 0;
        var top10Count = 0;
        var unrankedCount = 0;

        var $btn = $('#wprt-front-submit');
        $btn.prop('disabled', true).text('Checking Rankings...');
        $('#wprt-front-progress-box').show();
        $('#wprt-front-progress-bar').css('width', '0%');
        $('#wprt-front-progress-status').text('Checking 0 of ' + total + ' keywords...');

        $('#wprt-front-results-box').show();
        var $tbody = $('#wprt-front-results-body');
        $tbody.empty();

        // Build initial placeholder rows
        for (var j = 0; j < total; j++) {
            var rowHtml = '<tr id="wprt-f-row-' + j + '">' +
                '<td style="text-align: center; color: #718096;">' + (j + 1) + '</td>' +
                '<td style="font-weight: 600;">' + $('<div>').text(keywords[j]).html() + '</td>' +
                '<td style="text-align: center;" class="f-col-rank"><span style="color: #a0aec0;">Waiting...</span></td>' +
                '<td class="f-col-url"><span style="color: #a0aec0;">-</span></td>' +
                '</tr>';
            $tbody.append(rowHtml);
        }

        // Process queue
        var queueIndex = 0;

        function processNext() {
            if (queueIndex >= total) {
                $btn.prop('disabled', false).text('▶ Check Google Rankings');
                $('#wprt-front-progress-status').text('All ' + total + ' keywords checked!');
                return;
            }

            var currentIdx = queueIndex;
            var currentKw = keywords[currentIdx];
            var $row = $('#wprt-f-row-' + currentIdx);
            $row.find('.f-col-rank').html('<span style="color: #3182ce;">Scanning...</span>');

            $.ajax({
                url: wprtFrontData.ajax_url,
                type: 'POST',
                data: {
                    action: 'wprt_frontend_check',
                    nonce: wprtFrontData.nonce,
                    keyword: currentKw,
                    domain: domain,
                    region: region
                },
                success: function(resp) {
                    completed++;
                    var pct = Math.round((completed / total) * 100);
                    $('#wprt-front-progress-bar').css('width', pct + '%');
                    $('#wprt-front-progress-status').text('Checked ' + completed + ' of ' + total + ' (' + pct + '%)...');

                    var rankVal = null;
                    var urlVal = 'Not ranked in Top 100';

                    if (resp.success && resp.data) {
                        rankVal = resp.data.rank;
                        urlVal = resp.data.url;
                    }

                    resultsData.push({
                        id: currentIdx + 1,
                        keyword: currentKw,
                        rank: rankVal ? rankVal : 'Not ranked',
                        url: urlVal
                    });

                    // Update Row
                    var badge = getFrontendBadge(rankVal);
                    $row.find('.f-col-rank').html(badge);

                    if (rankVal && urlVal && urlVal.indexOf('http') === 0) {
                        $row.find('.f-col-url').html('<a href="' + urlVal + '" target="_blank" class="wprt-url-link" title="' + urlVal + '">' + urlVal + '</a>');
                        if (rankVal <= 3) top3Count++;
                        if (rankVal <= 10) top10Count++;
                    } else {
                        $row.find('.f-col-url').html('<span style="color: #a0aec0;">Not ranked</span>');
                        unrankedCount++;
                    }

                    // Update summary chips
                    $('#wprt-stat-total').text(completed);
                    $('#wprt-stat-top3').text(top3Count);
                    $('#wprt-stat-top10').text(top10Count);
                    $('#wprt-stat-unranked').text(unrankedCount);

                    queueIndex++;
                    setTimeout(processNext, 200);
                },
                error: function() {
                    completed++;
                    $row.find('.f-col-rank').html('<span style="color: #e53e3e;">Failed</span>');
                    $row.find('.f-col-url').html('<span style="color: #e53e3e;">Error</span>');
                    unrankedCount++;
                    queueIndex++;
                    setTimeout(processNext, 200);
                }
            });
        }

        processNext();
    });

    // Client-side CSV Download
    $('#wprt-front-export-btn').on('click', function(e) {
        e.preventDefault();
        if (resultsData.length === 0) {
            alert('No results available to download.');
            return;
        }

        var csvContent = "data:text/csv;charset=utf-8,";
        csvContent += "#,Keyword,Google Rank,Ranked Landing Page URL\n";

        for (var i = 0; i < resultsData.length; i++) {
            var item = resultsData[i];
            var row = [
                item.id,
                '"' + item.keyword.replace(/"/g, '""') + '"',
                '"' + item.rank + '"',
                '"' + item.url.replace(/"/g, '""') + '"'
            ].join(",");
            csvContent += row + "\n";
        }

        var encodedUri = encodeURI(csvContent);
        var link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "google_rankings_" + (new Date().toISOString().slice(0, 10)) + ".csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

});
