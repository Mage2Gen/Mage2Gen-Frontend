function clickTitleForToggle(panel){
	$($(panel).parent().find('.panel-collapse')[0]).collapse('toggle');
}

function ModuleRenderer(templates, container, snippets, config, copyright, mainVersion) {
    var self = this;
	self.templates = templates;
	self.mainVersion = mainVersion;
    self.custom_renderers = 'custom_renderers' in config ? config['custom_renderers'] : {};
    self.container = $(container);
    self.snippets = snippets;
    self.renderers = [];
    self.packageField = new FieldRenderer(templates, 'module', {
    	label: 'Type',
    	name: 'Package',
    	description: '',
    	required: true,
    	regex_validator:'^[a-zA-Z]{1}[a-zA-Z0-9]+$',
    	error_message: 'Only alphanumeric characters are allowed, and need to start with a alphabetic character.',
    	}, 0, 'col-md-6', 'col-md-6');
    self.packageField = new FieldRenderer(templates, 'module', {
    	label: 'Vendor name',
    	name: 'Package', 
    	description: '',
    	required: true, 
    	regex_validator:'^[a-zA-Z]{1}[a-zA-Z0-9]+$',
    	error_message: 'Only alphanumeric characters are allowed, and need to start with a alphabetic character.',
    	}, 0, 'col-md-6', 'col-md-6');
    self.nameField = new FieldRenderer(templates, 'module', {
    	label: 'Module name',
    	name: 'Name',
    	description: '', 
    	required: true,
    	regex_validator:'^[a-zA-Z]{1}[a-zA-Z0-9]+$',
    	error_message: 'Only alphanumeric characters are allowed, and need to start with a alphabetic character.',
    	}, 0, 'col-md-6', 'col-md-6');
	self.licenseField = new FieldRenderer(templates, 'module', {
    	label: 'License',
    	name: 'license',
    	description: '',
    	required: false,
    	choises: [
    		['no', 'No License'],
    		['gplv3', 'GPL V3'],
    		['oslv3', 'OSL V3'],
    		['apache2', 'Apache 2.0'],
    		['mit', 'MIT'],
    		['custom', 'Custom (Edit on account page, default to GPL V3)'],
    	],
    	default: 'gplv3'
    	}, 0, 'col-md-6', 'col-md-6');
	self.copyrightField = new FieldRenderer(templates, 'module', {
    	label: 'Copyright',
    	name: 'copyright',
    	description: '', 
    	required: true,
    	}, 0, 'col-md-6', 'col-md-6');
    self.descriptionField = new FieldRenderer(templates, 'module', {
    	label: 'Description', 
    	name: 'description',
    	description: '', 
    	required: true
    }, 0, 'col-md-12', 'col-md-12');

    self.packageField.change(function(){
		if(typeof self.change_callback !== 'undefined'){
			self.change_callback();
		}
	})
	self.nameField.change(function(){
		if(typeof self.change_callback !== 'undefined'){
			self.change_callback();
		}
	})
	self.descriptionField.change(function(){
		if(typeof self.change_callback !== 'undefined'){
			self.change_callback();
		}
	})
	self.licenseField.change(function(){
		if(typeof self.change_callback !== 'undefined'){
			self.change_callback();
		}
	})
	self.copyrightField.change(function(){
		if(typeof self.change_callback !== 'undefined'){
			self.change_callback();
		}
	})

    self.render();

    module_config = 'module_config' in config ? config['module_config'] : null;
    if(module_config != null){
    	self.setData(module_config);
    }
};

