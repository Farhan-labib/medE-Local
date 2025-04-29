$(document).ready(function () {
    function fetchSearchResults(query, inputId, resultsId) {
        if (!query) {
            $(resultsId).empty();
            return;
        }

        $.ajax({
            url: '/live_search/',
            data: { q: query },
            dataType: 'json',
            success: function (data) {
                const resultsDiv = $(resultsId);
                resultsDiv.empty();

                if (data.length > 0) {
                    $.each(data, function (_, item) {
                        const url = '/product/' + item.p_link;
                        resultsDiv.append('<li><a href="' + url + '">' + item.p_name + ' - ' + item.p_type + ' - ' + item.size + '</a></li>');
                    });
                } else {
                    resultsDiv.append('<p>No results found.</p>');
                }
            }
        });
    }

    $('#search-input').on('input', function () {
        fetchSearchResults($(this).val(), '#search-input', '#search-results');
    });

    $('#search-input2').on('input', function () {
        fetchSearchResults($(this).val(), '#search-input2', '#search-results2');
    });

    $(document).on('click', function (event) {
        const target = $(event.target);
        if (!target.is('#search-input') && !target.is('#search-results')) {
            $('#search-results').empty();
        }
        if (!target.is('#search-input2') && !target.is('#search-results2')) {
            $('#search-results2').empty();
        }
    });
});

function searchresults() {
    const searchInput = $('#search-input').val();
    const resultsDiv = $('#search-results');

    if (!searchInput) {
        resultsDiv.empty();
        return;
    }

    $.ajax({
        url: '/live_search/',
        data: { q: searchInput },
        dataType: 'json',
        success: function (data) {
            $.ajax({
                url: '/searchresult/',
                method: 'POST',
                data: { search_results: JSON.stringify(data) },
                success: function (response) {
                    document.documentElement.innerHTML = response;
                }
            });
        }
    });
}

function searchresults2() {
    const searchInput = $('#search-input2').val();
    const resultsDiv = $('#search-results2');

    if (!searchInput) {
        resultsDiv.empty();
        return;
    }

    $.ajax({
        url: '/live_search/',
        data: { q: searchInput },
        dataType: 'json',
        success: function (data) {
            $.ajax({
                url: '/searchresult/',
                method: 'POST',
                data: { search_results: JSON.stringify(data) },
                success: function (response) {
                    document.documentElement.innerHTML = response;
                }
            });
        }
    });
}
