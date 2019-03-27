// Returns a string trimmed to the last instance of a character
function trimBeforeLast(string, character) {
  return string.substr(0, Math.min(string.length, string.lastIndexOf(character)+1))
}

// Returns a string trimmed after the first instance of a character
function trimAfterFirst(string, character) {
  return string.substr(Math.min(string.length, string.indexOf(character)+1), string.length)
}

function displaySearchResults(results, query) {
  $('#results').empty().hide();
  if (results.length) { // Are there any results?
    var appendString = '<table class="table table-striped"><tbody>'
    var url = document.URL, basePath=url.substring(0,url.lastIndexOf("/"));

    $.getJSON(basePath+"/search-data.json", function(documents){
      results.forEach(function (r) {  // Iterate over the results

        var snippets = []

        Object.keys(r.matchData.metadata).forEach(function (term) {
          Object.keys(r.matchData.metadata[term]).forEach(function (fieldName) {
            var positions = r.matchData.metadata[term][fieldName].position
            positions.forEach(function (pos) {
              var snippet = documents[r.ref].text.slice(pos[0]-50, pos[0]+pos[1]+50)
              var wordTrim = trimAfterFirst(trimBeforeLast(snippet, ' '), ' ')
              snippets.push('...'+wordTrim+'...')
              })
            })
          })

        var results = '<div class="results ml-4 mr-4"><h6>Results</h6><small><p class="snippets">'+snippets.join('<br/>')+'</p></small></div>'

        let item = documents[r.ref];
        var text = trimBeforeLast(item.text.substr(0, 400), '.')

        appendString += '<tr><td><p class="lead mb-1"><a href="'+item.url+'">'+item.title+'</a></p><p>'+text+'</p>'+results+'</td></tr>';
      })
      appendString += '</tbody></table>'
      $('#results').append(appendString);
    });
  }
  $('#results').prepend('<p><span class="badge badge-secondary">'+results.length+'</span> result(s) for <span class="badge badge-secondary">'+query+'</span></p>').fadeIn(200, function(){
    $(".snippets").unmark({
      done: function() {
        $(".snippets").mark(searchTerm);
      }
    });
  });
}

function getQueryVariable(variable) {
  let query = window.location.search.substring(1);
  let vars = query.split('&');

  for (var i = 0; i < vars.length; i++) {
    let pair = vars[i].split('=');

    if (pair[0] === variable) {
      return decodeURIComponent(pair[1].replace(/\+/g, '%20'));
    }
  }
}

let searchTerm = getQueryVariable('q');
let searchType = $('form').attr('action').substring(1);

if (searchTerm) {
  $('#results').empty().append('<img class="mx-auto d-block" src="/img/loading.gif" />')
  $('#query').attr("value", searchTerm);

  ga('send', 'event', 'search', 'search', searchTerm);

  var url = document.URL, basePath=url.substring(0,url.lastIndexOf("/"));

  $.getJSON(basePath+"/search-index.json", function(data){
    let index = lunr.Index.load(data)

    let results = index.search(searchTerm); // Get lunr to perform a search
    displaySearchResults(results, searchTerm);

  });

}