ModuleRenderer.prototype.render = function(){
	var self = this;
	self.container.html('');
	

	/* Add general block */
	self.generalBlock = $('<section class="panel panel-primary">');
    
    self.generalBlock.append($('<div class="panel-heading">').append($('<h4 class="panel-title">').text('General')))

    self.generalBlock.append($('<div class="panel-body">')
    	.append(self.packageField.renderField())
    	.append(self.nameField.renderField())
    	.append(self.licenseField.renderField())
    	.append(self.copyrightField.renderField())
    	.append(self.descriptionField.renderField()))

   	self.container.append(self.generalBlock);

   	/* Add search bar */
   	var searchInput = $('.search-query');
   	searchInput.keyup(function() {
		self.search($(searchInput).val());
	});

   	searchButton = $('btn.search');
   	searchButton.click(function(){
   		self.search($(searchInput).val());
   	});

   	/* Add filter bar */
   	filterButton = $('btn.filter');
   	filterButton.click(function(){
   		console.log('Click');
   		self.filter();
   	});


   	self.renderers = [];
    $(self.snippets).each(function(index, snippet){
    	if(snippet['name'] in self.custom_renderers){
    		renderer = new self.custom_renderers[snippet['name']](self.templates, snippet);
    	} else {
    		renderer = new DefaultSnippetRenderer(self.templates, snippet);
    	}

    	renderer.change(function(){
			if(typeof self.change_callback !== 'undefined'){
				self.change_callback();
			}
		})
    	
    	self.renderers.push(renderer);
    	result = renderer.renderContainer();
    	self.container.append(result);
    });
}

ModuleRenderer.prototype.search = function(search){
	$(this.renderers).each(function(index, renderer){
		renderer.search(search);
	});
}

ModuleRenderer.prototype.filter = function(filter){
	$(this.renderers).each(function(index, renderer){
		renderer.filter(filter);
	});
}


ModuleRenderer.prototype.validate = function(display_error){
	display_error = typeof display_error !== 'undefined' ? display_error : true;
	var self = this;
	var valid = true;

	valid = self.packageField.validate(display_error) && valid;
	valid = self.nameField.validate(display_error) && valid;
	valid = self.descriptionField.validate(display_error) && valid;

	if(display_error){
		self.generalBlock.removeClass('panel-danger');
		self.generalBlock.addClass('panel-primary');

		if(!valid){
			self.generalBlock.removeClass('panel-primary');
			self.generalBlock.addClass('panel-danger');
		}
	}

	return self.validateSnippets(display_error) && valid;
};

ModuleRenderer.prototype.validateSnippets = function(display_error){
	display_error = typeof display_error !== 'undefined' ? display_error : true;
	var valid = true;
	$(this.renderers).each(function(index, renderer){
		valid = renderer.validate(display_error) && valid;
	});
	return valid;
};

ModuleRenderer.prototype.hasSnippetData = function(){
	hasSnippets = false;
	$(this.renderers).each(function(index, renderer){
		data = renderer.getData(true);
		if(data.length){
			hasSnippets = true;
			return false;
		}
	});
	return hasSnippets;
}

ModuleRenderer.prototype.getData = function(){
	snippets = {};
	$(this.renderers).each(function(index, renderer){
		data = renderer.getData();
		if(data.length){
			snippets[renderer.config['name']] = data;
		}
	});
	
	return {
		package_name: this.packageField.value(),
		module_name: this.nameField.value(),
		description: this.descriptionField.value(),
		license: this.licenseField.value(),
		copyright: this.copyrightField.value(),
		magento_version: this.mainVersion,
		snippets: snippets
	};
};

ModuleRenderer.prototype.setData = function(data){
	this.packageField.value(data['package_name']);
	this.nameField.value(data['module_name']);
	this.descriptionField.value(data['description']);
	this.licenseField.value(data['license']);
	this.copyrightField.value(data['copyright']);

	$(this.renderers).each(function(index, renderer){
		if (renderer.config.name in data.snippets){
			renderer.setData(data.snippets[renderer.config.name]);
		}
	});
};

ModuleRenderer.prototype.change = function(callback){
	this.change_callback = callback;
}

/*****************************************************************************/
/*** Base snippet renderer                                                   */
/*****************************************************************************/
function SnippetRenderer(templates, config){
	var self = this;
	this.templates = templates;
	this.config = config;
	snippetClass = typeof config !== 'undefined' ? 'snippet-' + config['name'] : '';
};

SnippetRenderer.prototype.renderContainer = function(){
	var self = this;
	var template = $(this.templates).filter('#snippet-container-tmpl').html();
	html = $(Mustache.render(template, {snippet_name: this.config['label']}));

	this.containerDiv = html;
	this.counterSpan = html.find('.badge');
	this.bodyDiv = html.find('.panel-body');
	this.panelDiv = html.find('.panel-collapse'); 

	html.find('.add-button').click(function(){
		self.addOption();
	});
	
	// Help
	if(self.config.description != ''){
		var template = $(this.templates).filter('#snippet-help-popup-tmpl').html();
		var help_html = $(Mustache.render(template, {
			snippet_name: this.config['label'],
			description: self.config.description,
		}));

		html.find('.help-button').click(function(){
			$(help_html).modal('show');
		});

	}

	return html;
};

