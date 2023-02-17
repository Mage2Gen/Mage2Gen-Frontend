function startIntro(){
	Cookies.set("intro", 'true', { expires: 7 });

	var intro = introJs();
	intro.setOptions({
		steps: [
			{
				element: 'section.panel:first-child',
				intro: "Start building your first Magento 2 module here by giving it a vendor name and a module name.",
				position: 'bottom-right-aligned'
			},
			{
				element: '#code-navigation',
				intro: "Your code gets generated real time when editing fields. Click on one of the files to open the file and view the generated code!",
				position: 'bottom-right-aligned'
			},
			{
				element: '#introjs-login',
				intro: "<b>Create an account</b> and benefit from even <b>more awesome features</b> like: <br/> <br/> <ul><li>Save your modules to continue your work another time!</li><li>Add custom copyright licenses to your modules</li></ul>",
				position: 'bottom-right-aligned'
			},

		],
		//showButtons: false,
		showBullets: false,
		showProgress: false,
		showStepNumbers: false,
		showProgress: true,
		doneLabel: "Got it!"
	});

	intro.start();
}

jQuery(window).on('load', function(){
	if(Cookies.get("intro") != 'true') {
		startIntro();
	} else {
		return;
	}
})