var lunr = require('lunr')
var fs = require('fs');
var data;
var source = process.argv.slice(2)[0];
var destination = process.argv.slice(2)[1];
var regex = temp = /[^`~!@#$%^&*()-=+\|/?.>,<;:'"[{]}]+/g

buildIndex(source, destination);

function buildIndex(source, destination) {
  fs.readFile(source, 'utf8', function(err, data) {
      if (err) throw err;
      documents = JSON.parse(data.replace(regex, ''));

      var idx = lunr(function() {
          this.ref('href')
          this.field('title')
          this.field('text')
          this.metadataWhitelist = ['position']

          for (doc in documents) {
              this.add(documents[doc])
          }
      })

      fs.writeFile(destination, JSON.stringify(idx), function(err) {
          if (err) throw err;
          console.log('New index file created at '+destination);
      });

  });

}