SnippetRenderer.prototype.search = function(search){
	var self = this;
	this.containerDiv.show();

	if(search != ''){
		var match = false;
		$.each(search.split(" "), function(index, search_item){
			search_item = search_item.trim().toLowerCase();
			if(search_item != '' && (self.config.name.toLowerCase().search(search_item) != -1 || self.config.description.toLowerCase().search(search_item) != -1)){
				match = true;
				return false;
			}
		});
		if(!match){
			this.containerDiv.hide();
		}
	}
}

SnippetRenderer.prototype.filter = function(filter){
	var self = this;
	this.containerDiv.show();

	console.log(filter);

	if(search != ''){
		var match = false;
		$.each(search.split(" "), function(index, search_item){
			search_item = search_item.trim().toLowerCase();
			if(search_item != '' && (self.config.name.toLowerCase().search(search_item) != -1 || self.config.description.toLowerCase().search(search_item) != -1)){
				match = true;
				return false;
			}
		});
		if(!match){
			this.containerDiv.hide();
		}
	}
}

SnippetRenderer.prototype.setSnippetInUseFlag = function(flag){
	var self = this;
	var snippetInUseFlag = flag;
	var snippetContainer = this.containerDiv;
	if(snippetInUseFlag === true){
		$(snippetContainer).addClass('is-in-use');
	}else {
		$(snippetContainer).removeClass('is-in-use');
	}
};

SnippetRenderer.prototype.setOptionsCount = function(count){
	this.counterSpan.html(count);

	// Set Snippet 'snippet_in_use' flag to true
	// when option count > 0
	// Used to be able to filter active snippets
	if(count > 0) {
		this.setSnippetInUseFlag(true);
	} else {
		this.setSnippetInUseFlag(false);
	}

};

SnippetRenderer.prototype.validate = function(){
	return true;
};

SnippetRenderer.prototype.getData = function(){
	return [];
};

SnippetRenderer.prototype.setData = function(){
	return [];
};

SnippetRenderer.prototype.change = function(callback){
	this.change_callback = callback;
}

/*****************************************************************************/
/*** Default snippet renderer                                                */
/*****************************************************************************/
function DefaultSnippetRenderer(templates, config){
	SnippetRenderer.call(this, templates, config);
	this.optionCount = 0;
	this.rows = {};
}
DefaultSnippetRenderer.prototype = new SnippetRenderer();

DefaultSnippetRenderer.prototype.validate = function(display_error){
	display_error = typeof display_error !== 'undefined' ? display_error : true;
	var self = this;
	var valid = true;

	this.containerDiv.removeClass('panel-danger');
	this.containerDiv.addClass('panel-primary');

	$.each(this.rows, function(index, fields){
		$.each(fields, function(index, field){
			valid = field.validate(display_error) && valid;
		});
	});
	
	if(display_error){
		if(!valid){
			this.containerDiv.removeClass('panel-primary');
			this.containerDiv.addClass('panel-danger');
		}
	}
	return valid;
};

DefaultSnippetRenderer.prototype.getData = function(all_data){
	all_data = typeof all_data !== 'undefined' ? all_data : false;
	var rows = [];
	$.each(this.rows, function(index, fields){
		var row = {extra_params: {}};
		var valid = true;
		$.each(fields, function(index, field){
			if(field.validate(false)){
				var regex = /^__extra__(.*)/g;
				match = regex.exec(field.param.name);
				if(match != null){
					row['extra_params'][match[1]] = field.value();
				} else {
					row[field.param.name] = field.value();
				}
			} else {
				valid = false;
				return false;
			}
		});

		if(all_data || valid){
			rows.push(row);
		}
	});
	return rows;
};

DefaultSnippetRenderer.prototype.getLastRowData = function(){
	var row_id = 0;
	$.each(this.rows, function(index, fields){
		row_id = index > row_id ? index : row_id;
	});

	var row = {};
	if(row_id != 0){
		$.each(this.rows[row_id], function(index, field){
			row[field.param.name] = field.value();
		});
	}
	return row;
}

