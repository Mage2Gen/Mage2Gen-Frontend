;(function ( $, window, document, undefined ) {
    
    $.fn.copyToClipboard = function() {

        var _
        var _this = this;

        _this.copy = function(target) {
            var eventTarget = _this;
            var range = document.createRange();  
            range.selectNode(target[0]);  
            window.getSelection().addRange(range);

            // copy the selection
            var succeed;
            try {
                succeed = document.execCommand("copy");
                console.log("Copy command was successful"); 
                _this.toggleSuccessButton(eventTarget);
            } catch(e) {
                succeed = false;
                console.log("Oops, unable to copy"); 
                _this.toggleSuccessButton(eventTarget);
            }
            
            window.getSelection().removeAllRanges();
        }

        _this.toggleSuccessButton = function(target) {
            target.toggleClass("btn-success btn-default");
            target.children('.glyphicon-ok').toggle();
            setTimeout(function(){
                target.toggleClass("btn-success btn-default");
                target.children('.glyphicon-ok').toggle();
            }, 500);
        }

        return _this;

    };

}( jQuery, window, document ))


$(document).on("ready", function(){
    $("body").on("click", ".copy-button", function(){
        $(this).copyToClipboard().copy(jQuery(".copy-target"));
    })
    $("body").on("click", ".copy-file-path-button", function(){
        $(this).copyToClipboard().copy(jQuery("#mage2-selected-file-name"));
    })
});