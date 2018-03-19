var lunr = require('lunr')
var fs = require('fs');
var data;

var fs = require('fs');

buildIndex();

function buildIndex() {
  fs.readFile('_site/search-data.json', 'utf8', function(err, data) {
      if (err) throw err;
      documents = JSON.parse(data);

      var idx = lunr(function() {
          this.ref('href')
          this.field('title')
          this.field('text')

          for (doc in documents) {
              this.add(documents[doc])
          }
      })

      fs.writeFile('_site/search-index.json', JSON.stringify(idx), (err) => {
          if (err) throw err;
          console.log('New index file created.');
      });

  });

}
