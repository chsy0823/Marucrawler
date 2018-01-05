var casper = require('casper').create({
	pageSettings: {
		loadImages: false,//The script is much faster when this field is set to false
		loadPlugins: false,
		webSecurityEnabled: false,
		resourceTimeout: 60000,
		userAgent: 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
	}
});
var fs = require('fs');
//var request = require('request');
var links = [];
var selectLink = [];
var downloadPath = "/Users/Elen/Documents/book/comic/";
var link = casper.cli.args[0]
var downloadImg = function(uri, filename, callback){
//	request.head(uri, function(err, res, body){
//		//console.log('content-type:', res.headers['content-type']);
//		//console.log('content-length:', res.headers['content-length']);
//
//		request(uri).pipe(fs.createWriteStream(filename)).on('close', callback);
//	});
};

casper.start(link, function() {
	this.echo(this.getTitle());
});

casper.then(function() {
	// aggregate results for the 'casperjs' search
	//links = this.evaluate(getLinks);
	
	var vContent = this.getElementsInfo('#vContent a');
	for (var i = 0; i < vContent.length; i++) 
		links[i] = {"name":vContent[i].html,"href":vContent[i].attributes.href};
			
	this.echo(links.length + ' links found:');
	for(var index in links) {
		var link = links[index].href;
		var name = links[index].name;
		
		if(link !== undefined && link != "") {
			if(link.indexOf("archives") > -1) {
				name = name.split("<i style")[0];
				links[index].name = name;
				selectLink.push(links[index]);
				this.echo(name + " - " + link);
			}
		}
	}
});

casper.then(function() {
	casper.page.settings.loadImages = true;
	casper.start().each(selectLink, function(self, item) {
		self.thenOpen(item.href, function() {
		    
		    if (casper.exists("#gallery_vertical"))
		    {
				var path = downloadPath+""+item.name;
				if(fs.makeDirectory(path)) {
					
					casper.waitForSelector("#gallery_vertical", function() {
						this.echo("\nStart download -"+item.name+"\n");
						var hostUrl = this.getCurrentUrl();
				    	var imgInfo = casper.getElementsInfo('#gallery_vertical img');
						for (var i = 0; i < imgInfo.length; i++) {
							var downloadUrl = "http://wasabisyrup.com"+imgInfo[i].attributes["data-src"];
							this.download(downloadUrl, path+"/"+i+".jpg", 'get');
							//casper.echo("download url = " + downloadUrl);
							if(fs.isFile(path+"/"+i+".jpg") && fs.size(path+"/"+i+".jpg") <= 0) {
								i--;
							}
						}
						this.echo("\end download -"+item.name+"\n");
					});
				}
				else
					this.echo('cannot create folder');	
	        }
			else {
				this.echo(this.getTitle());
				this.echo(casper.getPageContent());
			}
	    });
    });	
});

casper.run();
