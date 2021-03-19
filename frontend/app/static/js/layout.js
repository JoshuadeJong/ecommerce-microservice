// SnackBar + Flash Messages
function r(f){/in/.test(document.readyState)?setTimeout('r('+f+')',9):f()}

r( function() {
    // Grab Data from html
        let flashMessage = document.getElementById('flash_message')
        let flashCategory = document.getElementById('flash_category')

        // Display Snackbar
        if (flashMessage && flashCategory){
            let notification = document.getElementById('snackbar');
            notification.MaterialSnackbar.showSnackbar({
                message: flashMessage.innerText
            });
        }
    }
)