DefaultSnippetRenderer.prototype.setData = function(data){
	var self = this;
	this.panelDiv.collapse('show');

	$.each(data, function(index, values){
		if('extra_params' in values){
			$.each(values['extra_params'], function(index, value){
				values['__extra__' + index] = value;
			});
		}
		self.addOption(values);
	});
};

DefaultSnippetRenderer.prototype.addOption = function(values){
	var self = this;
	var values = typeof values !== 'undefined' ? values : {};
	this.optionCount += 1;
	var row_id = this.optionCount;
	var fields = [];
	var last_row = this.getLastRowData();

	if(Object.keys(this.rows).length >= 100){
		alert('You cant add more ' + this.config['name']);
		return;
	}
	
	var template = $(this.templates).filter('#snippet-row-tmpl').html();
	var html = $(Mustache.render(template, {
		snippet_name: this.config['name'],
		has_extra_params: this.config['extra_params'].length > 0,
	}));
	var row = html.find('.snippet-fields');
	var row_extra = html.find('.snippet-fields-extra');

	// Add param fields
	$(this.config['params']).each(function(key, param){
		var field = new FieldRenderer(self.templates, self.config['name'], param, row_id);
		field.change(function(){
			if(typeof self.change_callback !== 'undefined'){
				self.change_callback();
			}
			/* notify all fields in row */
			self.rowUpdate(fields);
		})

		fields.push(field);
		row.append(field.renderField());

		//Fill field with last row data
		if(param['repeat'] && param['name'] in last_row){
			field.value(last_row[param['name']]);	
		}
		
		if(param['name'] in values){
			field.value(values[param['name']]);
		}
	});
	
	// add extra fields
	$(this.config['extra_params']).each(function(key, param){
		if(typeof param == 'string'){
			sep = $("<div class='col-xs-12 extra-param-title'>").text(param);
			row_extra.append(sep);	
		} else {
			var field = new FieldRenderer(self.templates, self.config['name'], param, row_id, 'col-xs-4', 'col-xs-4');
			field.change(function(){
				if(typeof self.change_callback !== 'undefined'){
					self.change_callback();
				}
				/* notify all fields in row */
				self.rowUpdate(fields);
			})
			fields.push(field);
			row_extra.append(field.renderField());

			//Fill field with last row data
			if(param['repeat'] && param['name'] in last_row){
				field.value(last_row[param['name']]);	
			}
			
			if(param['name'] in values){
				field.value(values[param['name']]);
			}

		}
	});

	this.rowUpdate(fields);
	this.rows[row_id] = fields;

	// Add close button
	html.find('.remove').click(function(){
		delete self.rows[row_id];
		html.slideUp('.2s', function(){ html.remove(); });
		self.setOptionsCount(Object.keys(self.rows).length);

		if(typeof self.change_callback !== 'undefined'){
			self.change_callback();
		}
	});

	// Append row
	html.appendTo(self.bodyDiv).hide().slideDown('.2s');

	this.setOptionsCount(Object.keys(this.rows).length);

	// Enable popover help
	$('[data-toggle="popover"]').popover({
    	container: 'body'
	});

	if(typeof self.change_callback !== 'undefined'){
		self.change_callback();
	}
};

DefaultSnippetRenderer.prototype.rowUpdate = function(fields){
	var data = {};
	$(fields).each(function(index, field){
		data[field.param.name] = field.value();
	});
	
	$(fields).each(function(index, field){
		field.rowUpdate(data);
	});
}

/*****************************************************************************/
/*** Field renderer                                                          */
/*****************************************************************************/
function FieldRenderer(templates, snippet_name, param, row_id, bootstrap_col, focus_bootstrap_col){
	this.templates = templates
	this.snippetName = snippet_name;
	this.param = param;
	this.rowId = row_id;
	this.bootstrap_col = typeof bootstrap_col !== 'undefined' ? bootstrap_col : 'col-xs-4';
	this.focus_bootstrap_col = typeof focus_bootstrap_col !== 'undefined' ? focus_bootstrap_col : 'col-xs-4';
	this.field_hidden = false;
}

FieldRenderer.prototype.getId = function(){
	return this.snippetName + '-' + this.param['name'] + '-' + this.rowId;
};

