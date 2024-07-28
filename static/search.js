$(document).ready(function () {
    // Function to fetch and display search results for the first search input
    function fetchSearchResults(query) {
        // Check if the query is empty
        if (!query) {
            $('#search-results').empty();
            return;
        }

        // Make an AJAX request to your Django live_search view
        $.ajax({
            url: '/live_search/', // Update this URL to match your live_search view URL
            data: { 'q': query },
            dataType: 'json',
            success: function (data) {
                var resultsDiv = $('#search-results');
                resultsDiv.empty(); // Clear previous search results

                if (data.length > 0) {
                    $.each(data, function (index, item) {
                        // Construct the URL for the product details page
                        var url = '/product/' + item.p_link

                        // Display the search results with the constructed URL and combined name-type-size
                        resultsDiv.append('<li><a href="' + url + '">' + item.p_name + ' - ' + item.p_type + ' - ' + item.size + '</a></li>');
                    });
                } else {
                    resultsDiv.append('<p>No results found.</p>');
                }
            }
        });
    }

    $('#search-input').on('input', function () {
        var query = $(this).val();
        fetchSearchResults(query);
    });

    // Clear search results when clicking somewhere else on the page
    $(document).on('click', function (event) {
        var target = $(event.target);
        if (!target.is('#search-input') && !target.is('#search-results')) {
            $('#search-results').empty();
        }
    });
});

$(document).ready(function () {
    // Function to fetch and display search results for the second search input
    function fetchSearchResults(query) {
        // Check if the query is empty
        if (!query) {
            $('#search-results2').empty();
            return;
        }

        // Make an AJAX request to your Django live_search view
        $.ajax({
            url: '/live_search/', // Update this URL to match your live_search view URL
            data: { 'q': query },
            dataType: 'json',
            success: function (data) {
                var resultsDiv = $('#search-results2');
                resultsDiv.empty(); // Clear previous search results

                if (data.length > 0) {
                    $.each(data, function (index, item) {
                        // Construct the URL for the product details page
                        var url = '/product/' + item.p_link
                        // Display the search results with the constructed URL and combined name-type-size
                        resultsDiv.append('<li><a href="' + url + '">' + item.p_name + ' - ' + item.p_type + ' - ' + item.size + '</a></li>');
                    });
                } else {
                    resultsDiv.append('<p>No results found.</p>');
                }
            }
        });
    }

    $('#search-input2').on('input', function () {
        var query = $(this).val();
        fetchSearchResults(query);
    });

    // Clear search results when clicking somewhere else on the page
    $(document).on('click', function (event) {
        var target = $(event.target);
        if (!target.is('#search-input2') && !target.is('#search-results2')) {
            $('#search-results2').empty();
        }
    });
});

function searchresults() {
    var searchInput = document.getElementById('search-input').value;
    var resultsDiv = $('#search-results');

    // Check if the search input is empty
    if (!searchInput) {
        resultsDiv.empty();
        return;
    }

    // Make an AJAX request to your Django live_search view
    $.ajax({
        url: '/live_search/',
        data: { 'q': searchInput },
        dataType: 'json',
        success: function (data) {
            // Make a new AJAX request to pass the data to the searchresult view
            $.ajax({
                url: '/searchresult/',
                method: 'POST',
                data: { 'search_results': JSON.stringify(data) },
                success: function (response) {
                    // Replace the entire current page with the received HTML
                    document.documentElement.innerHTML = response;
                }
            });
        }
    });
}

function searchresults2() {
    var searchInput = document.getElementById('search-input2').value;
    var resultsDiv = $('#search-results2');

    // Check if the search input is empty
    if (!searchInput) {
        resultsDiv.empty();
        return;
    }

    // Make an AJAX request to your Django live_search view
    $.ajax({
        url: '/live_search/',
        data: { 'q': searchInput },
        dataType: 'json',
        success: function (data) {
            // Make a new AJAX request to pass the data to the searchresult view
            $.ajax({
                url: '/searchresult/',
                method: 'POST',
                data: { 'search_results': JSON.stringify(data) },
                success: function (response) {
                    // Replace the entire current page with the received HTML
                    document.documentElement.innerHTML = response;
                }
            });
        }
    });
}
