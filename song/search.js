const youtube = require('scrape-youtube').default;
// const youtube = require('scrape-youtube').default;
youtube.search(process.argv[2]).then(results => {
    // Unless you specify a type, it will only return 'video' results

    var i;
    var links = "";
    for (i = 0; i < 10; i++) {
      console.log(i, ": ", results.videos[i]["title"], "duration: ",results.videos[i]["duration"],  "seconds. \n views: ", results.videos[i]["views"], '\n');
      links = links.concat(results.videos[i]["link"],'\n');
    }

    fs = require('fs');
    fs.writeFile('links.txt', links, function (err) {
      if (err) return console.log("there was a fatal error");
      console.log('success!');
    });


  //  console.log(results.videos)

});