FieldRenderer.prototype.getDefaultValue = function(){
	return((this.param['default'] == null) ? '' : this.param['default']);
};
FieldRenderer.prototype.value = function(value){
	if(this.param['yes_no']){
		if(typeof value !== 'undefined'){
			return this.field.prop('checked', value);;
		}
		return this.field.is(':checked');
	}

	if(typeof value !== 'undefined'){
		return this.field.val(value);
	}
	return this.field.val();
};

FieldRenderer.prototype.renderField = function(){
	var self = this;

	if(this.field_hidden){
		return '';
	}

	if(this.param['yes_no']){
		var template = $(this.templates).filter('#snippet-field-checkbox-tmpl').html();
		var html = $(Mustache.render(template, {
			label: self.param['label'],
			field_id: self.getId(),
			bs_col: self.bootstrap_col,
			show_help: this.param['description'] != '',
			help_text: this.param['description'],
		}));

	} else if(this.param['choises']) {
		var template = $(this.templates).filter('#snippet-field-select-tmpl').html();
		//Create options
		var options = $('<div>');
		$(this.param['choises']).each(function(index, value){
			options.append($('<option>').attr("value",value[0]).text(value[1]));
		});
		
		// Render template
		var html = $(Mustache.render(template, {
			options: options.html(),
			label: self.param['label'],
			field_id: self.getId(),
			bs_col: self.bootstrap_col,
			show_help: this.param['description'] != '',
			help_text: this.param['description'],
			multi: this.param['multiple_choices'] ? 'size="3" multiple="multiple"' : '',
		}));
	} else {
		var template = $(this.templates).filter('#snippet-field-text-tmpl').html();
		var html = $(Mustache.render(template, {
			label: self.param['label'],
			field_id: self.getId(),
			bs_col: self.bootstrap_col,
			show_help: this.param['description'] != '',
			help_text: this.param['description'],
		}));
		html.find('#' + self.getId()).focus(function() {
			self.containerDiv.removeClass(self.bootstrap_col);
			self.containerDiv.addClass(self.focus_bootstrap_col);
		}).focusout(function() {
			self.containerDiv.removeClass(self.focus_bootstrap_col);
			self.containerDiv.addClass(self.bootstrap_col);
		});
	}

	this.field = html.find('#' + self.getId());
	this.value(this.getDefaultValue());
	this.containerDiv = html;	
	this.formGroupDiv = html.find('.form-group');
	this.helpBlock = html.find('.help-block');

	this.field.change(function(){
		self.validate();
		if(typeof self.change_callback !== 'undefined'){
			self.change_callback();
		}
	})

	
	return html;
};

FieldRenderer.prototype.validate = function(display_error){
	display_error = typeof display_error !== 'undefined' ? display_error : true;

	if(this.field_hidden){
		return true;
	}

	if(this.param['yes_no']){
		return true;
	}
	
	// Reset errors
	if(display_error){
		this.formGroupDiv.removeClass('has-error');
		this.helpBlock.text('');
	}

	// Check if not empty
	var value = this.field.val();
	if(value != null && typeof value == 'object'){
		value = value.join();
	}
	if(value == '' || value == null){
		if(this.param['required']){
			if(display_error){
				this.formGroupDiv.addClass('has-error');
				this.helpBlock.text('This field is required');
			}
			return false;
		}
	} else if(this.param['regex_validator'] != null 
		&& !value.match(new RegExp(this.param['regex_validator'], 'g'))){
		if(display_error){
			this.formGroupDiv.addClass('has-error');
			this.helpBlock.text(this.param['error_message']);
		}
		return false;
	}
	return true;
};

FieldRenderer.prototype.change = function(callback){
	this.change_callback = callback;
}

FieldRenderer.prototype.rowUpdate = function(data){
	if(this.param.depend != null){
		var show = true;
		for (var key in this.param.depend) {
			if(!data[key].match(new RegExp(this.param.depend[key], 'g'))){
				show = false;
			}
		}
		if(show){
			this.show();
			this.field_hidden = false;
		} else {
			this.hide();
			this.field_hidden = true;
		}
	}
}

FieldRenderer.prototype.show = function(){
	this.containerDiv.show();
}

FieldRenderer.prototype.hide = function(){
	this.containerDiv.hide();
}
